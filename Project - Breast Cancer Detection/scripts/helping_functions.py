# Import the required libraries
from pathlib import Path
import numpy as np
import joblib

# Creating the path for the model
path = Path.cwd()

# Loading the model
model = joblib.load(f"{path}/models/main_model_v1.joblib")

# Defining the input features
FEATURES = [
    "radius_mean", "texture_mean", "perimeter_mean", "area_mean", "smoothness_mean", "compactness_mean",
    "concavity_mean", "concave points_mean", "symmetry_mean", "fractal_dimension_mean", "radius_se",
    "texture_se", "perimeter_se", "area_se", "smoothness_se", "compactness_se", "concavity_se",
    "concave points_se", "symmetry_se", "fractal_dimension_se", "radius_worst",
    "texture_worst", "perimeter_worst", "area_worst", "smoothness_worst",
    "compactness_worst", "concavity_worst", "concave points_worst",
    "symmetry_worst", "fractal_dimension_worst"
]


# Data Validation
def validate_input(input_data: dict) -> bool:
    """
    Validate the input data before sending it to the predictive model.

    :param input_data: Dictionary containing data.
    :return: True if the data is valid, False otherwise.

    """

    # Check if all required keys are present in the JSON data
    if not all(key in input_data for key in FEATURES):
        return False

    # Check if the values are numeric (int or float) and not null
    for key in FEATURES:
        value = input_data[key]
        if value is None:
            return False
        if not isinstance(value, (int, float)):
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
    # Extract feature values in the correct order (without mutating the input)
    feature_values = [validated_data[key] for key in FEATURES]

    # Reshape into a 2D array for sklearn (1 sample, 30 features)
    input_array = np.array(feature_values).reshape(1, -1)

    # Get the hard prediction
    prediction = model.predict(input_array)[0]

    # Get the raw probability scores (Outputs: [[prob_benign, prob_malignant]])
    confidence_score = model.predict_proba(input_array)[0][1] * 100

    # Construct the dictionary with the prediction and confidence score
    prediction_result = {
        "diagnosis": "Malignant" if prediction == 1 else "Benign",
        "confidence": round(confidence_score, 2),
    }

    # Return the prediction result
    return prediction_result
