import torch
import torch.nn as nn
from torchvision.models import (
    resnet50, ResNet50_Weights,
    densenet121, DenseNet121_Weights,
    efficientnet_b0, EfficientNet_B0_Weights
)

class SimpleCNN(nn.Module):
    """
    Custom Baseline 4-layer Convolutional Neural Network trained from scratch.
    """
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
    """
    Standard ResNet-50 Baseline (without attention modules).
    """
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
    """
    DenseNet-121 Baseline.
    """
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
    """
    EfficientNet-B0 Baseline.
    """
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
