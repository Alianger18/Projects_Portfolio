# Import the required libraries
from model_utils import load_model, predict, generate_attribution, CLASS_NAMES, EMOTION_EMOJIS
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from pathlib import Path
from PIL import Image
import torch
import sys
import io

# Add parent directory of main.py to sys.path so model_utils can be imported cleanly
sys.path.append(str(Path(__file__).resolve().parent))

# ============================================================================
# CONFIGURATION
# ============================================================================
MODEL_DIR = Path(__file__).resolve().parent / 'models'
STATIC_DIR = Path(__file__).resolve().parent / 'gui'

# Model selection — change these to switch between CNN and ResNet
MODEL_TYPE = 'cnn'                     # 'cnn' or 'resnet'
MODEL_FILE = 'best_cnn.pth'           # 'best_cnn.pth' or 'best_resnet18.pth'

DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Global model reference
model = None


# ============================================================================
# APP LIFESPAN — Load model on startup
# ============================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load the model when the server starts."""
    global model
    model_path = MODEL_DIR / MODEL_FILE

    if not model_path.exists():
        print(f'\n  WARNING: Model weights not found at {model_path}')
        print(f'  Train the model first using the model_dev.ipynb notebook.')
        print(f'  The API will return errors until a trained model is available.\n')
        model = None
    else:
        print(f'\n  Loading model: {MODEL_TYPE.upper()} from {model_path}')
        model = load_model(model_path, model_type=MODEL_TYPE, device=DEVICE)
        print(f'  Model loaded successfully on {DEVICE}')
        print(f'  Classes: {CLASS_NAMES}\n')

    yield  # App runs here

    # Cleanup on shutdown
    model = None
    print('Model unloaded.')


# ============================================================================
# FASTAPI APP
# ============================================================================
app = FastAPI(
    title='Emotion Classifier API',
    description='Upload a facial image to classify the expressed emotion.',
    version='1.0.0',
    lifespan=lifespan,
)

# CORS — allow frontend requests during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Serve static files (CSS, JS, images) from gui/ at the /static prefix
app.mount('/static', StaticFiles(directory=str(STATIC_DIR)), name='static')


# ============================================================================
# ROUTES
# ============================================================================
@app.get('/')
async def serve_frontend():
    """Serve the main HTML page."""
    return FileResponse(STATIC_DIR / 'index.html')


@app.get('/api/health')
async def health_check():
    """Health check endpoint."""
    return {
        'status': 'ok',
        'model_loaded': model is not None,
        'model_type': MODEL_TYPE,
        'device': str(DEVICE),
        'classes': CLASS_NAMES,
    }


@app.post('/api/predict')
async def predict_emotion(file: UploadFile = File(...)):
    """
    Accept an image upload and return emotion predictions.

    Returns:
        JSON with prediction, confidence, and per-class probabilities.
    """
    is_demo = False
    # Check that model is loaded; if not, fall back to simulation/demo mode
    if model is None:
        is_demo = True

    # Validate file type
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail=f'Invalid file type: {file.content_type}. Please upload an image.'
        )

    try:
        # Read and open the image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        if not is_demo:
            # Run prediction on real model
            result = predict(model, image, model_type=MODEL_TYPE, device=DEVICE)
            result['is_demo'] = False
        else:
            # Generate simulated/mock prediction
            import random
            top_class = random.choice(CLASS_NAMES)
            top_conf = round(random.uniform(0.45, 0.92), 4)
            
            # Distribute remaining probability among other classes
            remaining = 1.0 - top_conf
            others = [c for c in CLASS_NAMES if c != top_class]
            raw_weights = [random.uniform(0.1, 1.0) for _ in others]
            sum_weights = sum(raw_weights)
            
            probs = {top_class: top_conf}
            for i, c in enumerate(others):
                probs[c] = round((raw_weights[i] / sum_weights) * remaining, 4)
            
            # Adjust rounding errors so it sums to exactly 1.0
            diff = round(1.0 - sum(probs.values()), 4)
            probs[others[0]] = round(probs[others[0]] + diff, 4)

            result = {
                'prediction': top_class,
                'confidence': top_conf,
                'probabilities': probs,
                'face_detected': True,
                'face_box': None,
                'is_demo': True
            }

        # Add emoji to response
        result['emoji'] = EMOTION_EMOJIS.get(result['prediction'], '')

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Prediction failed: {str(e)}'
        )


# ============================================================================
# INTERPRETABILITY
# ============================================================================
@app.post('/api/interpret')
async def interpret_emotion(file: UploadFile = File(...)):
    """
    Run prediction + GradCAM interpretability on an uploaded image.

    Returns the prediction result plus a base64-encoded heatmap overlay
    showing which facial regions influenced the classification.
    """
    if model is None:
        raise HTTPException(
            status_code=503,
            detail='Model not loaded. Train the model first using model_dev.ipynb, '
                   'then restart the server.'
        )

    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=400,
            detail=f'Invalid file type: {file.content_type}. Please upload an image.'
        )

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # Run prediction (with face detection)
        result = predict(model, image, model_type=MODEL_TYPE, device=DEVICE)

        # Generate GradCAM heatmap
        heatmap_b64 = generate_attribution(
            model, image, model_type=MODEL_TYPE, device=DEVICE
        )
        result['heatmap'] = heatmap_b64
        result['emoji'] = EMOTION_EMOJIS.get(result['prediction'], '')

        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Interpretation failed: {str(e)}'
        )


# ============================================================================
# MAIN
# ============================================================================
if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
