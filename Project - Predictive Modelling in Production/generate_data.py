# Importing the required libraries
import time
import random
import requests
import pandas as pd
import psycopg2 as psql


# Function to generate simulated sensor data
def generate_sensor_data():
    temperature = random.uniform(20, 30).__round__(__ndigits=2)
    humidity = random.uniform(40, 60).__round__(__ndigits=2)
    sound = random.uniform(60, 80).__round__(__ndigits=2)
    return {'Temperature': temperature,
            'Humidity': humidity,
            'Sound': sound}

def send_request():
    url = 'http://127.0.0.1:5000/predict'
    response = requests.post(url, json=generate_sensor_data())


def store_sensor_data():
    # Getting the generated data
    data = generate_sensor_data()

    # statement to connect with the database
    conn = psql.connect(host="localhost", database="")
    cur = conn.cursor()

    # Setting the data appropriately for saving
    unit = {
        "Time": pd.Timestamp.now(),
        "Temperature": data["Temperature"],
        "Humidity": data["Humidity"],
        "Sound": data["Sound"]
    }

    # Saving the data into the database
    cur.execute()

    # Closing the connection once done with the transaction
    cur.close()

    return None


# Simulate continuous data stream
while True:
    sensor_data = generate_sensor_data()
    store_sensor_data()
    # Assuming you have a function to update BI dashboard data source
    # update_dashboard(sensor_data)
    time.sleep(10)  # Simulating 1-second interval for data stream
    print(sensor_data)
