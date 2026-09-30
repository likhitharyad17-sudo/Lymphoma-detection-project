import torch
import torch.nn as nn
from torchvision.models import resnet50, ResNet50_Weights
from .cbam_modules import ChannelAttention, SpatialAttention, CBAMBlock

class ResNet50_NoAttention(nn.Module):
    """Experiment A: ResNet-50 Baseline without attention."""
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
    """Experiment B: ResNet-50 + Channel Attention Only."""
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
    """Experiment C: ResNet-50 + Spatial Attention Only."""
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
