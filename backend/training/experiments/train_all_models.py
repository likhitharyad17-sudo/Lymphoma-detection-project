import os
import sys
import json
import time
import copy
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from backend.training.data.dataset import LymphomaDataset, get_data_transforms
from backend.training.architectures import (
    AttentionResNet50_CBAM,
    SimpleCNN,
    ResNet50Baseline,
    DenseNet121Baseline,
    EfficientNetB0Baseline,
    ResNet50_NoAttention,
    ResNet50_CAMOnly,
    ResNet50_SAMOnly
)

def train_single_model(model_name, model, train_loader, val_loader, device, epochs=25, lr=3e-4, weight_decay=1e-4):
    print(f"\n=======================================================")
    print(f" Training: {model_name} on {device}")
    print(f"=======================================================")
    
    model = model.to(device)
    criterion = nn.CrossEntropyLoss(label_smoothing=0.05)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=weight_decay)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-6)

    best_val_acc = 0.0
    best_val_loss = float("inf")
    best_weights = copy.deepcopy(model.state_dict())

    history = {
        "train_loss": [], "train_acc": [],
        "val_loss": [], "val_acc": [],
        "learning_rates": []
    }

    start_time = time.time()

    for epoch in range(1, epochs + 1):
        # Training Phase
        model.train()
        train_loss, train_correct, total_train = 0.0, 0, 0

        for batch in train_loader:
            images = batch["image"].to(device)
            labels = batch["label"].to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            train_loss += loss.item() * images.size(0)
            _, preds = torch.max(outputs, 1)
            train_correct += torch.sum(preds == labels.data).item()
            total_train += images.size(0)

        epoch_train_loss = train_loss / total_train
        epoch_train_acc = train_correct / total_train

        # Validation Phase
        model.eval()
        val_loss, val_correct, total_val = 0.0, 0, 0

        with torch.no_grad():
            for batch in val_loader:
                images = batch["image"].to(device)
                labels = batch["label"].to(device)

                outputs = model(images)
                loss = criterion(outputs, labels)

                val_loss += loss.item() * images.size(0)
                _, preds = torch.max(outputs, 1)
                val_correct += torch.sum(preds == labels.data).item()
                total_val += images.size(0)

        epoch_val_loss = val_loss / total_val
        epoch_val_acc = val_correct / total_val
        current_lr = optimizer.param_groups[0]["lr"]

        scheduler.step()

        history["train_loss"].append(epoch_train_loss)
        history["train_acc"].append(epoch_train_acc)
        history["val_loss"].append(epoch_val_loss)
        history["val_acc"].append(epoch_val_acc)
        history["learning_rates"].append(current_lr)

        if epoch_val_acc >= best_val_acc:
            best_val_acc = epoch_val_acc
            best_val_loss = epoch_val_loss
            best_weights = copy.deepcopy(model.state_dict())

        if epoch % 5 == 0 or epoch == epochs:
            print(f"Epoch [{epoch:02d}/{epochs:02d}] "
                  f"Train Loss: {epoch_train_loss:.4f} | Train Acc: {epoch_train_acc*100:.2f}% | "
                  f"Val Loss: {epoch_val_loss:.4f} | Val Acc: {epoch_val_acc*100:.2f}% | LR: {current_lr:.2e}")

    elapsed = time.time() - start_time
    print(f"Finished {model_name} in {elapsed:.1f}s | Best Val Acc: {best_val_acc*100:.2f}%")

    model.load_state_dict(best_weights)
    return model, history, best_val_acc, best_val_loss

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using compute device: {device} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'})")

    base_dir = r"D:\Lymphoma Detection Project"
    splits_dir = os.path.join(base_dir, "dataset", "splits")
    models_dir = os.path.join(base_dir, "models")
    results_dir = os.path.join(base_dir, "results")
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(results_dir, exist_ok=True)

    train_manifest = os.path.join(splits_dir, "train_manifest.json")
    val_manifest = os.path.join(splits_dir, "val_manifest.json")

    train_transform, eval_transform = get_data_transforms(img_size=224)

    train_dataset = LymphomaDataset(train_manifest, transform=train_transform, is_training=True)
    val_dataset = LymphomaDataset(val_manifest, transform=eval_transform, is_training=False)

    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True, num_workers=2, pin_memory=True if torch.cuda.is_available() else False)
    val_loader = DataLoader(val_dataset, batch_size=16, shuffle=False, num_workers=2, pin_memory=True if torch.cuda.is_available() else False)

    print(f"Training samples: {len(train_dataset)} | Validation samples: {len(val_dataset)}")

    models_to_train = {
        # Proposed Primary Model
        "attention_resnet50_cbam": (AttentionResNet50_CBAM(num_classes=3, pretrained=True), 25, 2e-4),
        
        # Baselines
        "resnet50_baseline": (ResNet50Baseline(num_classes=3, pretrained=True), 20, 2e-4),
        "densenet121": (DenseNet121Baseline(num_classes=3, pretrained=True), 20, 2e-4),
        "efficientnet_b0": (EfficientNetB0Baseline(num_classes=3, pretrained=True), 20, 3e-4),
        "simple_cnn": (SimpleCNN(num_classes=3), 25, 5e-4),
        
        # Ablation Variants
        "ablation_resnet50_no_attention": (ResNet50_NoAttention(num_classes=3, pretrained=True), 20, 2e-4),
        "ablation_resnet50_cam_only": (ResNet50_CAMOnly(num_classes=3, pretrained=True), 20, 2e-4),
        "ablation_resnet50_sam_only": (ResNet50_SAMOnly(num_classes=3, pretrained=True), 20, 2e-4),
    }

    all_histories = {}

    for name, (model_obj, epochs, lr) in models_to_train.items():
        trained_model, history, best_val_acc, best_val_loss = train_single_model(
            name, model_obj, train_loader, val_loader, device, epochs=epochs, lr=lr
        )
        # Save model weights
        save_path = os.path.join(models_dir, f"{name}.pth")
        torch.save(trained_model.state_dict(), save_path)
        print(f"Saved checkpoint to: {save_path}")

        # Also save as best_model.pth if it's the proposed model
        if name == "attention_resnet50_cbam":
            torch.save(trained_model.state_dict(), os.path.join(models_dir, "best_model.pth"))

        all_histories[name] = {
            "best_val_acc": float(best_val_acc),
            "best_val_loss": float(best_val_loss),
            "history": history
        }

    with open(os.path.join(results_dir, "training_histories.json"), "w", encoding="utf-8") as f:
        json.dump(all_histories, f, indent=2)

    print("\nAll models successfully trained and checkpoints saved.")

if __name__ == "__main__":
    main()
