# Importing the required libraries
import mlflow
import subprocess


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


def run_gunicorn():
    # Define the Gunicorn command
    gunicorn_command = [
        'gunicorn',
        '-w', '4',            # Number of worker processes
        '-b', 'dashboard.vestas.com:8000',  # Bind address and port
        'main:app'             # Flask application module and instance
    ]

    # Run Gunicorn using subprocess
    subprocess.Popen(gunicorn_command)

