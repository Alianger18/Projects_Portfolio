# Importing the required libraries
import pandas as pd
import numpy as np
import mlflow

def pre_processing(json_file):
    """
    Converts a json file into a 2D numpy array

    Args :
    json_file (dictionary): Dictionary of measurements containing
    sound, temperature, and humidity data.

    Returns :
    two-dimensional numpy array.
    """
    # Transform the dictionary into a list of values
    values = list(json_file.values())

    # Expressing the values in 2D array
    input_data = [values]

    # Make the data available for use
    return input_data

def validation(data) -> bool:
    """
    Validates the input data.

    Args:
    - data (list): List of measurements where each measurement
    is a list containing sound, temperature, and humidity data.

    Returns:
    - bool: True if the data is valid, False otherwise.
    """
    # Getting data
    sound = data[0][0]
    temperature = data[0][1]
    humidity = data[0][2]

    # Check if each input is within normal ranges for each measurement
    if 85 >= sound >= 60 >= humidity >= 40 and 68 <= temperature <= 86:
        return True  # If all checks pass for all measurements, return True

    else:
        return False  # False, otherwise

def check_experiment(prospected_experiment_name):
    """
    Check the experiment's appropriate name and number
    :param prospected_experiment_name: suggested experiment name
    :return: the appropriate name and number of the experiment
    """
    # Get existing experiments with the same base name
    experiments = [experiment.name for experiment in mlflow.search_experiments() if
                   experiment.name != 'Default' and experiment.name != 'Training prospected models']

    # Determine the next experiment number
    experiment_number = len(experiments) + 1

    # Create the new experiment name
    experiment_name = f"Running {prospected_experiment_name} model - Experiment N°{experiment_number}"

    # Create the experiment
    return experiment_name

def fetch_data(connection):
    """
    Fetch data from the database and return it as a pandas dataframe
    :param connection: a database connection
    :return: pandas dataframe
    """
    # Query the data
    query = "SELECT * FROM Records ORDER BY TIMESTAMP DESC LIMIT 16"

    # Store the data into a pandas dataframe
    df = pd.read_sql(query, connection)

    # Return the dataframe
    return df

def store_data(database, storage_model, input_measurements, output_score):

    """
    Stores the input/output data in a database.

    Args:
    - database: a sqlalchemy database
    - storage_model: a sqlalchemy database model
    - input_measurements: a list of measurements where each measurement is containing sound, temperature, and humidity.
    - output_score: the output score of the model.

    Returns:
    - None.
    """
    # Adjusting values
    sound = input_measurements[0][0]
    temperature = input_measurements[0][1]
    humidity = input_measurements[0][2]
    score = np.round(output_score[0], decimals=2)

    # Creating a record using these values
    record = storage_model(sound=sound, temperature=temperature, humidity=humidity, score=score)

    # Add the record to the database
    database.session.add(record)
    database.session.commit()

    return None
