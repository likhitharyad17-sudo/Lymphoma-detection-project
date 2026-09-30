import io
import cv2
import numpy as np
from PIL import Image

class ImageValidator:
    """
    Multi-Tier Histopathology Specimen Gating & Out-of-Distribution Rejection Engine.
    Strictly validates that uploaded images are microscopic lymphoid biopsy slides (H&E stained).
    Automatically rejects:
    - Natural scenery, foliage, trees, outdoor photos
    - Everyday objects, food, faces, animals, vehicles
    - Blurry, macroscopic, blank, pitch-black, or unreadable files
    """
    @staticmethod
    def validate_image(image_bytes: bytes):
        if not image_bytes or len(image_bytes) < 100:
            return False, "Uploaded file is empty or corrupted."

        # Attempt to decode as PIL Image
        try:
            pil_img = Image.open(io.BytesIO(image_bytes))
            pil_img.verify()
            pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except Exception as e:
            return False, f"Unsupported or unreadable image format ({e}). Please upload a valid TIFF, PNG, or JPEG file."

        w, h = pil_img.size
        if w < 64 or h < 64:
            return False, f"Image resolution too small ({w}x{h}). Minimum required resolution is 64x64."

        np_img = np.array(pil_img)
        total_pixels = float(w * h)

        # 1. Blank, Pitch-Black, or Uniform Field Check
        mean_val = np.mean(np_img)
        std_dev = np.std(np_img)
        if mean_val < 5.0:
            return False, "Image is completely pitch black with no cellular tissue."
        if mean_val > 250.0:
            return False, "Image is completely blank white with no cellular structure."
        if std_dev < 8.0:
            return False, "Image contains almost zero contrast (uniform or blank field)."

        # 2. Histopathology Stain Chromaticity Analysis (H&E / Giemsa Spectrum)
        hsv = cv2.cvtColor(np_img, cv2.COLOR_RGB2HSV)
        h_chan, s_chan, v_chan = cv2.split(hsv)

        # Natural Green / Yellow foliage & daylight scenery (Hue [26, 88], Saturation >= 25, Value >= 25)
        # These colors are completely absent in microscopic lymphoid biopsies.
        green_yellow_mask = (h_chan >= 26) & (h_chan <= 88) & (s_chan >= 25) & (v_chan >= 25)
        green_yellow_ratio = np.sum(green_yellow_mask) / total_pixels
        if green_yellow_ratio > 0.10:
            return False, (
                f"Non-histological image detected: The image contains natural environmental colors ({green_yellow_ratio*100:.1f}% foliage/daylight scenery). "
                "Only microscopic histopathology slides (H&E stained lymphoid biopsies) are accepted."
            )

        # Histological Tissue Stain Spectrum:
        # Hematoxylin (Blue/Purple/Violet: Hue [95, 180]) + Eosin (Pink/Magenta/Red: Hue [175, 180] or [0, 25]) + Pale Glass Background (Saturation < 22)
        stain_or_glass_mask = ((h_chan >= 95) & (h_chan <= 180)) | (h_chan <= 25) | (s_chan < 22)
        stain_ratio = np.sum(stain_or_glass_mask) / total_pixels
        if stain_ratio < 0.70:
            return False, (
                f"Non-histological image detected: Color profile does not match Hematoxylin & Eosin (H&E) staining ({stain_ratio*100:.1f}% match). "
                "Please upload a valid microscopic biopsy slide."
            )

        # 3. Microscopic Edge Granularity & Cellular Gradient Density
        # High-power microscopic lymphoid biopsies contain dense microscopic cell nuclei, producing high spatial frequency edges.
        # Everyday macroscopic photos (food, objects, faces) have smooth surfaces or bokeh blur with low edge density.
        gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
        gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
        mag = cv2.magnitude(gx, gy)
        edge_ratio = np.sum(mag > 35) / total_pixels
        if edge_ratio < 0.35:
            return False, (
                f"Non-histological image detected: Insufficient microscopic cellular structure ({edge_ratio*100:.1f}% edge density). "
                "Lymphoma diagnosis requires high-power microscopic lymphoid biopsy specimens with clear cellular architecture."
            )

        return True, "Valid histopathological biopsy slide."
