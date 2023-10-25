# Importing the datetime module
import datetime

# Defining a class named Tracker
class Tracker:

    # Setting the count of habits created
    count = 0

    # Defining the constructor for the Tracker class
    def __init__(self, name, periodicity):
        """
        Create habits based on simple parameters in order to create class objects and store them
        in a separate list with a unified order, a count variable is also incremented everytime
        a habit has been created.
        :param name: The name of the habit
        :param periodicity: The frequency of this habit
        """

        # Incrementing the count variable to keep track of the number of habits created
        Tracker.count += 1

        # Setting the attributes of the habit object
        self.habit_id = Tracker.count  # A unique identifier for the habit
        self.name = name  # The name of the habit
        self.periodicity = periodicity  # The frequency of the habit
        self.start_date = datetime.date.today()  # The date on which the habit was created
        self.streak_active = 0  # The current streak of the habit

        # This attribute hold every detail related to a given habit
        # It's initialized as a list containing the habit's ID, name, periodicity, start date, and streak activity
        self.details = [self.habit_id, self.name, self.periodicity, self.start_date, self.streak_active]
