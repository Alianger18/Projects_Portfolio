# Importing the required libraries
import pickle
from generate_data import generate_sensor_data
import numpy as np
from flask import Flask, request, json

# Loading the model
model = pickle.load(open('model_1.pkl', 'rb'))

# Initiating the flask app
app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    # Getting the actual data
    x_infer = list(request.json.values())

    # Generating the prediction
    y_infer = model.predict([x_infer])[0]

    # Returning the values
    return json.dumps(f'The predicted value for these measures is : %.3f' % y_infer)


# Launching the app
if __name__ == "__main__":
    app.run()
