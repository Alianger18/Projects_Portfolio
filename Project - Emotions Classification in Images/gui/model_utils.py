"""
Model utilities for Emotion Classification inference.
Contains the model architecture definition, loading, and prediction logic.
"""
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import numpy as np
from pathlib import Path

# ============================================================================
# CONSTANTS
# ============================================================================
CLASS_NAMES = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
NUM_CLASSES = len(CLASS_NAMES)

# Approximate per-channel statistics for the MMA Facial Expression dataset.
# These are close approximations for 48×48 RGB face images.
# For best accuracy, replace with the exact values computed in the notebook.
CHANNEL_MEAN = [0.5066, 0.4565, 0.4291]
CHANNEL_STD  = [0.2586, 0.2428, 0.2398]

# Emoji mapping for display
EMOTION_EMOJIS = {
    'angry':    '😠',
    'disgust':  '🤢',
    'fear':     '😨',
    'happy':    '😊',
    'neutral':  '😐',
    'sad':      '😢',
    'surprise': '😲',
}


# ============================================================================
# MODEL ARCHITECTURE — must match the notebook definition exactly
# ============================================================================
class EmotionCNN(nn.Module):
    """
    Custom CNN for 48×48 facial emotion classification.
    Architecture: 3 conv blocks + 2 FC layers → 7 classes.
    """
    def __init__(self, num_classes=7):
        super(EmotionCNN, self).__init__()

        # Block 1: 3 → 64 channels, 48×48 → 24×24
        self.block1 = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Dropout(0.25)
        )

        # Block 2: 64 → 128 channels, 24×24 → 12×12
        self.block2 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Dropout(0.25)
        )

        # Block 3: 128 → 256 channels, 12×12 → 6×6
        self.block3 = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Dropout(0.25)
        )

        # Classifier head
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256 * 6 * 6, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )

    def forward(self, x):
        x = self.block1(x)
        x = self.block2(x)
        x = self.block3(x)
        x = self.classifier(x)
        return x


# ============================================================================
# RESNET-18 BUILDER
# ============================================================================
def build_resnet18(num_classes=7):
    """Build a ResNet-18 model with the same architecture as the notebook."""
    model = models.resnet18(weights=None)
    num_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(0.5),
        nn.Linear(num_features, num_classes)
    )
    return model


# ============================================================================
# INFERENCE TRANSFORMS
# ============================================================================
def get_transform(model_type='cnn'):
    """
    Get the inference transform pipeline matching the training transforms
    (without augmentation).
    """
    img_size = 48 if model_type == 'cnn' else 224
    return transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=CHANNEL_MEAN, std=CHANNEL_STD)
    ])


# ============================================================================
# MODEL LOADING
# ============================================================================
def load_model(model_path: Path, model_type: str = 'cnn', device: torch.device = None):
    """
    Load a trained model from a checkpoint file.

    Args:
        model_path: Path to the .pth weights file.
        model_type: 'cnn' for EmotionCNN, 'resnet' for ResNet-18.
        device: Torch device to load the model onto.

    Returns:
        The model in eval mode on the specified device.
    """
    if device is None:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    if model_type == 'cnn':
        model = EmotionCNN(NUM_CLASSES)
    elif model_type == 'resnet':
        model = build_resnet18(NUM_CLASSES)
    else:
        raise ValueError(f"Unknown model_type: {model_type}. Use 'cnn' or 'resnet'.")

    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    return model


# ============================================================================
# PREDICTION
# ============================================================================
def predict(model, image: Image.Image, model_type: str = 'cnn',
            device: torch.device = None):
    """
    Run inference on a single PIL Image.

    Args:
        model: The loaded PyTorch model (in eval mode).
        image: A PIL Image (any size/mode — will be converted to RGB).
        model_type: 'cnn' or 'resnet' — determines the transform pipeline.
        device: Torch device.

    Returns:
        dict with keys:
            - prediction (str): Top predicted emotion.
            - confidence (float): Confidence of the top prediction.
            - probabilities (dict): {emotion: probability} for all 7 classes.
    """
    if device is None:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Ensure RGB
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Transform and add batch dimension
    transform = get_transform(model_type)
    tensor = transform(image).unsqueeze(0).to(device)

    # Inference
    with torch.no_grad():
        outputs = model(tensor)
        probabilities = torch.softmax(outputs, dim=1)[0]

    # Build result
    probs_dict = {
        cls: round(float(probabilities[i]), 4)
        for i, cls in enumerate(CLASS_NAMES)
    }

    top_idx = int(torch.argmax(probabilities))
    top_class = CLASS_NAMES[top_idx]
    top_conf = float(probabilities[top_idx])

    return {
        'prediction': top_class,
        'confidence': round(top_conf, 4),
        'probabilities': probs_dict,
    }
