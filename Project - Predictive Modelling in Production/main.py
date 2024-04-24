# Importing the required libraries
from helping_functions import pre_processing, validation, check_experiment, store_data
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from flask import Flask, request
from pathlib import Path
import numpy as np
import warnings
import mlflow

# Ignore the warnings
warnings.filterwarnings("ignore")

# Loading and tracking the runs of the model inside mlflow experiments
# Creating the path for the model
path = Path.cwd()

# Loading the model
model = mlflow.sklearn.load_model(f"{path}/models/Linear Regression")

# Start Tracking
experiment_name = check_experiment("Linear Regression")
mlflow.create_experiment(experiment_name)

# Initiating the flask app
app = Flask(__name__)

# Configuring the database and its models
# Setting our storage with SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path}/main.db'
db = SQLAlchemy(app)


# Creating Storage class, the default database
class Storage(db.Model):
    __tablename__ = 'RECORDS'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=dt.utcnow())
    sound = db.Column(db.Integer)
    temperature = db.Column(db.Integer)
    humidity = db.Column(db.Integer)
    score = db.Column(db.Float)

    def __init__(self, sound, temperature, humidity, score):
        self.timestamp = dt.utcnow()
        self.sound = sound
        self.temperature = temperature
        self.humidity = humidity
        self.score = score


# Setting the API routes
# The index route
@app.route('/', methods=['GET'])
def index():
    return "Provide Documentation here!"

# The PREDICT route
@app.route('/predict', methods=['POST'])
def predict():
    # Getting the actual data
    input_data = pre_processing(request.get_json())

    # Validating the data
    if validation(input_data):
        # Set the experiment as the default experiment
        mlflow.set_experiment(f"{experiment_name}")

        # Starting a new run
        with mlflow.start_run():
            # Getting model predictions
            output_data = model.predict(input_data)

            # Logging inputs
            mlflow.log_params({"Sound": input_data[0][0]})
            mlflow.log_params({"Temperature": input_data[0][1]})
            mlflow.log_params({"Humidity": input_data[0][2]})

            # Logging output
            mlflow.log_params({"Score": np.round(output_data[0], decimals=2)})

        # Storing the data
        store_data(db, Storage, input_data, output_data)

        # Returning the values
        response = f'The predicted value for these measures is : {np.round(output_data[0], decimals=2)}'

        return response

    else:
        return "The input data is not valid"


# Launching the flask app
if __name__ == "__main__":
    # Run the Flask application
    with app.app_context():
        db.create_all()
    app.run(debug=True)
