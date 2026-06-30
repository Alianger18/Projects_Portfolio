# Data Science in Health Care: Breast Cancer Detection

## Overview

This project is an **anomaly detection** system designed to provide real-time diagnostic scoring for breast cancer
detection. A classification model is trained on the **Wisconsin Breast Cancer Dataset** to predict whether a tumor is
**Malignant** or **Benign**, along with a confidence score. The system consists of three integrated parts:

1. **Flask REST API** — Serves the trained ML model as a prediction service with a human-in-the-loop confirmation workflow.
2. **Data Stream Client** — Simulates real-time FNA biopsy data ingestion by sending patient samples to the API on a timed interval.
3. **React Clinical Dashboard** — A modern diagnostic interface where oncologists review predictions, inspect biopsy features, and confirm or reject AI diagnoses.

### Aim

Early detection of breast cancer is crucial for patient survival. This project aims to assist oncologists by delivering
a high-accuracy, reliable, and efficient model. Beyond clinical utility, it serves as a case study designed to reinforce
trust in AI models and their applications in the health sector.

### About the Data

The data used in this project is the [Wisconsin Breast Cancer Dataset](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic)).
Features are computed from a digitised image of a fine needle aspirate (FNA) of a breast mass and describe
characteristics of the cell nuclei present in the image. The target variable is the diagnosis — either **Malignant** or
**Benign**. Each sample contains 30 numeric features (10 mean, 10 standard error, 10 worst-case measurements).


## Project Structure

```
├── main.py                       # Flask API entry point (port 5000)
├── scripts/
│   ├── helping_functions.py      # Input validation, prediction logic & patient ID generation
│   └── data_stream.py            # Simulated real-time data stream client
├── gui/                          # React clinical dashboard (port 3000)
│   ├── server.ts                 # Express dev server with Flask API proxy
│   ├── vite.config.ts            # Vite + Tailwind CSS v4 configuration
│   ├── package.json              # Node.js dependencies
│   ├── index.html                # HTML entry point
│   └── src/
│       ├── main.tsx              # React entry point
│       ├── App.tsx               # Root application component
│       ├── types.ts              # TypeScript type definitions
│       ├── index.css             # Tailwind CSS import
│       └── components/
│           ├── Header.tsx              # Top navigation bar
│           ├── Sidebar.tsx             # Left navigation rail
│           ├── DiagnosisPane.tsx        # Primary diagnostic workspace
│           ├── DiagnosisResultCard.tsx  # Reusable AI diagnosis result card
│           ├── PatientSearchPane.tsx    # Patient list with search & filters
│           ├── GenomicRecordPane.tsx    # Genomic profiling panel
│           ├── LongitudinalPane.tsx     # Treatment response timeline chart
│           └── ClinicalAssistant.tsx    # AI clinical consultation chat
├── models/
│   └── main_model_v1.joblib      # Trained scikit-learn classification model
├── data/                         # Dataset versions (CSV)
├── notebooks/
│   ├── model_dev_notebook.ipynb  # Model development & evaluation
│   └── model_dep_notebook.ipynb  # Model deployment notebook
├── assets/                       # Figures & metrics
├── docs/                         # Project documentation / task briefs
├── DockerFile                    # Container image definition (Flask API)
├── .dockerignore                 # Files excluded from the Docker build
├── requirements.txt              # Python dependencies
├── LICENSE                       # MIT License
└── ReadMe.md
```


## Getting Started

### Prerequisites

| Component          | Requirement           |
|--------------------|-----------------------|
| Python             | 3.10+                 |
| Node.js            | 18+                   |
| pip                | Latest recommended    |
| npm                | Bundled with Node.js  |

### 1. Clone the Repository

```shell
git clone https://github.com/Alianger18/Projects_Portfolio.git
cd "Project - Breast Cancer Detection"
```

### 2. Install Python Dependencies

```shell
pip install -r requirements.txt
```

### 3. Install Node.js Dependencies

```shell
cd gui
npm install
cd ..
```


## Running the Full System

The system requires **three terminals** running simultaneously. Launch them in the order below.

### Terminal 1 — Start the Flask API

```shell
python main.py
```

The Flask server starts on **`http://127.0.0.1:5000`**. It initialises the SQLite database (`main.db`) on first run and
exposes the prediction, confirmation, and rejection endpoints.

### Terminal 2 — Start the Data Stream

In a **separate terminal**, launch the simulated data stream client. It generates a realistic patient sample (using
centroid interpolation between benign and malignant feature profiles) and sends it to the `/predict` endpoint every
60 seconds:

```shell
python scripts/data_stream.py
```

Each request creates a new patient record in the database with a random name, age, 30 FNA features, and the model's
predicted diagnosis and confidence score. The data stream runs indefinitely until manually stopped (`Ctrl+C`).

### Terminal 3 — Start the React Dashboard

In a **third terminal**, start the clinical dashboard:

```shell
cd gui
npm run dev
```

The Express + Vite dev server starts on **`http://localhost:3000`**. It proxies all `/api/flask/*` requests to the Flask
backend on port 5000, so both services must be running for the dashboard to load patient data.

> **Open `http://localhost:3000` in your browser** to access the OncoAI Diagnostic Dashboard.

### Quick Start Summary

| Terminal | Command                         | Port | Purpose                        |
|----------|---------------------------------|------|--------------------------------|
| 1        | `python main.py`                | 5000 | Flask API (model serving)      |
| 2        | `python scripts/data_stream.py` | —    | Simulated patient data stream  |
| 3        | `cd gui && npm run dev`         | 3000 | React clinical dashboard       |


## API Endpoints

### `GET /`

Health-check endpoint. Returns a status string confirming the API is running.

### `GET /patients`

Returns all patient records ordered by newest first. Used by the React dashboard to populate the patient queue.

### `POST /predict`

Submit a JSON payload with 30 numeric FNA features (and optional patient metadata) to receive a diagnosis.

**Request:**
```json
{
  "radius_mean": 17.99,
  "texture_mean": 10.38,
  "perimeter_mean": 122.8,
  "area_mean": 1001.0,
  "smoothness_mean": 0.1184,
  "compactness_mean": 0.2776,
  "concavity_mean": 0.3001,
  "concave points_mean": 0.1471,
  "symmetry_mean": 0.2419,
  "fractal_dimension_mean": 0.07871,
  "radius_se": 1.095,
  "texture_se": 0.9053,
  "perimeter_se": 8.589,
  "area_se": 153.4,
  "smoothness_se": 0.006399,
  "compactness_se": 0.04904,
  "concavity_se": 0.05373,
  "concave points_se": 0.01587,
  "symmetry_se": 0.03003,
  "fractal_dimension_se": 0.006193,
  "radius_worst": 25.38,
  "texture_worst": 17.33,
  "perimeter_worst": 184.6,
  "area_worst": 2019.0,
  "smoothness_worst": 0.1622,
  "compactness_worst": 0.6656,
  "concavity_worst": 0.7119,
  "concave points_worst": 0.2654,
  "symmetry_worst": 0.4601,
  "fractal_dimension_worst": 0.1189,
  "patient_name": "Catherine Dupont",
  "patient_age": 54
}
```

**Response:**
```json
{
  "diagnosis": "Malignant",
  "confidence": 99.78,
  "record_id": 1,
  "patient_id": "882-XJ"
}
```

### `POST /confirm/<record_id>`

Oncologist confirmation endpoint — confirm or flag a previous prediction for review.

**Request:**
```json
{
  "is_confirmed": true
}
```

**Response:**
```json
{
  "record_id": 1,
  "diagnosis": "Malignant",
  "is_confirmed": true,
  "message": "Diagnosis confirmed."
}
```

### `POST /reject/<record_id>`

Reject a diagnosis with mandatory clinical feedback notes.

**Request:**
```json
{
  "feedback_body": "Histological review shows benign fibroadenoma morphology inconsistent with malignant classification."
}
```

**Response:**
```json
{
  "record_id": 1,
  "patient_id": "882-XJ",
  "diagnosis": "Malignant",
  "is_confirmed": false,
  "feedback_body": "Histological review shows benign fibroadenoma morphology inconsistent with malignant classification.",
  "message": "Diagnosis rejected. Feedback recorded."
}
```


## Docker

The Flask API is fully containerized. Build and run with:

```shell
docker build -t breast-cancer-detection -f DockerFile .
```

```shell
docker run -p 5000:5000 breast-cancer-detection
```

The API will be available at `http://localhost:5000`. Note that the Docker image only packages the Flask API — the React
dashboard should be run separately via `npm run dev` in the `gui/` directory.


## Explore the Notebooks

To inspect model training, evaluation, and feature engineering:

```shell
jupyter notebook notebooks/model_dev_notebook.ipynb
```

To review the model deployment pipeline:

```shell
jupyter notebook notebooks/model_dep_notebook.ipynb
```


## Tech Stack

| Component        | Technology                                  |
|------------------|---------------------------------------------|
| Language         | Python 3.10, TypeScript                     |
| ML Framework     | scikit-learn                                |
| Backend API      | Flask + Flask-SQLAlchemy                    |
| Database         | SQLite                                      |
| Frontend         | React 19 + Vite + Tailwind CSS v4           |
| Dev Server       | Express (proxies Flask API)                 |
| Serialisation    | joblib                                      |
| Visualisation    | Plotly, Matplotlib, Seaborn                 |
| Containerisation | Docker                                      |


## Contributing

If you would like to contribute to this project, please feel free to submit a pull request. We welcome contributions of
all kinds, including bug fixes, feature requests, and code improvements.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
