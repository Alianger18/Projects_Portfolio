# Importing the required libraries
import pandas as pd
import mlflow


def pre_processing(dictionary):
    """
    Converts a dictionary into a 2D numpy array
    :param dictionary: a dictionary type
    :return: 2D numpy array
    """
    # Transform the dictionary into a list of values
    values = list(dictionary.values())

    # Expressing the values in 2D array
    input_data = [values]

    # Make the data available for use
    return input_data


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

