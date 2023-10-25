# Importing the pandas module
import pandas as pd

def show_habits_active(db):
    """
    Shows the records of active habits
    :param db: The database.
    :return: A dataframe.
    """
    # Retrieving data from the database
    cur = db.cursor()
    cur.execute("SELECT * FROM ACTIVE_HABITS")

    # Transforming data into a dataframe
    data = cur.fetchall()
    df = pd.DataFrame(data,
                      columns=['HABIT_ID', 'HABIT_NAME', 'PERIODICITY', 'LAST_INCREMENTATION_DATE', 'STREAK_ACTIVE']
                      ).set_index("HABIT_ID")

    return df

def show_habits_broken(db):
    """
    Shows the records of broken habits
    :param db: The database.
    :return: a dataframe.
    """
    # Starting a cursor object
    cur = db.cursor()

    # Retrieving data from the database
    cur.execute("SELECT * FROM BROKEN_HABITS")

    # Transforming data into a dataframe
    data = cur.fetchall()
    df = pd.DataFrame(data,
                      columns=['HABIT_ID', 'HABIT_NAME', 'PERIODICITY', 'START_DATE', 'END_DATE', 'STREAK_ENDED']
                      ).set_index("HABIT_ID")

    return df

def show_habits_with_same_periodicity(db, habit_periodicity):
    """
    Based on a specified periodicity, shows the active habits with the same periodicity.
    :param db: The database.
    :param habit_periodicity: The periodicity of this habit
    :return: a dataframe.
    """
    # Retrieving the dataframe
    habit_data = show_habits_active(db)

    # Returning only the rows with the habit_periodicity specified
    if habit_periodicity in habit_data["PERIODICITY"].tolist():
        df_periodicity = habit_data[habit_data["PERIODICITY"] == habit_periodicity]
        return df_periodicity
    else:
        # In case the specified periodicity doesn't belong to a habit, this line is to handle this case.
        print("Sorry, there are currently no habits with the specified periodicity.")

def show_longest_streak(db):
    """
    Shows the longest streak ever made by the user.
    :param db: The database.
    :return: list
    """
    # Setting basic variables
    active_habits = show_habits_active(db)
    broken_habits = show_habits_broken(db)

    # Retrieving the longest streak for both active and broken habits
    longest_streak_active = active_habits.loc[active_habits["STREAK_ACTIVE"].idxmax()]
    longest_streak_broken = broken_habits.loc[broken_habits["STREAK_ENDED"].idxmax()]

    # Performing the evaluation
    if longest_streak_active["STREAK_ACTIVE"] > longest_streak_broken["STREAK_ENDED"]:
        results = [longest_streak_active["HABIT_NAME"], longest_streak_active["PERIODICITY"],
                   longest_streak_active["STREAK_ACTIVE"]
                   ]
    else:
        results = [longest_streak_broken["HABIT_NAME"], longest_streak_broken["PERIODICITY"],
                   longest_streak_broken["STREAK_ENDED"]
                   ]
    # Showing the end results
    return results

def show_longest_streak_of_a_habit(db, habit_name):
    """
    Shows the longest streak ever made by the user by sticking to the habit.
    :param db: The database.
    :param habit_name: The name of this habit
    :return: an integer.
    """
    # Setting basic variables
    cur = db.cursor()

    active_habit = cur.execute(
        "SELECT MAX(STREAK_ACTIVE) FROM ACTIVE_HABITS WHERE HABIT_NAME=?", (habit_name,)).fetchone()[0]
    broken_habit = cur.execute(
        "SELECT MAX(STREAK_ENDED) FROM BROKEN_HABITS WHERE HABIT_NAME=?", (habit_name,)).fetchone()[0]

    # Checking if there are any records
    if not active_habit and not broken_habit:
        return 0

    # Setting the longest streak to be the greater value between the two
    longest_streak = max(active_habit or 0, broken_habit or 0)

    # Return the longest streak
    if longest_streak == 0:
        print('This habit has no streak.')
    else:
        return longest_streak
