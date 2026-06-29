# Importing the required libraries
import requests
import random
import time


# --- Centroid profiles for controlled sample generation ------------------
# Mean feature values for benign cases in the Wisconsin Breast Cancer Dataset
BENIGN_CENTROID = {
    "radius_mean": 12.15, "texture_mean": 17.91, "perimeter_mean": 78.08,
    "area_mean": 462.79, "smoothness_mean": 0.0925, "compactness_mean": 0.0801,
    "concavity_mean": 0.0461, "concave points_mean": 0.0257, "symmetry_mean": 0.1742,
    "fractal_dimension_mean": 0.0629, "radius_se": 0.2840, "texture_se": 1.2200,
    "perimeter_se": 2.0000, "area_se": 21.14, "smoothness_se": 0.0071,
    "compactness_se": 0.0213, "concavity_se": 0.0260, "concave points_se": 0.0091,
    "symmetry_se": 0.0206, "fractal_dimension_se": 0.0037, "radius_worst": 13.38,
    "texture_worst": 23.52, "perimeter_worst": 87.01, "area_worst": 558.90,
    "smoothness_worst": 0.1250, "compactness_worst": 0.1827, "concavity_worst": 0.1663,
    "concave points_worst": 0.0742, "symmetry_worst": 0.2701, "fractal_dimension_worst": 0.0795
}

# Mean feature values for malignant cases in the Wisconsin Breast Cancer Dataset
MALIGNANT_CENTROID = {
    "radius_mean": 17.46, "texture_mean": 21.60, "perimeter_mean": 115.37,
    "area_mean": 978.38, "smoothness_mean": 0.1029, "compactness_mean": 0.1454,
    "concavity_mean": 0.1607, "concave points_mean": 0.0880, "symmetry_mean": 0.1929,
    "fractal_dimension_mean": 0.0627, "radius_se": 0.6090, "texture_se": 1.2100,
    "perimeter_se": 4.3200, "area_se": 72.67, "smoothness_se": 0.0071,
    "compactness_se": 0.0321, "concavity_se": 0.0418, "concave points_se": 0.0152,
    "symmetry_se": 0.0206, "fractal_dimension_se": 0.0040, "radius_worst": 21.13,
    "texture_worst": 29.32, "perimeter_worst": 141.37, "area_worst": 1422.29,
    "smoothness_worst": 0.1449, "compactness_worst": 0.3749, "concavity_worst": 0.4506,
    "concave points_worst": 0.1822, "symmetry_worst": 0.3234, "fractal_dimension_worst": 0.0916
}
# -------------------------------------------------------------------------


# --- Sample patient data for realistic records ---------------------------
FIRST_NAMES = [
    "Catherine", "Marie", "Sarah", "Fatima", "Elena", "Amina", "Sophie",
    "Lina", "Nadia", "Olivia", "Hannah", "Grace", "Leila", "Priya",
    "Yuki", "Rosa", "Clara", "Diana", "Layla", "Ines", "Hana", "Zara",
    "Aisha", "Julia", "Emma", "Victoria", "Samira", "Mona", "Reem", "Dina",
]

LAST_NAMES = [
    "Dupont", "Al-Rashid", "Nakamura", "Petrov", "Garcia", "Chen",
    "Okonkwo", "Johansson", "Kim", "Müller", "Fernandez", "Barir",
    "Hassan", "Moreau", "Singh", "Tanaka", "Weber", "Rossi",
    "Larsen", "Park", "Ali", "Durand", "Torres", "Nguyen", "Patel",
]
# -------------------------------------------------------------------------


# 1-minute interval between data stream requests
INTERVAL_SECONDS = 60


def generate_sample() -> dict:
    """
    Generate a realistic set of 30 features by interpolating between
    the known benign and malignant centroids with controlled Gaussian noise.

    A random mixing ratio `t` determines where the sample falls on the
    benign–malignant spectrum:
        t ≈ 0.0  → strongly benign
        t ≈ 0.5  → borderline / ambiguous
        t ≈ 1.0  → strongly malignant

    The ratio is drawn uniformly from [0.15, 0.95] so the model produces
    a healthy spread of benign, borderline, and malignant predictions
    with realistic (non-100%) confidence scores.
    """
    # Draw a random mixing ratio — uniform across the spectrum
    t = random.uniform(0.15, 0.95)

    features = {}
    for feature in BENIGN_CENTROID:
        benign_val = BENIGN_CENTROID[feature]
        malignant_val = MALIGNANT_CENTROID[feature]

        # Linear interpolation between centroids
        interpolated = benign_val * (1 - t) + malignant_val * t

        # Add small Gaussian noise (5% of feature range) for realism
        feature_range = abs(malignant_val - benign_val)
        noise = random.gauss(0, feature_range * 0.05)
        value = interpolated + noise

        # Ensure non-negative values
        features[feature] = round(max(0.0, value), 6)

    return features


def generate_patient_info() -> dict:
    """Generate random patient demographics."""
    return {
        "patient_name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
        "patient_age": random.randint(28, 82),
    }


if __name__ == "__main__":

    while True:
        # Generate a realistic sample using centroid interpolation
        data = generate_sample()

        # Add patient demographics
        data.update(generate_patient_info())

        try:
            # Sending the data stream to the predict endpoint
            response = requests.post('http://127.0.0.1:5000/predict', json=data)
            result = response.json()
            print(
                f"[{time.strftime('%H:%M:%S')}] "
                f"Patient: {data['patient_name']} (Age {data['patient_age']}) | "
                f"Status: {response.status_code} | "
                f"Diagnosis: {result.get('diagnosis', 'N/A')} | "
                f"Confidence: {result.get('confidence', 'N/A')}%"
            )
        except requests.exceptions.ConnectionError:
            print(f"[{time.strftime('%H:%M:%S')}] Connection failed. Is the Flask server running?")

        # Wait before the next request
        time.sleep(INTERVAL_SECONDS)
