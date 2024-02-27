import time
import random
import pandas as pd

# Function to generate simulated sensor data
def generate_sensor_data():
    temperature = random.uniform(20, 30)
    humidity = random.uniform(40, 60)
    sound_volume = random.uniform(60, 80)
    timestamp = pd.Timestamp.now()
    return {'Timestamp': timestamp, 'Temperature': temperature, 'Humidity': humidity, 'SoundVolume': sound_volume}


# Simulate continuous data stream
while True:
    sensor_data = generate_sensor_data()
    # Assuming you have a function to update BI dashboard data source
    # update_dashboard(sensor_data)
    time.sleep(1)  # Simulating 1-second interval for data stream
