# Importing the required libraries
from scripts.helping_functions import validate_input, predict_diagnosis, FEATURES
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from flask_cors import CORS
from pathlib import Path
import warnings
import random
import string
import flask


# Ignore the warnings
warnings.filterwarnings("ignore")

# Creating the path for the model
path = Path.cwd()

# Initiating the flask app
app = flask.Flask(__name__)

# Configuring the database and its models
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path}/main.db'
db = SQLAlchemy(app)

# Enable CORS for the GUI running on port 3000
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


# --- Helper Functions ---------------------------------------------------
def generate_patient_id() -> str:
    """Generate a unique patient ID in the format '###-XX' (e.g. '882-XJ')."""
    num = random.randint(100, 999)
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    return f"{num}-{letters}"
# -------------------------------------------------------------------------


# --- Centroid profiles for controlled sample generation ------------------
# Mean feature values for benign cases in the Wisconsin Breast Cancer Dataset
BENIGN_CENTROID = {
    "radius_mean": 12.15, "texture_mean": 17.91, "perimeter_mean": 78.08,
    "area_mean": 462.79, "smoothness_mean": 0.0925, "compactness_mean": 0.0801,
    "concavity_mean": 0.0461, "concave points_mean": 0.0257, "symmetry_mean": 0.1742,
    "fractal_dimension_mean": 0.0629, "radius_se": 0.2840, "texture_se": 1.2200,
    "perimeter_se": 2.0000, "area_se": 21.14, "smoothness_se": 0.0071,
    "compactness_se": 0.0213, "concavity_se": 0.0260, "concave points_se": 0.0091,
    "symmetry_se": 0.0206, "fractal_dimension_se": 0.0037, "radius_worst": 13.38,
    "texture_worst": 23.52, "perimeter_worst": 87.01, "area_worst": 558.90,
    "smoothness_worst": 0.1250, "compactness_worst": 0.1827, "concavity_worst": 0.1663,
    "concave points_worst": 0.0742, "symmetry_worst": 0.2701, "fractal_dimension_worst": 0.0795
}

# Mean feature values for malignant cases in the Wisconsin Breast Cancer Dataset
MALIGNANT_CENTROID = {
    "radius_mean": 17.46, "texture_mean": 21.60, "perimeter_mean": 115.37,
    "area_mean": 978.38, "smoothness_mean": 0.1029, "compactness_mean": 0.1454,
    "concavity_mean": 0.1607, "concave points_mean": 0.0880, "symmetry_mean": 0.1929,
    "fractal_dimension_mean": 0.0627, "radius_se": 0.6090, "texture_se": 1.2100,
    "perimeter_se": 4.3200, "area_se": 72.67, "smoothness_se": 0.0071,
    "compactness_se": 0.0321, "concavity_se": 0.0418, "concave points_se": 0.0152,
    "symmetry_se": 0.0206, "fractal_dimension_se": 0.0040, "radius_worst": 21.13,
    "texture_worst": 29.32, "perimeter_worst": 141.37, "area_worst": 1422.29,
    "smoothness_worst": 0.1449, "compactness_worst": 0.3749, "concavity_worst": 0.4506,
    "concave points_worst": 0.1822, "symmetry_worst": 0.3234, "fractal_dimension_worst": 0.0916
}
# -------------------------------------------------------------------------


# Creating Storage class, the default database
class Record(db.Model):
    __tablename__ = 'RECORDS'

    # Primary Key & Timestamp
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=dt.now)

    # --- Patient Identification ---
    patient_id = db.Column(db.String(20), unique=True, nullable=False)
    patient_name = db.Column(db.String(100), nullable=False, default='Unknown Patient')
    patient_age = db.Column(db.Integer, nullable=True)

    # --- Mean Features ---
    radius_mean = db.Column(db.Float)
    texture_mean = db.Column(db.Float)
    perimeter_mean = db.Column(db.Float)
    area_mean = db.Column(db.Float)
    smoothness_mean = db.Column(db.Float)
    compactness_mean = db.Column(db.Float)
    concavity_mean = db.Column(db.Float)
    concave_points_mean = db.Column(db.Float)
    symmetry_mean = db.Column(db.Float)
    fractal_dimension_mean = db.Column(db.Float)

    # --- Standard Error (SE) Features ---
    radius_se = db.Column(db.Float)
    texture_se = db.Column(db.Float)
    perimeter_se = db.Column(db.Float)
    area_se = db.Column(db.Float)
    smoothness_se = db.Column(db.Float)
    compactness_se = db.Column(db.Float)
    concavity_se = db.Column(db.Float)
    concave_points_se = db.Column(db.Float)
    symmetry_se = db.Column(db.Float)
    fractal_dimension_se = db.Column(db.Float)

    # --- Worst Features ---
    radius_worst = db.Column(db.Float)
    texture_worst = db.Column(db.Float)
    perimeter_worst = db.Column(db.Float)
    area_worst = db.Column(db.Float)
    smoothness_worst = db.Column(db.Float)
    compactness_worst = db.Column(db.Float)
    concavity_worst = db.Column(db.Float)
    concave_points_worst = db.Column(db.Float)
    symmetry_worst = db.Column(db.Float)
    fractal_dimension_worst = db.Column(db.Float)

    # --- Output/Score ---
    diagnosis = db.Column(db.String(10))
    prediction_confidence = db.Column(db.Float)

    # --- Human-in-the-Loop ---
    # None = pending review, True = confirmed, False = flagged for review
    is_confirmed = db.Column(db.Boolean, nullable=True, default=None)

    # --- Relationships ---
    feedbacks = db.relationship('Feedback', backref='record', lazy=True)

    def to_dict(self) -> dict:
        """Serialize the record to a dictionary for JSON responses."""
        result = {
            "id": self.id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "patient_id": self.patient_id,
            "patient_name": self.patient_name,
            "patient_age": self.patient_age,
            "diagnosis": self.diagnosis,
            "prediction_confidence": self.prediction_confidence,
            "is_confirmed": self.is_confirmed,
        }

        # Include all 30 features (using underscored column names)
        for feature in FEATURES:
            column_name = feature.replace(" ", "_")
            result[column_name] = getattr(self, column_name, None)

        # Include associated feedbacks
        result["feedbacks"] = [
            {
                "feedback_id": f.feedback_id,
                "feedback_body": f.feedback_body,
                "created_at": f.created_at.isoformat() if f.created_at else None,
            }
            for f in self.feedbacks
        ]

        return result


# Creating the Feedback model for rejection notes
class Feedback(db.Model):
    __tablename__ = 'FEEDBACKS'

    feedback_id = db.Column(db.Integer, primary_key=True)
    feedback_body = db.Column(db.Text, nullable=False)
    record_id = db.Column(db.Integer, db.ForeignKey('RECORDS.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=dt.now)


# Setting the API routes -----------------------------------------------
# The index route
@app.route('/', methods=['GET'])
def index():
    return "Provide Documentation here!"

# The PREDICT route
@app.route('/predict', methods=['POST'])
def predict():
    # Getting the data
    input_data = flask.request.get_json()

    # Validating the data, in case invalid, return an error message
    if not validate_input(input_data):
        flask.abort(400, description="Invalid input data. Please check the documentation.")

    # Predicting the output
    result = predict_diagnosis(input_data)

    # Storing the data in the database
    # Map feature names with spaces to underscored column names
    record_data = {}
    for feature in FEATURES:
        column_name = feature.replace(" ", "_")
        record_data[column_name] = input_data[feature]

    # Get the predictions
    record_data["diagnosis"] = result["diagnosis"]
    record_data["prediction_confidence"] = result["confidence"]

    # Get optional patient identification fields
    record_data["patient_id"] = input_data.get("patient_id") or generate_patient_id()
    record_data["patient_name"] = input_data.get("patient_name", "Unknown Patient")
    record_data["patient_age"] = input_data.get("patient_age")

    # Add and Commit to the database
    record = Record(**record_data)
    db.session.add(record)
    db.session.commit()

    # Returning the output (include record info for the GUI)
    result["record_id"] = record.id
    result["patient_id"] = record.patient_id
    return flask.jsonify(result)


# The GET PATIENTS route — serve all records to the GUI
@app.route('/patients', methods=['GET'])
def get_patients():
    """Return all patient records ordered by newest first."""
    records = Record.query.order_by(Record.created_at.desc()).all()
    return flask.jsonify([record.to_dict() for record in records])


# The REJECT route — reject a diagnosis with mandatory clinical feedback
@app.route('/reject/<int:record_id>', methods=['POST'])
def reject(record_id):
    """Reject a diagnosis and store the oncologist's feedback."""
    # Getting the rejection data
    rejection_data = flask.request.get_json()

    # Validate the payload
    if not rejection_data or "feedback_body" not in rejection_data:
        flask.abort(400, description="Missing 'feedback_body' field.")

    feedback_body = rejection_data["feedback_body"]
    if not isinstance(feedback_body, str) or not feedback_body.strip():
        flask.abort(400, description="'feedback_body' must be a non-empty string.")

    # Fetch the record from the database
    record = db.session.get(Record, record_id)
    if record is None:
        flask.abort(404, description=f"Record with id {record_id} not found.")

    # Update the confirmation status to rejected
    record.is_confirmed = False

    # Create and store the feedback
    feedback = Feedback(
        feedback_body=feedback_body.strip(),
        record_id=record_id,
    )
    db.session.add(feedback)
    db.session.commit()

    return flask.jsonify({
        "record_id": record.id,
        "patient_id": record.patient_id,
        "diagnosis": record.diagnosis,
        "is_confirmed": record.is_confirmed,
        "feedback_body": feedback_body.strip(),
        "message": "Diagnosis rejected. Feedback recorded."
    })


# The GENERATE route — produce controlled sample feature sets
@app.route('/generate', methods=['POST'])
def generate():
    """
    Generate a realistic set of 30 features by interpolating between
    known benign and malignant centroids. Accepts an optional
    'target_confidence' (50-99) to control the malignancy level.
    """
    request_data = flask.request.get_json() or {}

    # Get or randomize the target confidence
    target_confidence = request_data.get("target_confidence")
    if target_confidence is None:
        target_confidence = random.choice([55, 65, 72, 78, 85, 91, 95])
    else:
        target_confidence = max(50, min(99, int(target_confidence)))

    # Compute the mixing ratio (0 = fully benign, 1 = fully malignant)
    t = target_confidence / 100.0

    # Interpolate features between centroids with controlled Gaussian noise
    generated_features = {}
    for feature in FEATURES:
        benign_val = BENIGN_CENTROID[feature]
        malignant_val = MALIGNANT_CENTROID[feature]

        # Linear interpolation
        interpolated = benign_val * (1 - t) + malignant_val * t

        # Add small Gaussian noise (5% of the feature range) for realism
        feature_range = abs(malignant_val - benign_val)
        noise = random.gauss(0, feature_range * 0.05)
        value = interpolated + noise

        # Ensure non-negative values
        generated_features[feature] = round(max(0.0, value), 6)

    # Run through the actual sklearn model to get the real prediction
    result = predict_diagnosis(generated_features)

    return flask.jsonify({
        "features": generated_features,
        "diagnosis": result["diagnosis"],
        "confidence": result["confidence"],
        "target_confidence": target_confidence,
    })


# The CONFIRMATION route — oncologist confirms or rejects a diagnosis
@app.route('/confirm/<int:record_id>', methods=['POST'])
def confirm(record_id):
    # Getting the confirmation data
    confirmation_data = flask.request.get_json()

    # Validate the payload
    if "is_confirmed" not in confirmation_data:
        flask.abort(400, description="Missing 'is_confirmed' field. Must be true or false.")

    if not isinstance(confirmation_data["is_confirmed"], bool):
        flask.abort(400, description="'is_confirmed' must be a boolean (true or false).")

    # Fetch the record from the database
    record = db.session.get(Record, record_id)
    if record is None:
        flask.abort(404, description=f"Record with id {record_id} not found.")

    # Update the confirmation status
    record.is_confirmed = confirmation_data["is_confirmed"]
    db.session.commit()

    return flask.jsonify({
        "record_id": record.id,
        "diagnosis": record.diagnosis,
        "is_confirmed": record.is_confirmed,
        "message": "Diagnosis confirmed." if record.is_confirmed else "Diagnosis flagged for review."
    })
# ---------------------------------------------------------------------


# Launching the flask app
if __name__ == "__main__":
    # Run the Flask application
    with app.app_context():
        db.create_all()
    app.run(debug=True)