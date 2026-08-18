# 🎭 Facial Emotion Classifier with MTCNN & Captum

A deep learning application that classifies facial expressions into **five emotion categories**: **Anger 😠, Joy 😊, Neutral 😐, Sad 😢, and Surprise 😲**.

The project features a **FastAPI** backend running inference on a **ResNet-18** model (transfer-learned on AffectNet), combined with **MTCNN** face detection and an interactive web GUI displaying real-time confidence scores and **GradCAM interpretability heatmaps** via **Captum**.

---

## 🖼️ Screenshots

<p align="center">
  <img src="assets/figures/Fig. 10 - Entry section.png" alt="Upload Page" width="3840" />
</p>
<p align="center"><em>Upload Page — Drag & drop or click to upload a facial image</em></p>

<p align="center">
  <img src="assets/figures/Fig. 11 - Inference section.png" alt="Prediction Results" width="3840" />
</p>
<p align="center"><em>Prediction Results — Per-class confidence bars with the top prediction highlighted</em></p>

<p align="center">
  <img src="assets/figures/Fig. 12 - Interpretability section.png" alt="GradCAM Interpretability" width="3840" />
</p>
<p align="center"><em>GradCAM Interpretability — Heatmap showing which facial regions drove the prediction</em></p>

---

## 📊 About the Dataset

This project uses the **AffectNet** dataset (available on [Kaggle](https://www.kaggle.com/datasets/mstjebashazida/affectnet)), a large-scale facial expression dataset containing in-the-wild facial images.

| Property | Detail |
|---|---|
| **Target Classes** | 5 emotions: `anger`, `happy` (joy), `neutral`, `sad`, `surprise` |
| **Native Resolution** | 96×96 px RGB images |
| **Directory Structure** | `Train/` and `Test/` with folder-based emotion labels |
| **Train/Val Split** | 80/20 stratified split from `Train/` |

**Preprocessing & Augmentation Pipeline**:
- **Training**: `Resize(256)` → `RandomCrop(224)` → `RandomHorizontalFlip` → `RandomRotation(10°)` → `ColorJitter` → `ImageNet Normalization`
- **Validation & Test**: `Resize(256)` → `CenterCrop(224)` → `ImageNet Normalization` (`mean=[0.485, 0.456, 0.406]`, `std=[0.229, 0.224, 0.225]`)

---

## ✨ Key Features

1. **MTCNN Face Detection & Alignment**
   - Automatically detects, aligns, and crops the largest face from any uploaded image with a 15% margin.
   - Falls back to the original image if no face is found.

2. **ResNet-18 Transfer Learning**
   - Fine-tuned ResNet-18 with a custom dropout + linear classification head for 5-class emotion prediction.
   - Trained on the AffectNet dataset with ImageNet-pretrained weights.

3. **Model Interpretability (Captum LayerGradCam)**
   - Computes spatial feature attributions on the last convolutional layer (`layer4[-1].conv2`).
   - Overlays a jet-colored attribution heatmap on the cropped face to show which regions (e.g., mouth, eyes, brow furrow) drove the prediction.

4. **Modern Glassmorphic Web GUI**
   - Side-by-side layout: image preview on the left, predictions on the right.
   - Drag-and-drop upload, animated loading states, custom-colored emotion progress bars, and a "Show Interpretability" button for GradCAM overlays.
   - Built-in **Demo/Simulation Mode** fallback when model weights are not loaded.

---

## 📁 Project Structure

```
├── assets/
│   └── figures/              # EDA plots, training curves, confusion matrices, GUI screenshots
├── data/                     # AffectNet dataset (Train/ and Test/ subdirectories)
├── gui/                      # Web application frontend
│   ├── index.html            # Main HTML page
│   ├── style.css             # Dark glassmorphic theme styles
│   └── script.js             # Frontend logic (upload, API calls, result display)
├── models/                   # Trained PyTorch model weights
│   ├── resnet18_affectnet.pth   # ★ ResNet-18 on AffectNet (5 classes) — active model
│   ├── resnet18_mma.pth         # ResNet-18 on MMA dataset
│   ├── cnn_affectnet.pth        # Baseline CNN on AffectNet
│   └── cnn_mma.pth             # Baseline CNN on MMA dataset
├── notebooks/
│   └── model_dev.ipynb       # Full training pipeline (EDA, training, evaluation)
├── Dockerfile                # Production container deployment
├── main.py                   # FastAPI server entry point
├── model_utils.py            # MTCNN, PyTorch inference, and Captum GradCAM logic
├── requirements.txt          # Python dependencies
└── ReadME.md                 # Project documentation (this file)
```

---

## 🚀 Local Setup & Run

### Prerequisites
- Python 3.11+

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/Alianger18/Projects_Portfolio.git
cd "Project - Emotions Classification in Images"
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python main.py
```
The server starts on **port 8000** with hot-reload enabled.

### 3. Open the GUI
Navigate to **[http://localhost:8000](http://localhost:8000)** in your browser.

> **Note**: If model weights are not found in `models/`, the app automatically runs in **Demo Mode** with simulated predictions.

---

## 🐳 Docker Deployment

```bash
# Build the Docker image
docker build -t emotion-classifier .

# Run the container
docker run -p 8000:8000 emotion-classifier
```

The built-in health check endpoint at `http://localhost:8000/api/health` automatically monitors the container state.

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/` | Serves the web GUI |
| `GET`  | `/api/health` | Health check — reports model status, device, and class list |
| `POST` | `/api/predict` | Upload an image → returns predicted emotion, confidence, and per-class probabilities |
| `POST` | `/api/interpret` | Upload an image → returns prediction + base64-encoded GradCAM heatmap overlay |

### Example Response (`/api/predict`)
```json
{
  "prediction": "surprise",
  "confidence": 0.932,
  "probabilities": {
    "surprise": 0.932,
    "neutral": 0.037,
    "joy": 0.014,
    "anger": 0.012,
    "sad": 0.005
  },
  "face_detected": true,
  "face_box": [45, 30, 210, 240],
  "emoji": "😲"
}
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Deep Learning** | PyTorch, torchvision (ResNet-18) |
| **Face Detection** | MTCNN (facenet-pytorch) |
| **Interpretability** | Captum (LayerGradCam) |
| **Backend** | FastAPI, Uvicorn |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Containerization** | Docker |

---

## Contributing

If you would like to contribute to this project, please feel free to submit a pull request. We welcome contributions of
all kinds, including bug fixes, feature requests, and code improvements.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
