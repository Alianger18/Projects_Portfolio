# Import the required libraries
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from datetime import datetime as dt
from pathlib import Path
import numpy as np
import sklearn

# Creating the path for the model
path = Path.cwd()

# Loading the model
model = sklearn.load_model(f"{path}/models/main_model_v1.joblib")

# Creating the pipeline
pipeline = Pipeline([
    ('Scaler', StandardScaler()),
    ('Diagnosis', model)
])

# Defining the features
features = [
    "id", "radius_mean", "texture_mean", "perimeter_mean", "area_mean", "radius_se", "concave points_mean", "area_worst",
    "concavity_mean", "symmetry_mean", "fractal_dimension_mean", "perimeter_worst", "compactness_mean", "smoothness_mean",
    "perimeter_se", "area_se", "smoothness_se", "compactness_se", "concavity_se", "concave points_se", "symmetry_worst",
    "symmetry_se", "fractal_dimension_se", "radius_worst", "texture_worst",  "texture_se", "smoothness_worst",
    "compactness_worst", "concavity_worst", "concave points_worst", "fractal_dimension_worst"
]


# Data Validation
def validate_input(input_data: dict) -> bool:
    """
    Validate the input data before sending it to the predictive model.

    :param input_data: Dictionary containing data.
    :return: True if the data is valid, False otherwise.

    """

    # Check if all required keys are present in the JSON data
    if not all(key in input_data for key in features):
        return False

    # Check if the values are of the correct type
    for key in features:
        if not isinstance(input_data[key], float):
            return False

    # check for null values
    for key in features:
        if input_data[key] is None:
            return False

    # Return True if the data is valid
    return True


# Predict diagnosis and Confidence
def predict_diagnosis(validated_data: dict) -> dict:
    """
    Predict the diagnosis based on the input data.
    :param validated_data: Dictionary containing validated data.
    :return: Dictionary containing the predicted diagnosis and confidence score.
    """
    # Remove the id key from the validated data
    validated_data.pop("id")

    # Get the hard prediction
    prediction = pipeline.predict([validated_data])

    # Get the raw probability scores (Outputs: [[0.119, 0.881]])
    confidence_score = pipeline.predict_proba(validated_data)[0][1] * 100

    # Construct the dictionary with the prediction and confidence score
    prediction_result = {
        "diagnosis": "Malignant" if prediction == 1 else "Benign",
        "confidence": confidence_score,
    }

    # Return the prediction result
    return prediction_result


