import os
import json
import torch
from torch.utils.data import Dataset
from PIL import Image
import torchvision.transforms as T

class LymphomaDataset(Dataset):
    """
    PyTorch Dataset for Malignant Lymphoma Histopathological Classification.
    Supports 3 classes: CLL, FL, MCL.
    Loads image paths from stratified manifest JSON files.
    """
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
    """
    Returns training and validation/testing data transforms with stain-aware augmentations.
    """
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

def get_eval_transforms(image_size=224):
    """Returns the evaluation/inference transform."""
    return T.Compose([
        T.Resize((image_size, image_size)),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

