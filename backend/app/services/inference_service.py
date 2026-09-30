import os
import io
import uuid
import datetime
import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.database.models import PredictionRecord, User
from backend.app.schemas.prediction import PredictionResponse, ProbabilityBreakdown
from backend.training.architectures.attention_residual_net import AttentionResNet50_CBAM
from backend.training.explainability.gradcam import GradCAMPlusPlus, overlay_heatmap_on_image
from backend.training.data.dataset import get_eval_transforms
from backend.app.services.image_validator import ImageValidator

MORPHOLOGY_KNOWLEDGE = {
    "CLL": "Diffuse effacement by small, mature round lymphocytes with heavily clumped chromatin (soccer-ball pattern), indistinct nucleoli, and scant cytoplasm.",
    "FL": "Nodular architectural pattern of closely packed neoplastic follicles composed of centrocytes (cleaved nuclei) and centroblasts (vesicular nuclei with peripheral nucleoli).",
    "MCL": "Monotonous expansion of mantle zone or diffuse pattern of small-to-medium lymphocytes with irregular, cleaved nuclear contours and hyalinized blood vessels."
}

class InferenceService:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.gradcam = None
        self.eval_transform = get_eval_transforms(image_size=settings.IMAGE_SIZE)
        self._load_model()

    def _load_model(self):
        try:
            self.model = AttentionResNet50_CBAM(num_classes=settings.NUM_CLASSES, pretrained=False)
            model_path = settings.BEST_MODEL_PATH
            if os.path.exists(model_path):
                state_dict = torch.load(model_path, map_location=self.device)
                self.model.load_state_dict(state_dict)
                print(f"Loaded trained lymphoma model from: {model_path}")
            else:
                print(f"Warning: Model weight file not found at {model_path}. Using initial weights.")
            
            self.model.to(self.device)
            self.model.eval()

            self.gradcam = GradCAMPlusPlus(self.model, self.model.cbam4)
        except Exception as e:
            print(f"Error initializing InferenceService model: {e}")

    def predict_image(
        self,
        file_bytes: bytes,
        filename: str,
        db: Session,
        current_user: User = None,
        custom_threshold: float = None,
        is_private: bool = False
    ) -> PredictionResponse:
        case_id = f"CASE-{uuid.uuid4().hex[:8].upper()}"
        threshold = custom_threshold if custom_threshold is not None else settings.LYMPHOMA_CONFIDENCE_THRESHOLD
        now = datetime.datetime.utcnow()

        user_id = current_user.id if current_user else None
        user_email = current_user.email if current_user else None
        user_name = current_user.full_name if current_user else None

        # Step 1: Multi-Tier Histopathology Gating & Slide Validation
        is_valid, val_msg = ImageValidator.validate_image(file_bytes)
        if not is_valid:
            rec = PredictionRecord(
                case_id=case_id,
                user_id=user_id,
                user_email=user_email,
                user_name=user_name,
                file_name=filename,
                outcome="UNABLE_TO_ANALYZE",
                threshold_used=threshold,
                rejection_reason=val_msg,
                is_private=is_private,
                is_hidden_by_admin=False,
                created_at=now
            )
            db.add(rec)
            db.commit()
            db.refresh(rec)

            return PredictionResponse(
                id=rec.id,
                case_id=case_id,
                user_id=user_id,
                user_email=user_email,
                user_name=user_name,
                file_name=filename,
                outcome="UNABLE_TO_ANALYZE",
                outcome_display="Unable to Analyze Image",
                threshold_used=threshold,
                rejection_reason=val_msg,
                model_version=settings.ACTIVE_MODEL_VERSION,
                is_hidden_by_admin=False,
                is_private=is_private,
                created_at=now
            )

        # Step 2: Preprocess Image
        pil_img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        img_tensor = self.eval_transform(pil_img).unsqueeze(0).to(self.device)

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

        # Step 4: Two-Stage Rejection / Screening Logic
        if top_conf >= threshold:
            outcome = "LYMPHOMA_DETECTED"
            outcome_display = "Lymphoma Detected"
            rejection_reason = None
            morphology = MORPHOLOGY_KNOWLEDGE.get(top_class, "")

            # Step 5: Grad-CAM++ Attention Heatmap Overlay
            cam, _ = self.gradcam.generate(img_tensor, target_class=top_idx)
            heatmap_img = overlay_heatmap_on_image(pil_img, cam, alpha=0.45)
            
            heatmap_filename = f"{case_id}_gradcam.jpg"
            heatmap_path = os.path.join(settings.UPLOADS_DIR, "heatmaps", heatmap_filename)
            heatmap_img.save(heatmap_path, format="JPEG", quality=95)
            heatmap_url = f"/uploads/heatmaps/{heatmap_filename}"
        else:
            outcome = "NO_LYMPHOMA_DETECTED"
            outcome_display = "No Lymphoma Detected"
            rejection_reason = (
                f"The highest classification confidence ({top_conf * 100:.2f}%) is below the screening threshold ({threshold * 100:.0f}%). "
                "The specimen is not confidently classified as CLL, FL, or MCL."
            )
            top_class = None
            top_class_full = None
            heatmap_url = None
            heatmap_path = None
            morphology = None

        # Step 6: Persist Record
        rec = PredictionRecord(
            case_id=case_id,
            user_id=user_id,
            user_email=user_email,
            user_name=user_name,
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
            heatmap_path=heatmap_path,
            report_path=None,
            is_hidden_by_admin=False,
            is_private=is_private,
            notes=morphology,
            created_at=now
        )
        db.add(rec)
        db.commit()
        db.refresh(rec)

        return PredictionResponse(
            id=rec.id,
            case_id=case_id,
            user_id=user_id,
            user_email=user_email,
            user_name=user_name,
            file_name=filename,
            outcome=outcome,
            outcome_display=outcome_display,
            predicted_subtype=top_class,
            predicted_subtype_full=top_class_full,
            confidence=top_conf if outcome == "LYMPHOMA_DETECTED" else None,
            confidence_percentage=f"{top_conf * 100:.2f}%" if outcome == "LYMPHOMA_DETECTED" else None,
            probabilities=ProbabilityBreakdown(**prob_dict),
            top_probabilities=prob_dict,
            predicted_class=top_class,
            threshold_used=threshold,
            rejection_reason=rejection_reason,
            heatmap_url=heatmap_url,
            original_url=orig_url,
            report_url=f"/api/reports/{case_id}/pdf",
            morphology_summary=morphology,
            model_version=settings.ACTIVE_MODEL_VERSION,
            is_hidden_by_admin=False,
            is_private=is_private,
            created_at=now
        )

inference_service = InferenceService()
