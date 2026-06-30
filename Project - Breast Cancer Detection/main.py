# Importing the required libraries
from scripts.helping_functions import validate_input, predict_diagnosis, FEATURES, generate_patient_id
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from flask_cors import CORS
from pathlib import Path
import warnings
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
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>OncoAI API Documentation</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-zinc-50 text-zinc-800 font-sans min-h-screen">
        <div class="max-w-4xl mx-auto px-6 py-12">
            <!-- Header -->
            <header class="border-b border-zinc-200 pb-6 mb-8">
                <div class="flex items-center gap-3 mb-2">
                    <div class="w-8 h-8 rounded bg-black flex items-center justify-center text-white font-black text-lg">Ω</div>
                    <h1 class="text-3xl font-black tracking-tight text-zinc-950">OncoAI API</h1>
                </div>
                <p class="text-zinc-500 text-sm font-medium">Breast Cancer Detection Model-as-a-Service & Human-in-the-Loop Workflow Engine</p>
            </header>

            <!-- Endpoints Section -->
            <section class="space-y-8">
                <h2 class="text-xl font-bold tracking-tight text-zinc-900 border-b border-zinc-150 pb-2">API Endpoints</h2>

                <!-- GET / -->
                <div class="bg-white border border-zinc-200 rounded-xl p-6 shadow-sm">
                    <div class="flex items-center gap-2 mb-3">
                        <span class="bg-emerald-100 text-emerald-800 text-[10px] font-bold px-2 py-0.5 rounded uppercase">GET</span>
                        <code class="font-mono text-zinc-900 font-bold text-sm">/</code>
                    </div>
                    <p class="text-xs text-zinc-655 font-medium mb-4">Serves this interactive API documentation page.</p>
                </div>

                <!-- GET /patients -->
                <div class="bg-white border border-zinc-200 rounded-xl p-6 shadow-sm">
                    <div class="flex items-center gap-2 mb-3">
                        <span class="bg-emerald-100 text-emerald-800 text-[10px] font-bold px-2 py-0.5 rounded uppercase">GET</span>
                        <code class="font-mono text-zinc-900 font-bold text-sm">/patients</code>
                    </div>
                    <p class="text-xs text-zinc-655 font-medium mb-4">Returns a list of all patient diagnostic records ordered by newest first.</p>
                    <div class="bg-zinc-950 text-zinc-250 p-4 rounded-lg text-xs font-mono overflow-x-auto">
                        <span class="text-zinc-400">// Response format:</span>
                        <pre class="text-emerald-400">[
  {
    "id": 1,
    "patient_id": "882-XJ",
    "patient_name": "Catherine Dupont",
    "patient_age": 54,
    "diagnosis": "Malignant",
    "prediction_confidence": 99.78,
    "is_confirmed": null,
    "feedbacks": []
  }
]</pre>
                    </div>
                </div>

                <!-- POST /predict -->
                <div class="bg-white border border-zinc-200 rounded-xl p-6 shadow-sm">
                    <div class="flex items-center gap-2 mb-3">
                        <span class="bg-blue-100 text-blue-800 text-[10px] font-bold px-2 py-0.5 rounded uppercase">POST</span>
                        <code class="font-mono text-zinc-900 font-bold text-sm">/predict</code>
                    </div>
                    <p class="text-xs text-zinc-655 font-medium mb-4">Submits 30 cytological measurements for real-time model prediction. Stores the record in the SQLite database.</p>
                    
                    <div class="space-y-4">
                        <div>
                            <span class="text-[10px] uppercase font-bold tracking-wider text-zinc-400 block mb-1">Payload Sample</span>
                            <div class="bg-zinc-950 text-zinc-250 p-4 rounded-lg text-xs font-mono overflow-x-auto">
                                <pre class="text-blue-400">{
  "radius_mean": 17.99,
  "texture_mean": 10.38,
  "perimeter_mean": 122.8,
  "area_mean": 1001.0,
  "smoothness_mean": 0.1184,
  ...
  "patient_name": "Catherine Dupont",
  "patient_age": 54
}</pre>
                            </div>
                        </div>

                        <div>
                            <span class="text-[10px] uppercase font-bold tracking-wider text-zinc-400 block mb-1">Response Sample</span>
                            <div class="bg-zinc-950 text-zinc-250 p-4 rounded-lg text-xs font-mono overflow-x-auto">
                                <pre class="text-emerald-400">{
  "diagnosis": "Malignant",
  "confidence": 99.78,
  "record_id": 1,
  "patient_id": "882-XJ"
}</pre>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- POST /confirm/<record_id> -->
                <div class="bg-white border border-zinc-200 rounded-xl p-6 shadow-sm">
                    <div class="flex items-center gap-2 mb-3">
                        <span class="bg-blue-100 text-blue-800 text-[10px] font-bold px-2 py-0.5 rounded uppercase">POST</span>
                        <code class="font-mono text-zinc-900 font-bold text-sm">/confirm/&lt;record_id&gt;</code>
                    </div>
                    <p class="text-xs text-zinc-655 font-medium mb-4">Records the oncologist's confirmation of the diagnosis.</p>
                    
                    <div class="space-y-4">
                        <div>
                            <span class="text-[10px] uppercase font-bold tracking-wider text-zinc-400 block mb-1">Payload</span>
                            <div class="bg-zinc-950 text-zinc-250 p-4 rounded-lg text-xs font-mono overflow-x-auto">
                                <pre class="text-blue-400">{
  "is_confirmed": true
}</pre>
                            </div>
                        </div>

                        <div>
                            <span class="text-[10px] uppercase font-bold tracking-wider text-zinc-400 block mb-1">Response</span>
                            <div class="bg-zinc-950 text-zinc-250 p-4 rounded-lg text-xs font-mono overflow-x-auto">
                                <pre class="text-emerald-400">{
  "record_id": 1,
  "diagnosis": "Malignant",
  "is_confirmed": true,
  "message": "Diagnosis confirmed."
}</pre>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- POST /reject/<record_id> -->
                <div class="bg-white border border-zinc-200 rounded-xl p-6 shadow-sm">
                    <div class="flex items-center gap-2 mb-3">
                        <span class="bg-blue-100 text-blue-800 text-[10px] font-bold px-2 py-0.5 rounded uppercase">POST</span>
                        <code class="font-mono text-zinc-900 font-bold text-sm">/reject/&lt;record_id&gt;</code>
                    </div>
                    <p class="text-xs text-zinc-655 font-medium mb-4">Rejects a prediction and records mandatory clinical feedback notes.</p>
                    
                    <div class="space-y-4">
                        <div>
                            <span class="text-[10px] uppercase font-bold tracking-wider text-zinc-400 block mb-1">Payload</span>
                            <div class="bg-zinc-950 text-zinc-250 p-4 rounded-lg text-xs font-mono overflow-x-auto">
                                <pre class="text-blue-400">{
  "feedback_body": "Biopsy morphology indicates a benign fibroadenoma."
}</pre>
                            </div>
                        </div>

                        <div>
                            <span class="text-[10px] uppercase font-bold tracking-wider text-zinc-400 block mb-1">Response</span>
                            <div class="bg-zinc-950 text-zinc-250 p-4 rounded-lg text-xs font-mono overflow-x-auto">
                                <pre class="text-emerald-400">{
  "record_id": 1,
  "patient_id": "882-XJ",
  "diagnosis": "Malignant",
  "is_confirmed": false,
  "feedback_body": "Biopsy morphology indicates a benign fibroadenoma.",
  "message": "Diagnosis rejected. Feedback recorded."
}</pre>
                            </div>
                        </div>
                    </div>
                </div>

            </section>
        </div>
    </body>
    </html>
    """


# The GET PATIENTS route — serve all records to the GUI
@app.route('/patients', methods=['GET'])
def get_patients():
    """Return all patient records ordered by newest first."""
    records = Record.query.order_by(Record.created_at.desc()).all()
    return flask.jsonify([record.to_dict() for record in records])


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


# Launching the flask app
if __name__ == "__main__":
    # Run the Flask application
    with app.app_context():
        db.create_all()
    app.run(debug=True)