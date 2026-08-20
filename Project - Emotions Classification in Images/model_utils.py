"""
Model utilities for Facial Emotion Classification inference.
Contains the model architecture definitions, checkpoint loading, face detection,
and Captum-based Grad-CAM interpretability routines.
"""
from __future__ import annotations

# Importing the required libraries
from typing import Any, Dict, List, Optional, Tuple, Union
from facenet_pytorch import MTCNN as FaceDetector
from torchvision import models, transforms
from captum.attr import LayerGradCam
import matplotlib.cm as cm
from pathlib import Path
from PIL import Image
import torch.nn as nn
import numpy as np
import base64
import torch
import io

# ============================================================================
# CONSTANTS & CONFIGURATION
# ============================================================================

# Model output classes (alphabetical order as standard in PyTorch ImageFolder)
CLASS_NAMES: List[str] = ['anger', 'happy', 'neutral', 'sad', 'surprise']
NUM_CLASSES: int = len(CLASS_NAMES)

# Normalization statistics
# ImageNet weights used for ResNet transfer learning
IMAGENET_MEAN: List[float] = [0.485, 0.456, 0.406]
IMAGENET_STD: List[float] = [0.229, 0.224, 0.225]

# AffectNet dataset statistics used for custom Baseline CNN
DATASET_MEAN: List[float] = [0.5410, 0.4332, 0.3833]
DATASET_STD: List[float] = [0.2918, 0.2655, 0.2614]

# Emotion emoji mappings for UI representation
EMOTION_EMOJIS: Dict[str, str] = {
    'anger': '😠',
    'happy': '😊',
    'neutral': '😐',
    'sad': '😢',
    'surprise': '😲',
}


# ============================================================================
# DEVICE RESOLUTION
# ============================================================================

def _resolve_device(device: Optional[Union[str, torch.device]] = None) -> torch.device:
    """Helper to resolve a torch device cleanly."""
    if device is None:
        return torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    return torch.device(device) if isinstance(device, str) else device


# ============================================================================
# FACE DETECTION (MTCNN Singleton)
# ============================================================================

_mtcnn_instance: Optional[FaceDetector] = None


def get_face_detector(device: Optional[Union[str, torch.device]] = None) -> FaceDetector:
    """Lazy-initialize and return a singleton MTCNN face detector."""
    global _mtcnn_instance
    if _mtcnn_instance is None:
        target_device = _resolve_device(device)
        _mtcnn_instance = FaceDetector(
            keep_all=False,
            device=target_device,
            select_largest=True,
            post_process=False,
        )
    return _mtcnn_instance


def detect_and_crop_face(
    image: Image.Image,
    device: Optional[Union[str, torch.device]] = None,
    margin_ratio: float = 0.15
) -> Tuple[Image.Image, bool, Optional[List[int]]]:
    """
    Detect and crop the largest face from an image using MTCNN.

    Args:
        image: Input PIL Image.
        device: Torch execution device.
        margin_ratio: Margin to add around the detected bounding box.

    Returns:
        face_crop: Cropped face PIL Image (or original if no face detected).
        face_detected: Boolean flag indicating detection success.
        face_box: [x1, y1, x2, y2] bounding box coordinates.
    """
    if image.mode != 'RGB':
        image = image.convert('RGB')

    detector = get_face_detector(device)
    boxes, _ = detector.detect(image)

    if boxes is not None and len(boxes) > 0:
        box = boxes[0]
        x1, y1, x2, y2 = [int(b) for b in box]

        # Apply boundary margin
        w, h = x2 - x1, y2 - y1
        margin_x = int(w * margin_ratio)
        margin_y = int(h * margin_ratio)

        img_w, img_h = image.size
        x1 = max(0, x1 - margin_x)
        y1 = max(0, y1 - margin_y)
        x2 = min(img_w, x2 + margin_x)
        y2 = min(img_h, y2 + margin_y)

        face_crop = image.crop((x1, y1, x2, y2))
        return face_crop, True, [x1, y1, x2, y2]

    return image, False, None


# ============================================================================
# MODEL ARCHITECTURES
# ============================================================================

class EmotionCNN(nn.Module):
    """
    Custom 4-Block Convolutional Neural Network for Facial Emotion Classification.
    Input: [B, 3, 224, 224] -> Output: [B, num_classes]
    """
    def __init__(self, num_classes: int = NUM_CLASSES):
        super().__init__()

        # Block 1: 3 -> 64 channels, 224x224 -> 112x112
        self.block1 = nn.Sequential(
            nn.Conv2d(3, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Dropout(0.25)
        )

        # Block 2: 64 -> 128 channels, 112x112 -> 56x56
        self.block2 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Dropout(0.25)
        )

        # Block 3: 128 -> 256 channels, 56x56 -> 28x28
        self.block3 = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.Conv2d(256, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Dropout(0.25)
        )

        # Block 4: 256 -> 512 channels, 28x28 -> 14x14
        self.block4 = nn.Sequential(
            nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Dropout(0.25)
        )

        # Classifier Head
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.block1(x)
        x = self.block2(x)
        x = self.block3(x)
        x = self.block4(x)
        x = self.classifier(x)
        return x


def build_resnet18(num_classes: int = NUM_CLASSES) -> nn.Module:
    """Build a ResNet-18 model with a custom classification head."""
    model = models.resnet18(weights=None)
    num_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(0.5),
        nn.Linear(num_features, num_classes)
    )
    return model


# ============================================================================
# TRANSFORMS & MODEL LOADING
# ============================================================================

def get_transform(model_type: str = 'cnn') -> transforms.Compose:
    """
    Get the standardized inference image transformation pipeline.

    Args:
        model_type: 'cnn' uses dataset statistics; 'resnet' uses ImageNet statistics.
    """
    mean, std = (DATASET_MEAN, DATASET_STD) if model_type == 'cnn' else (IMAGENET_MEAN, IMAGENET_STD)

    return transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=mean, std=std)
    ])


def load_model(
    model_path: Union[str, Path],
    model_type: str = 'resnet',
    device: Optional[Union[str, torch.device]] = None
) -> nn.Module:
    """
    Load trained weights into the appropriate model architecture.

    Args:
        model_path: Path to the .pth state dictionary.
        model_type: 'cnn' for EmotionCNN, 'resnet' for ResNet-18.
        device: Torch execution device.

    Returns:
        Evaluated PyTorch model instance.
    """
    target_device = _resolve_device(device)

    if model_type == 'cnn':
        model = EmotionCNN(num_classes=NUM_CLASSES)
    elif model_type == 'resnet':
        model = build_resnet18(num_classes=NUM_CLASSES)
    else:
        raise ValueError(f"Unsupported model_type: '{model_type}'. Choose 'cnn' or 'resnet'.")

    state_dict = torch.load(model_path, map_location=target_device, weights_only=True)
    model.load_state_dict(state_dict)
    model.to(target_device)
    model.eval()
    return model


# ============================================================================
# INFERENCE PIPELINE
# ============================================================================

def predict(
    model: nn.Module,
    image: Image.Image,
    model_type: str = 'resnet',
    device: Optional[Union[str, torch.device]] = None,
    use_face_detection: bool = True
) -> Dict[str, Any]:
    """
    Run full end-to-end emotion inference on an input image.

    Args:
        model: Loaded PyTorch model in eval mode.
        image: Raw PIL Image.
        model_type: 'cnn' or 'resnet'.
        device: Torch execution device.
        use_face_detection: Whether to run MTCNN face localization first.

    Returns:
        Structured prediction dictionary with classes, probabilities, and bbox info.
    """
    target_device = _resolve_device(device)

    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Step 1: Face Localization
    face_detected, face_box = False, None
    if use_face_detection:
        image, face_detected, face_box = detect_and_crop_face(image, target_device)

    # Step 2: Tensor Preprocessing & Batching: (3, 224, 224) -> (1, 3, 224, 224)
    transform = get_transform(model_type)
    tensor = transform(image).unsqueeze(0).to(target_device)

    # Step 3: Forward Pass
    model.eval()
    with torch.no_grad():
        logits = model(tensor)
        probabilities = torch.softmax(logits, dim=1).squeeze(0).cpu().numpy()

    # Step 4: Map probabilities strictly to raw class names
    probs_dict = {
        class_name: round(float(prob), 4)
        for class_name, prob in zip(CLASS_NAMES, probabilities)
    }

    top_class = max(probs_dict, key=lambda k: probs_dict[k])

    return {
        'prediction': top_class,
        'emoji': EMOTION_EMOJIS.get(top_class, ''),
        'confidence': probs_dict[top_class],
        'probabilities': probs_dict,
        'face_detected': face_detected,
        'face_box': face_box,
    }


# ============================================================================
# CAPTUM INTERPRETABILITY (Grad-CAM)
# ============================================================================

def generate_attribution(
    model: nn.Module,
    image: Image.Image,
    model_type: str = 'resnet',
    device: Optional[Union[str, torch.device]] = None
) -> str:
    """
    Generate an interpretable Grad-CAM attribution heatmap encoded as Base64.

    Args:
        model: Loaded PyTorch model.
        image: PIL Image.
        model_type: 'cnn' or 'resnet'.
        device: Torch execution device.

    Returns:
        Base64 Data URI string of the blended saliency map.
    """
    target_device = _resolve_device(device)

    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Detect face region to focus interpretability strictly on facial geometry
    face_image, _, _ = detect_and_crop_face(image, target_device)

    # Select target convolutional feature layer
    if model_type == 'cnn':
        target_layer = model.block4[3]       # Last Conv2d in custom block 4
    else:
        target_layer = model.layer4[-1].conv2  # Last Conv2d in ResNet-18 residual layer 4

    transform = get_transform(model_type)
    input_tensor = transform(face_image).unsqueeze(0).to(target_device)

    # Get target class for attribution
    model.eval()
    with torch.no_grad():
        output = model(input_tensor)
    pred_class_idx = int(output.argmax(dim=1).item())

    # Compute LayerGradCam
    grad_cam = LayerGradCam(model, target_layer)
    attribution = grad_cam.attribute(input_tensor, target=pred_class_idx)

    # Squeeze to 2D activation map & apply ReLU normalization
    attr = attribution.squeeze().cpu().detach().numpy()
    if attr.ndim > 2:
        attr = attr.mean(axis=0)
    attr = np.maximum(attr, 0)
    if attr.max() > 0:
        attr = attr / attr.max()

    # Resize heatmap to match cropped face dimensions
    attr_pil = Image.fromarray((attr * 255).astype(np.uint8))
    attr_resized = np.array(
        attr_pil.resize(face_image.size, resample=Image.Resampling.BILINEAR)
    ) / 255.0

    # Apply Jet color mapping
    heatmap_colored = (cm.jet(attr_resized)[:, :, :3] * 255).astype(np.uint8)

    # Alpha-blend (55% original facial features, 45% heatmap attribution)
    original_arr = np.array(face_image)
    blended = (0.55 * original_arr + 0.45 * heatmap_colored).astype(np.uint8)

    # Encode as Base64 Data URI
    blended_pil = Image.fromarray(blended)
    buffer = io.BytesIO()
    blended_pil.save(buffer, format='PNG')
    buffer.seek(0)
    b64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return f"data:image/png;base64,{b64_str}"