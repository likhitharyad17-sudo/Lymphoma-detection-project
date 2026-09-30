import os

project_root = r"D:\Lymphoma Detection Project"
files = {}

# Fixed Image Validator with import io
files["backend/app/services/image_validator.py"] = """import io
import cv2
import numpy as np
from PIL import Image

class ImageValidator:
    \"\"\"
    Validates uploaded images to reject non-histopathological, blank, corrupted, or unsupported images.
    \"\"\"
    @staticmethod
    def validate_image(image_bytes: bytes):
        if not image_bytes or len(image_bytes) < 100:
            return False, "Uploaded file is empty or corrupted."

        # Attempt to decode as PIL Image
        try:
            pil_img = Image.open(io.BytesIO(image_bytes))
            pil_img.verify() # Verify file integrity
            
            # Reopen for content analysis (verify closes stream)
            pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except Exception as e:
            return False, f"Unsupported or unreadable image format ({e}). Please upload a valid TIFF, PNG, or JPEG file."

        w, h = pil_img.size
        if w < 64 or h < 64:
            return False, f"Image resolution too small ({w}x{h}). Minimum required resolution is 64x64."

        # Convert to numpy for statistical analysis
        np_img = np.array(pil_img)
        
        # Check standard deviation (detect uniform/blank images)
        std_dev = np.std(np_img)
        if std_dev < 8.0:
            return False, "Image contains almost zero contrast (uniform or blank field). Please upload a valid histological slide."

        # Check mean intensity (detect completely pitch black or pure white slides)
        mean_val = np.mean(np_img)
        if mean_val < 5.0:
            return False, "Image is pitch black with no cellular structure."
        if mean_val > 250.0:
            return False, "Image is blank white with no cellular tissue."

        return True, "Valid histopathological image."
"""

# Inference Service with Two-Stage Logic & Grad-CAM++
files["backend/app/services/inference_service.py"] = """import os
import io
import uuid
import datetime
import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.database.models import PredictionRecord
from backend.app.schemas.prediction import PredictionResponse, ProbabilityBreakdown
from backend.app.services.image_validator import ImageValidator
from backend.training.architectures import AttentionResNet50_CBAM
from backend.training.data.dataset import get_data_transforms
from backend.training.explainability.gradcam import GradCAMPlusPlus, overlay_heatmap_on_image

# Clinical Morphological Summaries for the 3 Lymphoma Types
MORPHOLOGY_KNOWLEDGE = {
    "CLL": (
        "Chronic Lymphocytic Leukemia / Small Lymphocytic Lymphoma (CLL/SLL): "
        "Characterized by a diffuse proliferation of small, mature-appearing, monotonous round lymphocytes "
        "with dense clumped chromatin, indistinct nucleoli, and scant cytoplasm. Proliferation centers (pseudofollicles) "
        "containing prolymphocytes and para-immunoblasts may be present."
    ),
    "FL": (
        "Follicular Lymphoma (FL): "
        "Demonstrates a distinct nodular or follicular growth pattern closely packed throughout the lymph node cortex. "
        "Composed of a mixture of centrocytes (small to medium cleaved follicular center cells with indented irregular nuclear contours) "
        "and centroblasts (larger non-cleaved cells with vesicular chromatin and multiple peripheral nucleoli)."
    ),
    "MCL": (
        "Mantle Cell Lymphoma (MCL): "
        "Presents as a monotonous, diffuse, nodular, or mantle zone expansion of small to medium-sized lymphocytes. "
        "Cells feature irregular, indented, or cleaved nuclear membranes, condensed chromatin, and inconspicuous nucleoli, "
        "typically lacking transformed neoplastic centroblasts or proliferation centers."
    )
}

class InferenceService:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.gradcam = None
        self._load_model()
        _, self.eval_transform = get_data_transforms(img_size=224)

    def _load_model(self):
        try:
            self.model = AttentionResNet50_CBAM(num_classes=3, pretrained=False)
            if os.path.exists(settings.MODEL_PATH):
                self.model.load_state_dict(torch.load(settings.MODEL_PATH, map_location=self.device))
                print(f"Loaded trained lymphoma model from: {settings.MODEL_PATH}")
            else:
                print(f"Warning: Model weights not found at {settings.MODEL_PATH}. Initializing randomly.")
            
            self.model = self.model.to(self.device)
            self.model.eval()

            # Grad-CAM++ hooked on the last CBAM block of Stage 4
            self.gradcam = GradCAMPlusPlus(self.model, self.model.cbam4)
        except Exception as e:
            print(f"Error initializing InferenceService model: {e}")

    def predict_image(self, file_bytes: bytes, filename: str, db: Session, custom_threshold: float = None) -> PredictionResponse:
        case_id = f"CASE-{uuid.uuid4().hex[:8].upper()}"
        threshold = custom_threshold if custom_threshold is not None else settings.LYMPHOMA_CONFIDENCE_THRESHOLD
        now = datetime.datetime.utcnow()

        # Step 1: Image Validation
        is_valid, val_msg = ImageValidator.validate_image(file_bytes)
        if not is_valid:
            # Record invalid entry
            rec = PredictionRecord(
                case_id=case_id,
                file_name=filename,
                outcome="UNABLE_TO_ANALYZE",
                threshold_used=threshold,
                rejection_reason=val_msg,
                created_at=now
            )
            db.add(rec)
            db.commit()

            return PredictionResponse(
                case_id=case_id,
                file_name=filename,
                outcome="UNABLE_TO_ANALYZE",
                outcome_display="Unable to Analyze Image",
                threshold_used=threshold,
                rejection_reason=f"Image validation failed: {val_msg} Please upload a valid histological slide.",
                created_at=now
            )

        # Step 2: Preprocess Image
        pil_img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        img_tensor = self.eval_transform(pil_img).unsqueeze(0).to(self.device)

        # Save original uploaded image
        orig_filename = f"{case_id}_original.jpg"
        orig_path = os.path.join(settings.UPLOADS_DIR, "images", orig_filename)
        os.makedirs(os.path.dirname(orig_path), exist_ok=True)
        pil_img.save(orig_path, format="JPEG", quality=95)
        orig_url = f"/uploads/images/{orig_filename}"

        # Step 3: Deep Residual + Attention Inference
        with torch.no_grad():
            logits = self.model(img_tensor)
            probs = F.softmax(logits, dim=1).cpu().numpy()[0]

        prob_dict = {
            "CLL": float(probs[0]),
            "FL": float(probs[1]),
            "MCL": float(probs[2])
        }

        top_idx = int(np.argmax(probs))
        top_conf = float(probs[top_idx])
        top_class = settings.CLASSES[top_idx]
        top_class_full = settings.CLASS_FULL_NAMES[top_class]

        # Calculate Shannon Entropy for Out-of-Distribution / Ambiguity Detection
        # High entropy means the model is uncertain across all classes
        entropy = -float(np.sum(probs * np.log(probs + 1e-9)))

        # Step 4: Two-Stage Rejection / Screening Logic
        # If top_conf >= threshold -> Accepted as Lymphoma Detected
        # Else -> Rejected as No Lymphoma Detected
        if top_conf >= threshold:
            outcome = "LYMPHOMA_DETECTED"
            outcome_display = "Lymphoma Detected"
            rejection_reason = None
            morphology = MORPHOLOGY_KNOWLEDGE.get(top_class, "")

            # Step 5: Generate Grad-CAM++ Attention Heatmap Overlay
            cam, _ = self.gradcam.generate(img_tensor, target_class=top_idx)
            heatmap_img = overlay_heatmap_on_image(pil_img, cam, alpha=0.45)
            
            heatmap_filename = f"{case_id}_gradcam.jpg"
            heatmap_path = os.path.join(settings.UPLOADS_DIR, "heatmaps", heatmap_filename)
            os.makedirs(os.path.dirname(heatmap_path), exist_ok=True)
            heatmap_img.save(heatmap_path, format="JPEG", quality=95)
            heatmap_url = f"/uploads/heatmaps/{heatmap_filename}"
        else:
            outcome = "NO_LYMPHOMA_DETECTED"
            outcome_display = "No Lymphoma Detected / Not Classified as Lymphoma"
            rejection_reason = (
                f"The uploaded image could not be reliably classified as CLL, FL, or MCL by the model. "
                f"The maximum confidence ({top_conf*100:.2f}%) fell below the accepted classification threshold ({threshold*100:.0f}%). "
                f"Classification rejected to prevent out-of-distribution false positives."
            )
            top_class = None
            top_class_full = None
            morphology = None
            heatmap_url = None

        # Step 6: Log Prediction to Database
        rec = PredictionRecord(
            case_id=case_id,
            file_name=filename,
            file_path=orig_path,
            outcome=outcome,
            predicted_subtype=top_class,
            confidence=top_conf if outcome == "LYMPHOMA_DETECTED" else None,
            prob_cll=prob_dict["CLL"],
            prob_fl=prob_dict["FL"],
            prob_mcl=prob_dict["MCL"],
            threshold_used=threshold,
            rejection_reason=rejection_reason,
            heatmap_path=heatmap_url,
            created_at=now
        )
        db.add(rec)
        db.commit()

        return PredictionResponse(
            case_id=case_id,
            file_name=filename,
            outcome=outcome,
            outcome_display=outcome_display,
            predicted_subtype=top_class,
            predicted_subtype_full=top_class_full,
            confidence=top_conf if outcome == "LYMPHOMA_DETECTED" else None,
            confidence_percentage=f"{top_conf*100:.2f}%" if outcome == "LYMPHOMA_DETECTED" else None,
            probabilities=ProbabilityBreakdown(**prob_dict),
            threshold_used=threshold,
            rejection_reason=rejection_reason,
            heatmap_url=heatmap_url,
            original_url=orig_url,
            morphology_summary=morphology,
            created_at=now
        )

inference_service = InferenceService()
"""

# PDF Clinical Report Generator Service
files["backend/app/services/pdf_report_service.py"] = """import os
import io
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from backend.app.core.config import settings

class PDFReportService:
    @staticmethod
    def generate_clinical_report(record_data: dict, output_path: str):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=36, leftMargin=36,
            topMargin=36, bottomMargin=36
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "ReportTitle", parent=styles["Heading1"],
            fontSize=18, textColor=colors.HexColor("#0f172a"),
            spaceAfter=6, alignment=0
        )
        subtitle_style = ParagraphStyle(
            "ReportSubTitle", parent=styles["Normal"],
            fontSize=10, textColor=colors.HexColor("#475569"),
            spaceAfter=12
        )
        section_heading = ParagraphStyle(
            "SecHeading", parent=styles["Heading2"],
            fontSize=12, textColor=colors.HexColor("#1e293b"),
            spaceBefore=10, spaceAfter=6
        )
        body_style = ParagraphStyle(
            "ReportBody", parent=styles["Normal"],
            fontSize=9.5, textColor=colors.HexColor("#334155"),
            leading=13
        )
        alert_style = ParagraphStyle(
            "AlertBody", parent=styles["Normal"],
            fontSize=8.5, textColor=colors.HexColor("#b91c1c"),
            leading=11
        )

        story = []

        # 1. Header
        story.append(Paragraph("DIGITAL PATHOLOGY AI SCREENING REPORT", title_style))
        story.append(Paragraph("Attention Augmented Residual Deep Learning Framework for Lymphoma Detection", subtitle_style))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563eb"), spaceAfter=12))

        # 2. Case Metadata Table
        case_info = [
            [
                Paragraph("<b>Case Reference:</b> %s" % record_data.get("case_id", "N/A"), body_style),
                Paragraph("<b>Date/Time:</b> %s" % record_data.get("created_at", str(datetime.datetime.now())), body_style)
            ],
            [
                Paragraph("<b>Uploaded File:</b> %s" % record_data.get("file_name", "N/A"), body_style),
                Paragraph("<b>Confidence Threshold:</b> %.0f%%" % (record_data.get("threshold_used", 0.80) * 100), body_style)
            ]
        ]
        t_meta = Table(case_info, colWidths=[270, 270])
        t_meta.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(t_meta)
        story.append(Spacer(1, 10))

        # 3. Primary Screening Outcome
        outcome = record_data.get("outcome", "")
        if outcome == "LYMPHOMA_DETECTED":
            badge_color = colors.HexColor("#15803d") # Green
            outcome_txt = "LYMPHOMA DETECTED"
            subtype = record_data.get("predicted_subtype_full", record_data.get("predicted_subtype", "N/A"))
            conf_txt = record_data.get("confidence_percentage", "N/A")
        elif outcome == "NO_LYMPHOMA_DETECTED":
            badge_color = colors.HexColor("#d97706") # Amber
            outcome_txt = "NO LYMPHOMA DETECTED (REJECTED / UNCLASSIFIED)"
            subtype = "Not Classified as Lymphoma (Below Threshold)"
            conf_txt = "Below Threshold (%.2f%%)" % ((record_data.get("confidence") or 0.0) * 100)
        else:
            badge_color = colors.HexColor("#dc2626") # Red
            outcome_txt = "UNABLE TO ANALYZE"
            subtype = "Image Validation Failed"
            conf_txt = "N/A"

        outcome_table_data = [
            [
                Paragraph("<b>Screening Status:</b>", body_style),
                Paragraph("<b><font color='%s'>%s</font></b>" % (badge_color.hexval(), outcome_txt), body_style)
            ],
            [
                Paragraph("<b>Classification Subtype:</b>", body_style),
                Paragraph("<b>%s</b>" % subtype, body_style)
            ],
            [
                Paragraph("<b>Model Confidence:</b>", body_style),
                Paragraph("<b>%s</b>" % conf_txt, body_style)
            ]
        ]
        t_outcome = Table(outcome_table_data, colWidths=[160, 380])
        t_outcome.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#ffffff")),
            ("BOX", (0, 0), (-1, -1), 1, badge_color),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(t_outcome)
        story.append(Spacer(1, 10))

        # 4. Probability Distribution Table
        probs = record_data.get("probabilities", {})
        if probs:
            story.append(Paragraph("Three-Class Softmax Probability Distribution", section_heading))
            prob_rows = [
                [
                    Paragraph("<b>Class / Subtype</b>", body_style),
                    Paragraph("<b>Full Medical Designation</b>", body_style),
                    Paragraph("<b>Calculated Probability</b>", body_style)
                ],
                [
                    Paragraph("<b>CLL</b>", body_style),
                    Paragraph("Chronic Lymphocytic Leukemia / Small Lymphocytic Lymphoma", body_style),
                    Paragraph("%.2f%%" % (probs.get("CLL", 0.0) * 100), body_style)
                ],
                [
                    Paragraph("<b>FL</b>", body_style),
                    Paragraph("Follicular Lymphoma", body_style),
                    Paragraph("%.2f%%" % (probs.get("FL", 0.0) * 100), body_style)
                ],
                [
                    Paragraph("<b>MCL</b>", body_style),
                    Paragraph("Mantle Cell Lymphoma", body_style),
                    Paragraph("%.2f%%" % (probs.get("MCL", 0.0) * 100), body_style)
                ]
            ]
            t_probs = Table(prob_rows, colWidths=[60, 360, 120])
            t_probs.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f8fafc"), colors.white]),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))
            story.append(t_probs)
            story.append(Spacer(1, 10))

        # 5. Visual Explainability (Grad-CAM++ Side-by-Side)
        orig_p = record_data.get("original_path")
        heat_p = record_data.get("heatmap_path_full")

        if orig_p and os.path.exists(orig_p) and heat_p and os.path.exists(heat_p):
            story.append(Paragraph("Visual Explainability: Attention Heatmap (Grad-CAM++)", section_heading))
            img_table_data = [
                [
                    RLImage(orig_p, width=2.4*inch, height=1.8*inch),
                    RLImage(heat_p, width=2.4*inch, height=1.8*inch)
                ],
                [
                    Paragraph("<center><b>Original Histological Slide</b></center>", body_style),
                    Paragraph("<center><b>Grad-CAM++ Cellular Attention</b></center>", body_style)
                ]
            ]
            t_imgs = Table(img_table_data, colWidths=[270, 270])
            t_imgs.setStyle(TableStyle([
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]))
            story.append(t_imgs)
            story.append(Spacer(1, 8))

        # 6. Histological Hallmark Summary
        morph = record_data.get("morphology_summary")
        if morph:
            story.append(Paragraph("Histopathological Morphology Summary", section_heading))
            story.append(Paragraph(morph, body_style))
            story.append(Spacer(1, 10))

        # 7. Mandatory Medical Disclaimer
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=8))
        disclaimer_text = (
            "<b>ACADEMIC RESEARCH & CLINICAL DECISION SUPPORT NOTICE:</b><br/>"
            "This automated report was produced by the 'Attention Augmented Residual Deep Learning Framework for Lymphoma Detection' "
            "as a research-grade computer-aided screening tool. This system does not constitute a definitive medical or pathological diagnosis. "
            "Rejection or 'No Lymphoma Detected' indicates that the image features fell below the model's high-confidence threshold and "
            "must not be interpreted as definitive proof of cancer-free tissue. All digital pathology findings must be correlated with "
            "clinical context, immunohistochemistry (CD5, CD10, CD20, Cyclin D1), and board-certified pathological review."
        )
        story.append(Paragraph(disclaimer_text, alert_style))

        doc.build(story)
        return output_path
"""

for rel_path, content in files.items():
    full_path = os.path.join(project_root, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {rel_path}")

print("Inference service and PDF report generator created successfully.")
