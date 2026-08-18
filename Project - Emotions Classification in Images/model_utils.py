"""
Model utilities for Emotion Classification inference.
Contains the model architecture definition, loading, and prediction logic.
"""
from facenet_pytorch import MTCNN as FaceDetector
from torchvision import transforms, models
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
# CONSTANTS
# ============================================================================
# Internal model output classes
_INTERNAL_CLASSES = ['anger', 'happy', 'neutral', 'sad', 'surprise']

# Public-facing class names (5 classes)
CLASS_NAMES = ['anger', 'joy', 'neutral', 'sad', 'surprise']
NUM_CLASSES = len(CLASS_NAMES)

# Mapping from internal to display names
_INTERNAL_TO_DISPLAY = {
    'anger': 'anger',
    'happy': 'joy',
    'neutral': 'neutral',
    'sad': 'sad',
    'surprise': 'surprise',
}

# Normalization statistics
# ImageNet hardcoded weights used for ResNet-18 transfer learning
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD  = [0.229, 0.224, 0.225]

# Computed AffectNet dataset statistics used for Baseline CNN
DATASET_MEAN  = [0.5410, 0.4332, 0.3833]
DATASET_STD   = [0.2918, 0.2655, 0.2614]

CHANNEL_MEAN  = IMAGENET_MEAN
CHANNEL_STD   = IMAGENET_STD

# Emoji mapping for display
EMOTION_EMOJIS = {
    'anger':    '😠',
    'joy':      '😊',
    'neutral':  '😐',
    'sad':      '😢',
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
    Custom CNN for 224x224 facial emotion classification.
    Architecture: 4 conv blocks + AdaptiveAvgPool2d + FC layers → 4 classes.
    """
    def __init__(self, num_classes=4):
        super(EmotionCNN, self).__init__()

        # Block 1: 3 → 64 channels, 224×224 → 112×112
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

        # Block 2: 64 → 128 channels, 112×112 → 56×56
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

        # Block 3: 128 → 256 channels, 56×56 → 28×28
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

        # Block 4: 256 → 512 channels, 28×28 → 14×14
        self.block4 = nn.Sequential(
            nn.Conv2d(256, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.Conv2d(512, 512, kernel_size=3, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            nn.Dropout(0.25)
        )

        # Classifier head
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten(),
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        x = self.block1(x)
        x = self.block2(x)
        x = self.block3(x)
        x = self.block4(x)
        x = self.classifier(x)
        return x


# ============================================================================
# RESNET-18 BUILDER
# ============================================================================
def build_resnet18(num_classes=4):
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
    Get the inference transform pipeline matching the training transforms.
    Baseline CNN uses dataset-computed statistics; ResNet-18 uses ImageNet statistics.
    """
    if model_type == 'cnn':
        mean, std = DATASET_MEAN, DATASET_STD
    else:
        mean, std = IMAGENET_MEAN, IMAGENET_STD

    return transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=mean, std=std)
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

    # Map output probabilities to display classes
    probs_dict = {}
    for i, int_cls in enumerate(_INTERNAL_CLASSES):
        disp_name = _INTERNAL_TO_DISPLAY[int_cls]
        probs_dict[disp_name] = round(float(probabilities[i]), 4)

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
        target_layer = model.block4[3]   # Last Conv2d in block4
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
