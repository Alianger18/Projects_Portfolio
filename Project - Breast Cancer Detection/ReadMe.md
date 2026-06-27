# Data Science in Health Care: Breast Cancer Detection


## Overview

This project is an __anomaly detection__ system designed to provide real-time diagnostic scoring for breast cancer
detection. A classification model is trained on the __Wisconsin Breast Cancer Dataset__ to predict whether a tumour is
**Malignant** or **Benign**, along with a confidence score. The model is deployed as a **Flask REST API** (Model-as-a-Service)
and includes a human-in-the-loop confirmation workflow so oncologists can verify or flag each prediction.

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
├── main.py                  # Flask API entry point
├── scripts/
│   ├── helping_functions.py # Input validation & prediction logic
│   ├── data_stream.py       # Simulated real-time data stream client
│   └── dashboard.py         # Dash monitoring dashboard
├── models/
│   └── main_model_v1.joblib # Trained classification model
├── data/                    # Dataset versions (CSV)
├── notebooks/
│   ├── model_dev_notebook.ipynb  # Model development & evaluation
│   └── model_dep_notebook.ipynb  # Model deployment notebook
├── assets/                  # Figures & metrics
├── docs/                    # Project documentation / task briefs
├── DockerFile               # Container image definition
├── .dockerignore            # Files excluded from the Docker build
├── requirements.txt         # Python dependencies
├── LICENSE                  # MIT License
└── ReadMe.md
```


## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

```shell
pip install -r requirements.txt
```

### Launch the API (Model-as-a-Service)

```shell
python main.py
```

The Flask server starts on `http://127.0.0.1:5000`.

### Start the Data Stream

In a **separate terminal**, run the simulated data stream client. It sends a randomly generated sample to the
`/predict` endpoint every 60 seconds:

```shell
python scripts/data_stream.py
```

### View the Dashboard

After launching the API and the data stream, start the monitoring dashboard:

```shell
python scripts/dashboard.py
```

### Explore the Notebooks

To inspect model training, evaluation, and selection:

```shell
jupyter notebook notebooks/model_dev_notebook.ipynb
```


## API Endpoints

### `GET /`

Health-check / documentation stub.

### `POST /predict`

Submit a JSON payload with 30 numeric features and receive a diagnosis.

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
  "fractal_dimension_worst": 0.1189
}
```

**Response:**
```json
{
  "diagnosis": "Malignant",
  "confidence": 99.78
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


## Docker

The project is fully containerised. Build and run with:

```shell
docker build -t breast-cancer-detection -f DockerFile .
```

```shell
docker run -p 5000:5000 breast-cancer-detection
```

The API will be available at `http://localhost:5000`.


## Tech Stack

| Component       | Technology                    |
|-----------------|-------------------------------|
| Language        | Python 3.10                   |
| Web Framework   | Flask                         |
| ML Library      | scikit-learn                  |
| Database        | SQLite (via Flask-SQLAlchemy) |
| Serialisation   | joblib                        |
| Visualisation   | Plotly, Matplotlib, Seaborn   |
| Containerisation| Docker                        |


## Contributing

If you would like to contribute to this project, please feel free to submit a pull request. We welcome contributions of
all kinds, including bug fixes, feature requests, and code improvements.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
