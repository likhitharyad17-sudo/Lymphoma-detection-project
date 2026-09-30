import os
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
