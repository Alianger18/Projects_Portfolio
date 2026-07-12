"""
Model utilities for Emotion Classification inference.
Contains the model architecture definition, loading, and prediction logic.
"""
import io
import base64

import torch
import torch.nn as nn
import numpy as np
import matplotlib.cm as cm
from torchvision import transforms, models
from PIL import Image
from pathlib import Path
from facenet_pytorch import MTCNN as FaceDetector
from captum.attr import LayerGradCam

# ============================================================================
# CONSTANTS
# ============================================================================
# Internal model output classes — must match the trained 7-class model
_MODEL_CLASSES = ['angry', 'disgust', 'fear', 'happy', 'neutral', 'sad', 'surprise']
_NUM_MODEL_OUTPUTS = len(_MODEL_CLASSES)

# Mapping: internal model class → public display name (only kept classes)
_CLASS_RENAME = {
    'angry':    'anger',
    'happy':    'joy',
    'neutral':  'neutral',
    'surprise': 'surprise',
}

# Public-facing class names (4 classes)
CLASS_NAMES = ['anger', 'joy', 'neutral', 'surprise']
NUM_CLASSES = len(CLASS_NAMES)

# Approximate per-channel statistics for the MMA Facial Expression dataset.
# These are close approximations for 48×48 RGB face images.
# For the best accuracy, replace with the exact values computed in the notebook.
CHANNEL_MEAN = [0.5066, 0.4565, 0.4291]
CHANNEL_STD  = [0.2586, 0.2428, 0.2398]

# Emoji mapping for display
EMOTION_EMOJIS = {
    'anger':    '😠',
    'joy':      '😊',
    'neutral':  '😐',
    'surprise': '😲',
}


# ============================================================================
# FACE DETECTION — MTCNN singleton
# ============================================================================
_mtcnn = None


def get_face_detector(device=None):
    """Lazy-initialize and return the MTCNN face detector."""
    global _mtcnn
    if _mtcnn is None:
        if device is None:
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        _mtcnn = FaceDetector(
            keep_all=False,
            device=device,
            select_largest=True,
            post_process=False,
        )
    return _mtcnn


def detect_and_crop_face(image, device=None):
    """
    Detect and crop the largest face from an image using MTCNN.

    Args:
        image: PIL Image (any mode).
        device: Torch device.

    Returns:
        face_crop (PIL.Image): Cropped face, or original image if none found.
        face_detected (bool): Whether a face was successfully detected.
        face_box (list or None): [x1, y1, x2, y2] bounding box coordinates.
    """
    if image.mode != 'RGB':
        image = image.convert('RGB')

    detector = get_face_detector(device)
    boxes, probs = detector.detect(image)

    if boxes is not None and len(boxes) > 0:
        box = boxes[0]
        x1, y1, x2, y2 = [int(b) for b in box]

        # Add 15% margin around the detected face
        w, h = x2 - x1, y2 - y1
        margin_x = int(w * 0.15)
        margin_y = int(h * 0.15)

        img_w, img_h = image.size
        x1 = max(0, x1 - margin_x)
        y1 = max(0, y1 - margin_y)
        x2 = min(img_w, x2 + margin_x)
        y2 = min(img_h, y2 + margin_y)

        face_crop = image.crop((x1, y1, x2, y2))
        return face_crop, True, [x1, y1, x2, y2]
    else:
        return image, False, None


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
        model = EmotionCNN(_NUM_MODEL_OUTPUTS)
    elif model_type == 'resnet':
        model = build_resnet18(_NUM_MODEL_OUTPUTS)
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
            device: torch.device = None, use_face_detection: bool = True):
    """
    Run inference on a single PIL Image.

    Optionally detects and crops the face via MTCNN before classifying.

    Args:
        model: The loaded PyTorch model (in eval mode).
        image: A PIL Image (any size/mode — will be converted to RGB).
        model_type: 'cnn' or 'resnet' — determines the transform pipeline.
        device: Torch device.
        use_face_detection: If True, run MTCNN face detection first.

    Returns:
        dict with prediction, confidence, probabilities, and face metadata.
    """
    if device is None:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Ensure RGB
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Face detection & alignment (MTCNN)
    face_detected, face_box = False, None
    if use_face_detection:
        image, face_detected, face_box = detect_and_crop_face(image, device)

    # Transform and add batch dimension
    transform = get_transform(model_type)
    tensor = transform(image).unsqueeze(0).to(device)

    # Inference
    with torch.no_grad():
        outputs = model(tensor)
        probabilities = torch.softmax(outputs, dim=1)[0]

    # Build result — filter to 4 kept classes and re-normalize
    kept_raw = {}
    for i, model_cls in enumerate(_MODEL_CLASSES):
        if model_cls in _CLASS_RENAME:
            kept_raw[_CLASS_RENAME[model_cls]] = float(probabilities[i])

    total = sum(kept_raw.values())
    probs_dict = {
        cls: round(kept_raw[cls] / total, 4) if total > 0 else 0.0
        for cls in CLASS_NAMES
    }

    top_class = max(probs_dict, key=probs_dict.get)
    top_conf = probs_dict[top_class]

    return {
        'prediction': top_class,
        'confidence': round(top_conf, 4),
        'probabilities': probs_dict,
        'face_detected': face_detected,
        'face_box': [int(c) for c in face_box] if face_box else None,
    }


# ============================================================================
# CAPTUM INTERPRETABILITY — GradCAM Attribution
# ============================================================================
def generate_attribution(model, image: Image.Image, model_type: str = 'cnn',
                         device: torch.device = None):
    """
    Generate a GradCAM attribution heatmap for the predicted class.

    The image is first face-cropped via MTCNN, then the attribution is
    computed against the last convolutional layer and blended with the
    original face crop.

    Args:
        model: Loaded PyTorch model in eval mode.
        image: PIL Image (will be face-cropped automatically).
        model_type: 'cnn' or 'resnet'.
        device: Torch device.

    Returns:
        heatmap_b64 (str): data:image/png;base64,... encoded overlay.
    """
    if device is None:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Detect and crop face first
    face_image, _, _ = detect_and_crop_face(image, device)

    # Select the target convolutional layer for GradCAM
    if model_type == 'cnn':
        target_layer = model.block3[3]   # Last Conv2d in block3
    else:
        target_layer = model.layer4[-1].conv2  # Standard ResNet target

    # Prepare input tensor
    transform = get_transform(model_type)
    input_tensor = transform(face_image).unsqueeze(0).to(device)

    # Get predicted class index
    model.eval()
    with torch.no_grad():
        output = model(input_tensor)
    pred_class = int(output.argmax(dim=1))

    # Run LayerGradCam
    grad_cam = LayerGradCam(model, target_layer)
    attribution = grad_cam.attribute(input_tensor, target=pred_class)

    # Process: squeeze, average channels, ReLU, normalize to [0, 1]
    attr = attribution.squeeze().cpu().detach().numpy()
    if attr.ndim > 2:
        attr = attr.mean(axis=0)
    attr = np.maximum(attr, 0)                       # ReLU
    if attr.max() > 0:
        attr = attr / attr.max()                     # normalize

    # Resize heatmap to match face image dimensions
    attr_pil = Image.fromarray((attr * 255).astype(np.uint8))
    attr_resized = np.array(
        attr_pil.resize(face_image.size, Image.BILINEAR)
    ) / 255.0

    # Apply jet colormap
    heatmap_colored = cm.jet(attr_resized)[:, :, :3]        # drop alpha
    heatmap_colored = (heatmap_colored * 255).astype(np.uint8)

    # Blend heatmap with original face image (55% original, 45% heatmap)
    original_arr = np.array(face_image)
    blended = (0.55 * original_arr + 0.45 * heatmap_colored).astype(np.uint8)

    # Encode as base64 PNG
    blended_img = Image.fromarray(blended)
    buffer = io.BytesIO()
    blended_img.save(buffer, format='PNG')
    buffer.seek(0)
    b64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return f'data:image/png;base64,{b64_str}'
