# Importing the required libraries
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from pre_processing import pre_processing
from datetime import datetime as dt
from pathlib import Path
import numpy as np
import mlflow
import warnings

# Ignore the warnings
warnings.filterwarnings("ignore")


# Creating the path for the model
path = Path.cwd()

# Loading the model
model = mlflow.sklearn.load_model(f"{path}/models/Linear Regression")

# Creating experiment
# mlflow.create_experiment("Running Linear Regression model")

# Initiating the flask app
app = Flask(__name__)

# Configuring our storage with SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)

# Creating Records class, the default database
class Records(db.Model):
    __tablename__ = 'Records'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=dt.utcnow)
    sound = db.Column(db.Integer)
    temperature = db.Column(db.Integer)
    humidity = db.Column(db.Integer)
    score = db.Column(db.Float)

    def __init__(self, sound, temperature, humidity, score):
        self.timestamp = dt.now()
        self.sound = sound
        self.temperature = temperature
        self.humidity = humidity
        self.score = score


# Setting the index route
@app.route('/', methods=['GET'])
def index():
    measurements = Records.query.order_by(Records.timestamp.desc()).limit(10).all()
    return render_template("index.html", measurements=measurements)

# Configuring the predict route
@app.route('/predict', methods=['POST'])
def predict():
    # Getting the actual data
    input_data = pre_processing(request.get_json())

    # Set the experiment as the default experiment
    mlflow.set_experiment("Running Linear Regression model")

    # Generating the prediction
    with mlflow.start_run():
        # Getting model predictions
        output_data = model.predict(input_data)

        # Logging inputs and outputs
        mlflow.log_params({"input_data": input_data, "output_data": output_data})

    # Adjusting values
    sound = input_data[0][0]
    temperature = input_data[0][1]
    humidity = input_data[0][2]
    score = np.round(output_data[0], decimals=2)

    # Creating a record using these values
    record = Records(sound=sound, temperature=temperature, humidity=humidity, score=score)

    # Add the record to the database
    db.session.add(record)
    db.session.commit()

    # Returning the values
    response = f'The predicted value for these measures is : {score}'

    return response


# Launching the flask app
if __name__ == "__main__":
    # Create the Flask application context
    with app.app_context():
        # Create all database tables
        db.create_all()
    # Run the Flask application
    app.run(debug=True)
