import os

project_root = r"D:\Lymphoma Detection Project"

files = {}

# 1. Dataset Class
files["backend/training/data/__init__.py"] = """from .dataset import LymphomaDataset, get_data_transforms
"""

files["backend/training/data/dataset.py"] = """import os
import json
import torch
from torch.utils.data import Dataset
from PIL import Image
import torchvision.transforms as T

class LymphomaDataset(Dataset):
    \"\"\"
    PyTorch Dataset for Malignant Lymphoma Histopathological Classification.
    Supports 3 classes: CLL, FL, MCL.
    Loads image paths from stratified manifest JSON files.
    \"\"\"
    def __init__(self, manifest_path, transform=None, is_training=False):
        with open(manifest_path, 'r', encoding='utf-8') as f:
            self.samples = json.load(f)
        self.transform = transform
        self.is_training = is_training

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        item = self.samples[idx]
        image_path = item['file_path']
        class_idx = item['class_idx']
        class_name = item['class_name']

        try:
            image = Image.open(image_path).convert('RGB')
        except Exception as e:
            raise RuntimeError(f"Error loading image {image_path}: {e}")

        if self.transform is not None:
            image = self.transform(image)

        return {
            'image': image,
            'label': torch.tensor(class_idx, dtype=torch.long),
            'class_name': class_name,
            'file_name': item['file_name'],
            'file_path': image_path
        }

def get_data_transforms(img_size=224):
    \"\"\"
    Returns training and validation/testing data transforms with stain-aware augmentations.
    \"\"\"
    train_transform = T.Compose([
        T.Resize((img_size, img_size)),
        T.RandomHorizontalFlip(p=0.5),
        T.RandomVerticalFlip(p=0.5),
        T.RandomRotation(degrees=90),
        T.ColorJitter(brightness=0.15, contrast=0.15, saturation=0.15, hue=0.05),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    eval_transform = T.Compose([
        T.Resize((img_size, img_size)),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    return train_transform, eval_transform
"""

# 2. CBAM Modules
files["backend/training/architectures/cbam_modules.py"] = """import torch
import torch.nn as nn

class ChannelAttention(nn.Module):
    \"\"\"
    Channel Attention Module (CAM) of CBAM.
    Aggregates spatial information via Global Average Pooling (GAP) and Global Max Pooling (GMP).
    Squeezes through a shared Multi-Layer Perceptron (MLP) with reduction ratio r.
    \"\"\"
    def __init__(self, in_planes, ratio=16):
        super(ChannelAttention, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)

        reduced_planes = max(in_planes // ratio, 8)
        self.fc1 = nn.Conv2d(in_planes, reduced_planes, 1, bias=False)
        self.relu1 = nn.ReLU(inplace=True)
        self.fc2 = nn.Conv2d(reduced_planes, in_planes, 1, bias=False)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        avg_out = self.fc2(self.relu1(self.fc1(self.avg_pool(x))))
        max_out = self.fc2(self.relu1(self.fc1(self.max_pool(x))))
        out = avg_out + max_out
        return self.sigmoid(out)

class SpatialAttention(nn.Module):
    \"\"\"
    Spatial Attention Module (SAM) of CBAM.
    Aggregates channel information using average and max pooling along the channel axis.
    Applies a 7x7 standard convolution followed by sigmoid activation to highlight key cellular regions.
    \"\"\"
    def __init__(self, kernel_size=7):
        super(SpatialAttention, self).__init__()
        assert kernel_size in (3, 7), "kernel size must be 3 or 7"
        padding = 3 if kernel_size == 7 else 1

        self.conv1 = nn.Conv2d(2, 1, kernel_size, padding=padding, bias=False)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        avg_out = torch.mean(x, dim=1, keepdim=True)
        max_out, _ = torch.max(x, dim=1, keepdim=True)
        x_cat = torch.cat([avg_out, max_out], dim=1)
        out = self.conv1(x_cat)
        return self.sigmoid(out)

class CBAMBlock(nn.Module):
    \"\"\"
    Convolutional Block Attention Module (CBAM).
    Sequentially applies Channel Attention and Spatial Attention to refine intermediate feature maps.
    \"\"\"
    def __init__(self, in_planes, ratio=16, kernel_size=7):
        super(CBAMBlock, self).__init__()
        self.ca = ChannelAttention(in_planes, ratio)
        self.sa = SpatialAttention(kernel_size)

    def forward(self, x):
        out = x * self.ca(x)
        out = out * self.sa(out)
        return out
"""

# 3. Proposed Attention-Augmented ResNet Architecture
files["backend/training/architectures/attention_residual_net.py"] = """import torch
import torch.nn as nn
from torchvision.models import resnet50, ResNet50_Weights
from .cbam_modules import CBAMBlock

class AttentionResNet50_CBAM(nn.Module):
    \"\"\"
    Proposed Attention-Augmented Residual Network for Malignant Lymphoma Classification.
    Integrates CBAM (Channel + Spatial Attention) after Stage 3 (layer3) and Stage 4 (layer4) residual blocks.
    Features dual Global Average Pooling (GAP) + Global Max Pooling (GMP) and regularized classification head.
    \"\"\"
    def __init__(self, num_classes=3, pretrained=True, dropout=0.4):
        super(AttentionResNet50_CBAM, self).__init__()
        weights = ResNet50_Weights.DEFAULT if pretrained else None
        base_model = resnet50(weights=weights)

        self.conv1 = base_model.conv1
        self.bn1 = base_model.bn1
        self.relu = base_model.relu
        self.maxpool = base_model.maxpool

        self.layer1 = base_model.layer1
        self.layer2 = base_model.layer2
        self.layer3 = base_model.layer3
        self.cbam3 = CBAMBlock(1024, ratio=16)

        self.layer4 = base_model.layer4
        self.cbam4 = CBAMBlock(2048, ratio=16)

        self.gap = nn.AdaptiveAvgPool2d((1, 1))
        self.gmp = nn.AdaptiveMaxPool2d((1, 1))

        # 2048 (GAP) + 2048 (GMP) = 4096 dimensions
        self.classifier = nn.Sequential(
            nn.Linear(2048 * 2, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(inplace=True),
            nn.Dropout(p=dropout),
            nn.Linear(512, num_classes)
        )

    def forward_features(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.cbam3(x)

        x = self.layer4(x)
        x = self.cbam4(x)
        return x

    def forward(self, x):
        features = self.forward_features(x)
        gap_feat = self.gap(features).flatten(1)
        gmp_feat = self.gmp(features).flatten(1)
        pooled = torch.cat([gap_feat, gmp_feat], dim=1)
        logits = self.classifier(pooled)
        return logits
"""

# 4. Baselines
files["backend/training/architectures/baselines.py"] = """import torch
import torch.nn as nn
from torchvision.models import (
    resnet50, ResNet50_Weights,
    densenet121, DenseNet121_Weights,
    efficientnet_b0, EfficientNet_B0_Weights
)

class SimpleCNN(nn.Module):
    \"\"\"
    Custom Baseline 4-layer Convolutional Neural Network trained from scratch.
    \"\"\"
    def __init__(self, num_classes=3):
        super(SimpleCNN, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),

            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((1, 1))
        )
        self.classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(inplace=True),
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        feat = self.features(x).flatten(1)
        return self.classifier(feat)

class ResNet50Baseline(nn.Module):
    \"\"\"
    Standard ResNet-50 Baseline (without attention modules).
    \"\"\"
    def __init__(self, num_classes=3, pretrained=True, dropout=0.4):
        super(ResNet50Baseline, self).__init__()
        weights = ResNet50_Weights.DEFAULT if pretrained else None
        self.model = resnet50(weights=weights)
        in_features = self.model.fc.in_features
        self.model.fc = nn.Sequential(
            nn.Dropout(p=dropout),
            nn.Linear(in_features, num_classes)
        )

    def forward(self, x):
        return self.model(x)

class DenseNet121Baseline(nn.Module):
    \"\"\"
    DenseNet-121 Baseline.
    \"\"\"
    def __init__(self, num_classes=3, pretrained=True, dropout=0.4):
        super(DenseNet121Baseline, self).__init__()
        weights = DenseNet121_Weights.DEFAULT if pretrained else None
        self.model = densenet121(weights=weights)
        in_features = self.model.classifier.in_features
        self.model.classifier = nn.Sequential(
            nn.Dropout(p=dropout),
            nn.Linear(in_features, num_classes)
        )

    def forward(self, x):
        return self.model(x)

class EfficientNetB0Baseline(nn.Module):
    \"\"\"
    EfficientNet-B0 Baseline.
    \"\"\"
    def __init__(self, num_classes=3, pretrained=True, dropout=0.4):
        super(EfficientNetB0Baseline, self).__init__()
        weights = EfficientNet_B0_Weights.DEFAULT if pretrained else None
        self.model = efficientnet_b0(weights=weights)
        in_features = self.model.classifier[1].in_features
        self.model.classifier = nn.Sequential(
            nn.Dropout(p=dropout),
            nn.Linear(in_features, num_classes)
        )

    def forward(self, x):
        return self.model(x)
"""

# 5. Ablation Models
files["backend/training/architectures/ablation_models.py"] = """import torch
import torch.nn as nn
from torchvision.models import resnet50, ResNet50_Weights
from .cbam_modules import ChannelAttention, SpatialAttention, CBAMBlock

class ResNet50_NoAttention(nn.Module):
    \"\"\"Experiment A: ResNet-50 Baseline without attention.\"\"\"
    def __init__(self, num_classes=3, pretrained=True, dropout=0.4):
        super(ResNet50_NoAttention, self).__init__()
        weights = ResNet50_Weights.DEFAULT if pretrained else None
        base = resnet50(weights=weights)
        self.backbone = nn.Sequential(
            base.conv1, base.bn1, base.relu, base.maxpool,
            base.layer1, base.layer2, base.layer3, base.layer4
        )
        self.gap = nn.AdaptiveAvgPool2d((1, 1))
        self.gmp = nn.AdaptiveMaxPool2d((1, 1))
        self.classifier = nn.Sequential(
            nn.Linear(2048 * 2, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(inplace=True),
            nn.Dropout(p=dropout),
            nn.Linear(512, num_classes)
        )

    def forward(self, x):
        f = self.backbone(x)
        pooled = torch.cat([self.gap(f).flatten(1), self.gmp(f).flatten(1)], dim=1)
        return self.classifier(pooled)

class ResNet50_CAMOnly(nn.Module):
    \"\"\"Experiment B: ResNet-50 + Channel Attention Only.\"\"\"
    def __init__(self, num_classes=3, pretrained=True, dropout=0.4):
        super(ResNet50_CAMOnly, self).__init__()
        weights = ResNet50_Weights.DEFAULT if pretrained else None
        base = resnet50(weights=weights)
        self.conv1 = base.conv1
        self.bn1 = base.bn1
        self.relu = base.relu
        self.maxpool = base.maxpool
        self.layer1 = base.layer1
        self.layer2 = base.layer2
        self.layer3 = base.layer3
        self.ca3 = ChannelAttention(1024, ratio=16)
        self.layer4 = base.layer4
        self.ca4 = ChannelAttention(2048, ratio=16)
        self.gap = nn.AdaptiveAvgPool2d((1, 1))
        self.gmp = nn.AdaptiveMaxPool2d((1, 1))
        self.classifier = nn.Sequential(
            nn.Linear(2048 * 2, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(inplace=True),
            nn.Dropout(p=dropout),
            nn.Linear(512, num_classes)
        )

    def forward(self, x):
        x = self.maxpool(self.relu(self.bn1(self.conv1(x))))
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = x * self.ca3(x)
        x = self.layer4(x)
        x = x * self.ca4(x)
        pooled = torch.cat([self.gap(x).flatten(1), self.gmp(x).flatten(1)], dim=1)
        return self.classifier(pooled)

class ResNet50_SAMOnly(nn.Module):
    \"\"\"Experiment C: ResNet-50 + Spatial Attention Only.\"\"\"
    def __init__(self, num_classes=3, pretrained=True, dropout=0.4):
        super(ResNet50_SAMOnly, self).__init__()
        weights = ResNet50_Weights.DEFAULT if pretrained else None
        base = resnet50(weights=weights)
        self.conv1 = base.conv1
        self.bn1 = base.bn1
        self.relu = base.relu
        self.maxpool = base.maxpool
        self.layer1 = base.layer1
        self.layer2 = base.layer2
        self.layer3 = base.layer3
        self.sa3 = SpatialAttention(7)
        self.layer4 = base.layer4
        self.sa4 = SpatialAttention(7)
        self.gap = nn.AdaptiveAvgPool2d((1, 1))
        self.gmp = nn.AdaptiveMaxPool2d((1, 1))
        self.classifier = nn.Sequential(
            nn.Linear(2048 * 2, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(inplace=True),
            nn.Dropout(p=dropout),
            nn.Linear(512, num_classes)
        )

    def forward(self, x):
        x = self.maxpool(self.relu(self.bn1(self.conv1(x))))
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = x * self.sa3(x)
        x = self.layer4(x)
        x = x * self.sa4(x)
        pooled = torch.cat([self.gap(x).flatten(1), self.gmp(x).flatten(1)], dim=1)
        return self.classifier(pooled)
"""

files["backend/training/architectures/__init__.py"] = """from .cbam_modules import ChannelAttention, SpatialAttention, CBAMBlock
from .attention_residual_net import AttentionResNet50_CBAM
from .baselines import SimpleCNN, ResNet50Baseline, DenseNet121Baseline, EfficientNetB0Baseline
from .ablation_models import ResNet50_NoAttention, ResNet50_CAMOnly, ResNet50_SAMOnly
"""

# 6. Grad-CAM++ Explainability Module
files["backend/training/explainability/__init__.py"] = """from .gradcam import GradCAMPlusPlus, overlay_heatmap_on_image
"""

files["backend/training/explainability/gradcam.py"] = """import torch
import torch.nn.functional as F
import numpy as np
import cv2
from PIL import Image

class GradCAMPlusPlus:
    \"\"\"
    Grad-CAM++ (Generalized Gradient-weighted Class Activation Mapping).
    Computes higher-order pixel-level gradient weights to capture multiple instances
    and finer morphological structures in histopathological imagery.
    \"\"\"
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
    \"\"\"
    Overlays normalized CAM heatmap onto the original PIL image.
    Returns RGB PIL Image.
    \"\"\"
    img_np = np.array(original_image_pil.convert('RGB'))
    h, w, _ = img_np.shape

    cam_resized = cv2.resize(cam, (w, h))
    heatmap = (cam_resized * 255).astype(np.uint8)
    heatmap_colored = cv2.applyColorMap(heatmap, colormap)
    heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)

    blended = (alpha * heatmap_colored + (1.0 - alpha) * img_np).astype(np.uint8)
    return Image.fromarray(blended)
"""

for rel_path, content in files.items():
    full_path = os.path.join(project_root, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {rel_path}")

print("Successfully created all ML & architecture modules.")
