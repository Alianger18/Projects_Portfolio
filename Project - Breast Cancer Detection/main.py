# Importing the required libraries
from scripts.helping_functions import validate_input, predict_diagnosis, FEATURES
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
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


# Creating Storage class, the default database
class Record(db.Model):
    __tablename__ = 'RECORDS'

    # Primary Key & Timestamp
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=dt.now)

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

    # Add and Commit to the database
    record = Record(**record_data)
    db.session.add(record)
    db.session.commit()

    # Returning the output
    return flask.jsonify(result)

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