import torch
import torch.nn.functional as F
import numpy as np
import cv2
from PIL import Image

class GradCAMPlusPlus:
    """
    Grad-CAM++ (Generalized Gradient-weighted Class Activation Mapping).
    Computes higher-order pixel-level gradient weights to capture multiple instances
    and finer morphological structures in histopathological imagery.
    """
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        self.hook_handles = []
        self._register_hooks()

    def _register_hooks(self):
        def forward_hook(module, input, output):
            self.activations = output.detach()

        def backward_hook(module, grad_in, grad_out):
            self.gradients = grad_out[0].detach()

        self.hook_handles.append(self.target_layer.register_forward_hook(forward_hook))
        self.hook_handles.append(self.target_layer.register_full_backward_hook(backward_hook))

    def generate(self, input_tensor, target_class=None):
        self.model.eval()
        self.model.zero_grad()

        # Forward pass
        logits = self.model(input_tensor)

        if target_class is None:
            target_class = torch.argmax(logits, dim=1).item()

        score = logits[0, target_class]
        score.backward(retain_graph=True)

        grads = self.gradients[0] # [C, H, W]
        acts = self.activations[0] # [C, H, W]

        grads_pow2 = grads ** 2
        grads_pow3 = grads ** 3

        sum_acts = acts.sum(dim=(1, 2), keepdim=True)
        eps = 1e-7

        denom = 2 * grads_pow2 + sum_acts * grads_pow3
        denom = torch.where(denom != 0.0, denom, torch.ones_like(denom) * eps)
        alpha = grads_pow2 / denom

        weights = (alpha * F.relu(grads)).sum(dim=(1, 2), keepdim=True)

        cam = (weights * acts).sum(dim=0).cpu().numpy()
        cam = np.maximum(cam, 0)
        if cam.max() > 0:
            cam = cam / cam.max()
        else:
            cam = np.zeros_like(cam)

        return cam, target_class

    def remove_hooks(self):
        for h in self.hook_handles:
            h.remove()

def overlay_heatmap_on_image(original_image_pil, cam, alpha=0.45, colormap=cv2.COLORMAP_JET):
    """
    Overlays normalized CAM heatmap onto the original PIL image.
    Returns RGB PIL Image.
    """
    img_np = np.array(original_image_pil.convert('RGB'))
    h, w, _ = img_np.shape

    cam_resized = cv2.resize(cam, (w, h))
    heatmap = (cam_resized * 255).astype(np.uint8)
    heatmap_colored = cv2.applyColorMap(heatmap, colormap)
    heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)

    blended = (alpha * heatmap_colored + (1.0 - alpha) * img_np).astype(np.uint8)
    return Image.fromarray(blended)
