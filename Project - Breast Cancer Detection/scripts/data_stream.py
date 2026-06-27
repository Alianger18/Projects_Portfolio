# Importing the required libraries
import requests
import random
import time

# Realistic value ranges for each feature (min, max) from data_v1.0.0.csv
FEATURE_RANGES = {
    "radius_mean": (7, 28),
    "texture_mean": (10, 39),
    "perimeter_mean": (44, 188),
    "area_mean": (145, 2501),
    "smoothness_mean": (0.05263, 0.1634),
    "compactness_mean": (0.01938, 0.3454),
    "concavity_mean": (0.0, 0.4268),
    "concave points_mean": (0.0, 0.2012),
    "symmetry_mean": (0.106, 0.304),
    "fractal_dimension_mean": (0.04996, 0.09744),
    "radius_se": (0.1115, 2.873),
    "texture_se": (0.3602, 4.885),
    "perimeter_se": (0.757, 21.98),
    "area_se": (6.802, 542.2),
    "smoothness_se": (0.001713, 0.03113),
    "compactness_se": (0.002252, 0.1354),
    "concavity_se": (0.0, 0.396),
    "concave points_se": (0.0, 0.05279),
    "symmetry_se": (0.007882, 0.07895),
    "fractal_dimension_se": (0.0008948, 0.02984),
    "radius_worst": (7.93, 36.04),
    "texture_worst": (12.02, 49.54),
    "perimeter_worst": (50.41, 251.2),
    "area_worst": (185.2, 4254.0),
    "smoothness_worst": (0.07117, 0.2226),
    "compactness_worst": (0.02729, 1.058),
    "concavity_worst": (0.0, 1.252),
    "concave points_worst": (0.0, 0.291),
    "symmetry_worst": (0.1565, 0.6638),
    "fractal_dimension_worst": (0.05504, 0.2075),
}

# 5-minute interval between data stream requests
INTERVAL_SECONDS = 60

def generate_sample() -> dict:
    """Generate a random sample with realistic feature values."""
    return {
        feature: round(random.uniform(low, high), 6)
        for feature, (low, high) in FEATURE_RANGES.items()
    }


if __name__ == "__main__":

    while True:
        # Generate a random sample within realistic ranges
        data = generate_sample()

        try:
            # Sending the data stream to the predict endpoint
            response = requests.post('http://127.0.0.1:5000/predict', json=data)
            print(f"[{time.strftime('%H:%M:%S')}] Status: {response.status_code} | Response: {response.json()}")
        except requests.exceptions.ConnectionError:
            print(f"[{time.strftime('%H:%M:%S')}] Connection failed. Is the Flask server running?")

        # Wait 5 minutes before the next request
        time.sleep(INTERVAL_SECONDS)
