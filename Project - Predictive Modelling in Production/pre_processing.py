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
