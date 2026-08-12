# 🎭 Facial Emotion Classifier with MTCNN & Captum

A premium, responsive deep learning application to classify facial expressions into **four target emotion categories**: **Anger, Joy, Neutral, and Surprise**.

The project features a FastAPI backend running inference on a PyTorch CNN/ResNet-18 model, combined with MTCNN face detection and an interactive modern web GUI displaying real-time confidence scores and **GradCAM interpretability heatmaps**.

---

## 📊 About the Dataset

This project uses the **AffectNet** dataset (available on [Kaggle](https://www.kaggle.com/datasets/mstjebashazida/affectnet)), a large-scale facial expression dataset containing in-the-wild facial images.

- **Target Classes**: Filtered to **4 primary emotions**: `anger`, `happy` (joy), `neutral`, and `surprise`.
- **Native Resolution & Format**: **96×96 pixels** native **RGB** images.
- **Data Directory Structure**: Organized into `Train/` and `Test/` directories with folder-based emotion labels.
- **Train/Validation Split**: An **80/20 stratified split** is constructed from `Train/` for training and hyperparameter validation.
- **Preprocessing & Augmentation Pipeline**:
  - **Training**: `Resize(256)` → `RandomCrop(224)` → `RandomHorizontalFlip` → `RandomRotation(10°)` → `ColorJitter` → `ImageNet Normalization`
  - **Validation & Test**: `Resize(256)` → `CenterCrop(224)` → `ImageNet Normalization` (`mean=[0.485, 0.456, 0.406]`, `std=[0.229, 0.224, 0.225]`)

---

## Key Features

1. **MTCNN Face Detection & Alignment**
   - Automatically detects, aligns, and crops the largest face from any uploaded image with a 15% margin.
   - Falls back to the original image if no face is found.
2. **Model Interpretability (Captum LayerGradCam)**
   - Computes spatial feature attributions on the last convolutional layer (`block4[3]` for CNN, `layer4[-1].conv2` for ResNet).
   - Overlays a jet-colored attribution heatmap on the cropped face to show which regions (e.g., mouth, eyes, brow furrow) drove the prediction.
3. **Target 4-Class Mapping**
   - Directly predicts probabilities across Anger, Joy, Neutral, and Surprise.
4. **Modern Glassmorphic Web GUI**
   - Layout places the image preview on the left and predictions on the right.
   - Drag-and-drop file interface, animated loading states, custom-colored emotion progress bars, and a "Show Interpretability" view.
   - Built-in **Demo/Simulation Mode** fallback when model weights are not loaded.

---

## Project Structure

```
├── data/                 # AffectNet dataset (Train/ and Test/ subdirectories)
├── gui/                  # Web application frontend assets (HTML, CSS, JS)
│   ├── index.html
│   ├── style.css
│   └── script.js
├── models/               # Saved trained PyTorch models
│   └── best_cnn.pth
├── notebooks/            # Exploratory data analysis & model development
│   └── model_dev.ipynb   # Complete training pipeline for AffectNet
├── Dockerfile            # Container deployment script
├── main.py               # FastAPI server entry point
├── model_utils.py        # MTCNN, PyTorch inference, and Captum logic
├── requirements.txt      # Python dependencies
└── ReadME.md             # Project documentation (this file)
```

---

## Local Setup & Run

### 1. Install Dependencies
Ensure you have Python 3.11 installed, then install the required libraries:
```powershell
pip install -r requirements.txt
```

### 2. Start the Server
Run the uvicorn development server from the root of the project directory:
```powershell
& python.exe -m uvicorn main:app --reload --port 8000
```

### 3. Open the GUI
Navigate to **[http://localhost:8000](http://localhost:8000)** in your browser.

---

## Docker Deployment

To containerize and run the application in a docker container:

```bash
# Build the Docker image
docker build -t emotion-classifier .

# Run the container
docker run -p 8000:8000 emotion-classifier
```
The health check endpoint at `http://localhost:8000/api/health` automatically monitors the container state.
