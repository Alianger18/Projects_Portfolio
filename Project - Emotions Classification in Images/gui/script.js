// ============================================================
// EMOTION CLASSIFIER — Frontend Logic
// ============================================================

const EMOJIS = {
    anger:    '😠',
    joy:      '😊',
    neutral:  '😐',
    surprise: '😲',
};

// ---------- DOM REFERENCES ----------
const dropZone          = document.getElementById('dropZone');
const fileInput         = document.getElementById('fileInput');
const uploadCard        = document.getElementById('uploadCard');
const resultsContainer  = document.getElementById('resultsContainer');
const previewImage      = document.getElementById('previewImage');
const loadingState      = document.getElementById('loadingState');
const resultsContent    = document.getElementById('resultsContent');
const topEmoji          = document.getElementById('topEmoji');
const topLabel          = document.getElementById('topLabel');
const topConfidence     = document.getElementById('topConfidence');
const allPredictions    = document.getElementById('allPredictions');
const resetBtn          = document.getElementById('resetBtn');
const errorToast        = document.getElementById('errorToast');
const toastMessage      = document.getElementById('toastMessage');
const demoBadge         = document.getElementById('demoBadge');
const interpretBtn      = document.getElementById('interpretBtn');
const heatmapCard       = document.getElementById('heatmapCard');
const heatmapLoading    = document.getElementById('heatmapLoading');
const heatmapImage      = document.getElementById('heatmapImage');

// Store the current file for re-submission to /api/interpret
let currentFile = null;


// ---------- DRAG & DROP ----------
dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
});

dropZone.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    const files = e.dataTransfer.files;
    if (files.length > 0 && files[0].type.startsWith('image/')) {
        handleFile(files[0]);
    } else {
        showToast('Please drop a valid image file.');
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});


// ---------- FILE HANDLING ----------
function handleFile(file) {
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
    };
    reader.readAsDataURL(file);

    // Switch to results view
    uploadCard.style.display = 'none';
    resultsContainer.classList.add('visible');
    loadingState.style.display = 'flex';
    resultsContent.classList.remove('visible');
    heatmapCard.style.display = 'none';

    // Store file for later interpretability request
    currentFile = file;

    // Send to API
    uploadAndPredict(file);
}


// ---------- API CALL ----------
async function uploadAndPredict(file) {
    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/api/predict', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Server error (${response.status})`);
        }

        const result = await response.json();
        displayResults(result);

    } catch (err) {
        showToast(err.message || 'Failed to get prediction. Is the server running?');
        // Show the upload zone again so user can retry
        resetView();
    }
}


// ---------- DISPLAY RESULTS ----------
function displayResults(result) {
    // Hide loading
    loadingState.style.display = 'none';

    // Top prediction
    topEmoji.textContent      = EMOJIS[result.prediction] || '🤔';
    topLabel.textContent      = result.prediction;
    topConfidence.textContent = `${(result.confidence * 100).toFixed(1)}% confidence`;

    // Build per-class bars
    allPredictions.innerHTML = '';

    // Sort by probability descending
    const sorted = Object.entries(result.probabilities)
        .sort((a, b) => b[1] - a[1]);

    sorted.forEach(([emotion, prob]) => {
        const pct = (prob * 100).toFixed(1);

        const row = document.createElement('div');
        row.className = 'pred-row';

        row.innerHTML = `
            <span class="pred-emoji">${EMOJIS[emotion] || ''}</span>
            <span class="pred-label">${emotion}</span>
            <div class="pred-bar-track">
                <div class="pred-bar-fill" data-emotion="${emotion}"></div>
            </div>
            <span class="pred-pct">${pct}%</span>
        `;

        allPredictions.appendChild(row);

        // Animate bar width after a small delay
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                row.querySelector('.pred-bar-fill').style.width = `${pct}%`;
            });
        });
    });

    // Show results
    resultsContent.classList.add('visible');

    // Show interpret button only when model is loaded (not demo mode)
    if (!result.is_demo) {
        interpretBtn.style.display = 'inline-flex';
    } else {
        interpretBtn.style.display = 'none';
    }
}


// ---------- INTERPRETABILITY (GradCAM) ----------
interpretBtn.addEventListener('click', interpretImage);

async function interpretImage() {
    if (!currentFile) return;

    // Show heatmap card with loading state
    heatmapCard.style.display = 'block';
    heatmapLoading.style.display = 'flex';
    heatmapImage.style.display = 'none';
    interpretBtn.disabled = true;
    interpretBtn.textContent = 'Generating...';

    try {
        const formData = new FormData();
        formData.append('file', currentFile);

        const response = await fetch('/api/interpret', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Server error (${response.status})`);
        }

        const result = await response.json();

        // Display heatmap
        heatmapLoading.style.display = 'none';
        heatmapImage.src = result.heatmap;
        heatmapImage.style.display = 'block';

    } catch (err) {
        showToast(err.message || 'Failed to generate heatmap.');
        heatmapCard.style.display = 'none';
    } finally {
        interpretBtn.disabled = false;
        interpretBtn.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                 stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"/>
                <path d="m21 21-4.35-4.35"/>
            </svg>
            Show Interpretability
        `;
    }
}


// ---------- RESET ----------
resetBtn.addEventListener('click', resetView);

function resetView() {
    resultsContainer.classList.remove('visible');
    uploadCard.style.display = 'block';
    loadingState.style.display = 'flex';
    resultsContent.classList.remove('visible');
    allPredictions.innerHTML = '';
    fileInput.value = '';
    currentFile = null;

    // Reset heatmap
    heatmapCard.style.display = 'none';
    heatmapImage.src = '';
    heatmapImage.style.display = 'none';
    interpretBtn.style.display = 'none';

    // Re-trigger entrance animation
    uploadCard.style.animation = 'none';
    uploadCard.offsetHeight; // reflow
    uploadCard.style.animation = '';
}


// ---------- TOAST NOTIFICATIONS ----------
let toastTimer = null;

function showToast(message) {
    toastMessage.textContent = message;
    errorToast.classList.add('visible');

    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
        errorToast.classList.remove('visible');
    }, 5000);
}


// ---------- INITIAL HEALTH CHECK ----------
async function checkHealth() {
    try {
        const response = await fetch('/api/health');
        if (response.ok) {
            const data = await response.json();
            if (!data.model_loaded) {
                demoBadge.style.display = 'inline-block';
            } else {
                demoBadge.style.display = 'none';
            }
        }
    } catch (e) {
        console.warn('Health check connection failed:', e);
    }
}

window.addEventListener('DOMContentLoaded', checkHealth);
