# Importing the required libraries
from helping_functions import pre_processing, check_experiment, run_gunicorn
from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt
from pathlib import Path
import numpy as np
import warnings
import sqlite3
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

# Creating Records class, the default database
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
    return render_template(template_name_or_list='index.html')

# The STORE route
@app.route('/store', methods=['GET'])
def store(input_measurements, output_score):
    # Adjusting values
    sound = input_measurements[0][0]
    temperature = input_measurements[0][1]
    humidity = input_measurements[0][2]
    score = np.round(output_score[0], decimals=2)

    # Creating a record using these values
    record = Storage(sound=sound, temperature=temperature, humidity=humidity, score=score)

    # Add the record to the database
    db.session.add(record)
    db.session.commit()

    return None

# The PREDICT route
@app.route('/predict', methods=['POST'])
def predict():
    # Getting the actual data
    input_data = pre_processing(request.get_json())

    # Set the experiment as the default experiment
    mlflow.set_experiment(f"{experiment_name}")

    # Generating the prediction
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
    store(input_data, output_data)

    # Returning the values
    response = f'The predicted value for these measures is : {np.round(output_data[0], decimals=2)}'
    return response

# The UPDATE route
@app.route('/api/data', methods=['GET'])
def update():
    """
    This endpoint is used to update the dashboard with data from the database
    :return: json response with 17 rows from the updated database
    """
    # Connecting and fetching the last 17 rows
    with sqlite3.connect('main.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM RECORDS ORDER BY TIMESTAMP DESC LIMIT 17")
        data = cursor.fetchall()

    # Return response with 17 rows of data
    return jsonify(
        [
            {'timestamp': row[1],
             'sound': row[2],
             'temperature': row[3],
             'humidity': row[4],
             'score': row[5]
             } for row in data
        ]
    )


# Launching the flask app
if __name__ == "__main__":
    # Create the Flask application context
    with app.app_context():
        # Create all database tables
        db.create_all()
    # Run the Flask application
    app.run(debug=True)
