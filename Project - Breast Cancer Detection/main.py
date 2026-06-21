# Importing the required libraries
from scripts.helping_functions import validate_input, predict_diagnosis
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from pathlib import Path
import numpy as np
import warnings
import sklearn
import flask


# Ignore the warnings
warnings.filterwarnings("ignore")

# Creating the path for the model
path = Path.cwd()

# Initiating the flask app
app = flask.Flask(__name__)

# Configuring the database and its models
# Setting our storage with SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path}/main.db'
db = SQLAlchemy(app)


# Creating Storage class, the default database
class Storage(db.Model):
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


# Setting the API routes
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
        flask.raise_error(500, "Invalid input data. Please check the documentation.")

    # Predicting the output
    output = predict_diagnosis(input_data)

    # Storing the data in the database


    # Returning the output
    return output



# Launching the flask app
if __name__ == "__main__":
    # Run the Flask application
    with app.app_context():
        db.create_all()
    app.run(debug=True)