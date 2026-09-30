import torch
import torch.nn as nn
from torchvision.models import resnet50, ResNet50_Weights
from .cbam_modules import CBAMBlock

class AttentionResNet50_CBAM(nn.Module):
    """
    Proposed Attention-Augmented Residual Network for Malignant Lymphoma Classification.
    Integrates CBAM (Channel + Spatial Attention) after Stage 3 (layer3) and Stage 4 (layer4) residual blocks.
    Features dual Global Average Pooling (GAP) + Global Max Pooling (GMP) and regularized classification head.
    """
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
