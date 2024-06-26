# Importing the required libraries
import requests
import random
import time

# Initial values for sound, temperature, and humidity
sound = 70
temperature = 76
humidity = 50

while True:
    # Generate dummy data with one unit variation from the last measurement
    sound += random.choice([-1, 1])
    temperature += random.choice([-1, 1])
    humidity += random.choice([-1, 1])

    # Construct the data dictionary
    data = {
        'sound': sound,
        'temperature': temperature,
        'humidity': humidity
    }

    # Sending the data stream
    requests.post('http://127.0.0.1:5000/predict', json=data)

    # Adjust the interval as needed
    time.sleep(1)
