# Importing necessary functions and modules from other files
from analysis import show_habits_with_same_periodicity, show_longest_streak_of_a_habit, show_longest_streak
from analysis import show_habits_active, show_habits_broken
from db import get_db
from tracker import Tracker
import datetime
import os

# Defining a class TestTracker
class TestTracker:

    def setup_method(self):
        """
        This methode cleans the database in order to perform the tests on the test data
        :return: None
        """
        # Creating the test database
        self.db = get_db("test.db")

        # Creating a cursor object
        cur = self.db.cursor()

        # Loading the script containing the queries of user data of 4-weeks
        with open('user_data.sql', 'r') as file:
            user_data = file.read()
            file.close()

        # Running the script
        cur.executescript(user_data)

        # Shutdown the cursor object
        cur.close()

        # Resetting variable to 15, because 15 habits were already created
        Tracker.count = 15

    def teardown_method(self):
        """
        This method clean the resources after each test
        :return: None
        """
        # Resetting the variables
        Tracker.count = 0
        self.db.execute("DELETE FROM ACTIVE_HABITS")
        self.db.execute("DELETE FROM BROKEN_HABITS")
        self.db.execute("DELETE FROM TRACKING_HABITS")

        # Commit and close the database connection
        self.db.commit()
        self.db.close()

        # Remove the database file
        os.remove("test.db")

    def test_analysis(self):
        # 10 habits were created, 2 were deleted
        # The test's integrity could be examined by editing the teardown_method and inspecting the test database
        # Testing the existence of the active habits
        assert show_habits_active(self.db).shape[0] == 11

        # Testing the existence of the broken habits
        assert show_habits_broken(self.db).shape[0] == 4

        # Testing the existence of 2 habits with the same periodicity
        assert show_habits_with_same_periodicity(self.db, "Weekly").shape[0] == 3

        # Testing the longest streak made for 'Go sleep early'
        assert show_longest_streak_of_a_habit(self.db, "Go sleep early") == 156

        # Testing the longest streak ever made
        assert show_longest_streak(self.db) == ["Work", "Daily", 161]

    def test_tracker(self):
        tracker = Tracker("Habit", "Periodicity")
        # Because we created 10 habits before, the count parameter responsible for assigning the habits their IDs
        # In the Tracker class, will refer to 11 instead of 1.
        assert tracker.habit_id == 16
        assert tracker.name == "Habit"
        assert tracker.periodicity == "Periodicity"
        assert tracker.start_date == datetime.date.today()
        assert tracker.streak_active == 0
        assert tracker.details == [tracker.habit_id, tracker.name, tracker.periodicity,
                                   tracker.start_date, tracker.streak_active]
