# Importing necessary functions and modules from other files
from tracker import Tracker
from analysis import show_habits_active
import datetime
import sqlite3


# Designing the functions
def get_db(name="main.db"):
    """
    Create a connection to a SQLite database.
    :param name: The name of the database.
    :return: A database file.
    """
    # Initiating a database connection
    db = sqlite3.connect(name)

    # Creating the tables in the database
    create_tables(db)

    return db

def create_tables(db):
    """
    Creates 3 tables to store data.\n
    ACTIVE_HABITS: Holds the information about the active habits.\n
    BROKEN_HABITS: Holds the information about the broken habits.\n
    TRACKING_HABITS: Holds information about any event happened to habits. e.g. incrementation, deletion, or creation.
    :param db: a database.
    :return: None.
    """
    # Creating a cursor object
    cur = db.cursor()

    # Loading the script containing the queries to create tables
    with open('schema.sql', 'r') as file:
        schema = file.read()
        file.close()

    # Running the script
    cur.executescript(schema)

    # Shutdown the cursor object
    cur.close()

def add_habit(db, habit_name, habit_periodicity):
    """
    Based on the Tracker class, this method adds a habit to the database.
    :param db: the database
    :param habit_name: The name of this habit
    :param habit_periodicity: The periodicity of this habit
    :return: message confirming the successful execution of the operation is displayed
    """

    # Creating a Tracker object
    habit = Tracker(habit_name, habit_periodicity)
    values = habit.details

    # Starting a new cursor object
    cur = db.cursor()

    try:
        # Updating the database
        cur.execute("INSERT INTO ACTIVE_HABITS VALUES (?, ?, ?, ?, ?)",
                    (values[0], values[1], values[2], values[3], values[4]))

        # Getting the latest operation ID from the TRACKING_HABITS table
        max_operation_id = cur.execute("SELECT MAX(OPERATION_ID) FROM TRACKING_HABITS").fetchone()[0]

        # Setting the adequate value of operation_id
        operation_id = 1 if max_operation_id is None else max_operation_id + 1

        # Running Query to update values in the tracking habits table
        cur.execute("INSERT INTO TRACKING_HABITS (OPERATION_ID, HABIT_ID, EVENT_NAME, EVENT_DATE)"
                    "VALUES (?, ?, ?, ?)",
                    (operation_id, values[0], "CREATION", datetime.datetime.now().strftime('%Y-%m-%d %H:%M')))

        # Committing the commands to our database
        db.commit()

        # Displaying a message of successful execution of the operation
        return "Successfully created."

    except Exception as e:
        # Handle exceptions
        print(f"An error occurred: {e}")
        db.rollback()

    # Shutdown the cursor object
    finally:
        cur.close()

def edit_habit(db, habit_id, column, new_value):
    """
    Edit the habit's name and periodicity.
    :param db: Database
    :param habit_id: The unique id of the habit
    :param column: It can be either 'Habit_name' or 'Periodicity'
    :param new_value: The value you want to update to
    :return: message confirming the successful execution of the operation is displayed
    """
    # Starting a cursor object
    cur = db.cursor()

    try:
        # Running Query to update values in the active habits table
        cur.execute(f"UPDATE ACTIVE_HABITS SET {column} = '{new_value}' WHERE HABIT_ID = {habit_id};")

        # Running Query to update values in the tracking habits table
        operation_id = cur.execute("SELECT MAX(OPERATION_ID) FROM TRACKING_HABITS").fetchone()[0] + 1

        cur.execute("INSERT INTO TRACKING_HABITS (OPERATION_ID, HABIT_ID, EVENT_NAME, EVENT_DATE)"
                    "VALUES (?, ?, ?, ?)",
                    (operation_id, habit_id, "EDITION", datetime.datetime.now().strftime('%Y-%m-%d %H:%M')))

        # Committing the changes to the database
        db.commit()

        # Displaying a message of successful execution of the operation
        return "Successfully edited."

    except Exception as e:
        # Handle exceptions
        print(f"An error occurred: {e}")
        db.rollback()

    # Shutdown the cursor object
    finally:
        cur.close()

def increment_habit(db, habit_id):
    """
    Increment the streak of the habit by 1
    :param db: Database
    :param habit_id: The unique id of the habit
    :return: message confirming the successful execution of the operation is displayed
    """
    # Starting a cursor object
    cur = db.cursor()

    try:
        # Running Query to update values in the active habits table
        cur.execute("UPDATE ACTIVE_HABITS "
                    "SET STREAK_ACTIVE = STREAK_ACTIVE + 1, LAST_INCREMENTATION_DATE = ? "
                    "WHERE HABIT_ID = ?", (datetime.date.today(), habit_id))

        # Running Query to update values in the tracking habits table
        operation_id = cur.execute("SELECT MAX(OPERATION_ID) FROM TRACKING_HABITS").fetchone()[0] + 1

        cur.execute("INSERT INTO TRACKING_HABITS (OPERATION_ID, HABIT_ID, EVENT_NAME, EVENT_DATE)"
                    "VALUES (?, ?, ?, ?)",
                    (operation_id, habit_id, "INCREMENTATION", datetime.datetime.now().strftime('%Y-%m-%d %H:%M')))

        # Committing the changes to the database
        db.commit()

        # Displaying a message of successful execution of the operation
        return "Successfully incremented."

    except Exception as e:
        # Handle exceptions
        print(f"An error occurred: {e}")
        db.rollback()

    # Shutdown the cursor object
    finally:
        cur.close()

def reset_habit(db, habit_id):
    """
    Reset the streak of the habit to 0
    :param db: Database
    :param habit_id: The unique id of the habit
    :return: message confirming the successful execution of the operation is displayed
    """
    # Starting a cursor object
    cur = db.cursor()

    try:
        # Running Query to update values in the active habits table
        cur.execute(f"UPDATE ACTIVE_HABITS SET STREAK_ACTIVE = 0 WHERE HABIT_ID = {habit_id}")

        # Running Query to update values in the tracking habits table
        operation_id = cur.execute("SELECT MAX(OPERATION_ID) FROM TRACKING_HABITS").fetchone()[0] + 1

        cur.execute("INSERT INTO TRACKING_HABITS (OPERATION_ID, HABIT_ID, EVENT_NAME, EVENT_DATE)"
                    "VALUES (?, ?, ?, ?)",
                    (operation_id, habit_id, "RESET", datetime.datetime.now().strftime('%Y-%m-%d %H:%M')))

        # Committing the changes to the database
        db.commit()

        # Displaying a message of successful execution of the operation
        return "Successfully reset."

    except Exception as e:
        # Handle exceptions
        print(f"An error occurred: {e}")
        db.rollback()

    # Shutdown the cursor object
    finally:
        cur.close()

def delete_habit(db, habit_id, broken=False):
    """
    Delete a habit from the active habits table and move it to the broken habits table.
    :param db: database.
    :param habit_id:
    :param broken: Set by default to False, setting it to True changes
    how the operation is tracked in the tracking habits table.
    :return: message confirming the successful execution of the operation is displayed
    """
    # Starting a cursor object
    cur = db.cursor()

    try:
        # Retrieving the start date of the habit, which indicates the first time the habit was incremented by the user
        cur.execute("SELECT MIN(EVENT_DATE) FROM TRACKING_HABITS "
                    "WHERE HABIT_ID = ? AND EVENT_NAME = 'INCREMENTATION'", (habit_id,))
        start_date = cur.fetchone()[0]

        # Retrieving the end date of the habit, which indicates the last time the habit was incremented by the user
        cur.execute("SELECT MAX(EVENT_DATE) FROM TRACKING_HABITS "
                    "WHERE HABIT_ID = ? AND EVENT_NAME = 'INCREMENTATION'", (habit_id,))
        end_date = cur.fetchone()[0]

        # Backing-up data from the active habits table
        cur.execute("SELECT * FROM ACTIVE_HABITS WHERE HABIT_ID = ?", (habit_id,))
        data = cur.fetchone()

        # Deleting the data from the active habits table
        cur.execute("DELETE FROM ACTIVE_HABITS WHERE HABIT_ID = ?", (habit_id,))

        # Inserting data into the broken habits table
        cur.execute("INSERT INTO BROKEN_HABITS VALUES (?, ?, ?, ?, ?, ?)",
                    (data[0], data[1], data[2], start_date, end_date, data[4]))

        # Updating the habits tracking table depending on the case
        if broken:
            operation_id = cur.execute("SELECT MAX(OPERATION_ID) FROM TRACKING_HABITS").fetchone()[0] + 1

            cur.execute("INSERT INTO TRACKING_HABITS (OPERATION_ID, HABIT_ID, EVENT_NAME, EVENT_DATE)"
                        "VALUES (?, ?, ?, ?)",
                        (operation_id, habit_id, "BROKEN", datetime.datetime.now().strftime('%Y-%m-%d %H:%M')))
            message = f"{data[1]} is broken due to not being incremented on time."
        else:
            operation_id = cur.execute("SELECT MAX(OPERATION_ID) FROM TRACKING_HABITS").fetchone()[0] + 1

            cur.execute("INSERT INTO TRACKING_HABITS (OPERATION_ID, HABIT_ID, EVENT_NAME, EVENT_DATE)"
                        "VALUES (?, ?, ?, ?)",
                        (operation_id, habit_id, "DELETION", datetime.datetime.now().strftime('%Y-%m-%d %H:%M')))
            message = "Successfully deleted."

        # Committing the changes to the database
        db.commit()

        # Print the adequate message
        return message

    except Exception as e:
        # Handle exceptions
        print(f"An error occurred: {e}")
        db.rollback()

    # Shutting down the cursor object
    finally:
        cur.close()

def habit_breaking_check(db):
    """
    This function break habits that weren't incremented in time and delete them.
    :param db: The database
    :return: None
    """
    # Preparing  data
    df = show_habits_active(db).reset_index()

    # Designing our functions
    def quarter_range(date):
        """
        Determine of the starting date and end date of the quarter.
        :param date: the desired date.
        :return: list.
        """
        # Sets the quarter range to the first quarter
        # if the date is sometime between 01/01 and 31/03 of the same year
        if date.month in range(1, 4):
            start_quarter = datetime.date(datetime.date.today().year, 1, 1)
            end_quarter = datetime.date(datetime.date.today().year, 3, 31)
            quarter = [start_quarter, end_quarter]
            return quarter

        # Sets the quarter range to the second quarter
        # if the date is sometime between 01/04 and 30/06 of the same year
        elif date.month in range(4, 7):
            start_quarter = datetime.date(datetime.date.today().year, 4, 1)
            end_quarter = datetime.date(datetime.date.today().year, 6, 30)
            quarter = [start_quarter, end_quarter]
            return quarter

        # Sets the quarter range to the third quarter
        # if the date is sometime between 01/07 and 30/09 of the same year
        elif date.month in range(7, 10):
            start_quarter = datetime.date(datetime.date.today().year, 7, 1)
            end_quarter = datetime.date(datetime.date.today().year, 9, 30)
            quarter = [start_quarter, end_quarter]
            return quarter

        # Sets the quarter range to the fourth quarter
        # if the date is sometime between 01/10 and 31/12 of the same year
        else:
            start_quarter = datetime.date(datetime.date.today().year, 10, 1)
            end_quarter = datetime.date(datetime.date.today().year, 12, 31)
            quarter = [start_quarter, end_quarter]
            return quarter

    def semester_range(date):
        """
        Determine of the starting date and end date of the semester.
        :param date: the desired date.
        :return: list.
        """
        # Sets the semester range to the first semester
        # if the date is sometime between 01/01 and 30/06 of the same year
        if date.month in range(1, 7):
            start_semester = datetime.date(datetime.date.today().year, 1, 1)
            end_semester = datetime.date(datetime.date.today().year, 6, 30)
            semester = [start_semester, end_semester]
            return semester

        # Sets the semester range to the second semester
        # if the date is sometime between 01/07 and 31/12 of the same year
        else:
            start_semester = datetime.date(datetime.date.today().year, 7, 1)
            end_semester = datetime.date(datetime.date.today().year, 12, 31)
            semester = [start_semester, end_semester]
            return semester

    # Running our check
    for row in df.itertuples():
        # Setting some basic variables
        habit_id = row[1]
        periodicity = row[3]
        last_incrementation_date = datetime.date.fromisoformat(row[4])
        year, week_num, day_of_week = datetime.date.today().isocalendar()

        if periodicity == 'Daily':
            # if this habit isn't last_incrementation_date wasn't today, then it's broken
            if not last_incrementation_date == datetime.date.today():
                delete_habit(db, habit_id, broken=True)

        elif periodicity == 'Weekly':
            # Specifying the date range of the week starting from Monday and ending by Sunday
            start_date = datetime.date.fromisocalendar(year, week_num, 1)
            end_date = datetime.date.fromisocalendar(year, week_num, 7)

            # if this habit isn't last_incrementation_date wasn't in the range, then it's broken
            if not start_date <= last_incrementation_date <= end_date:
                delete_habit(db, habit_id, broken=True)

        elif periodicity == 'Twice a month':
            # Specifying the date range of the 2 weeks
            start_date = datetime.date.fromisocalendar(year, week_num, 1)
            end_date = datetime.date.fromisocalendar(year, week_num+1, 7)

            # if this habit isn't last_incrementation_date wasn't in the range, then it's broken
            if not start_date <= last_incrementation_date <= end_date:
                delete_habit(db, habit_id, broken=True)

        elif periodicity == 'Monthly':
            # if this habit isn't last_incrementation_date wasn't this month, then it's broken
            if not last_incrementation_date.month == datetime.date.today().month:
                delete_habit(db, habit_id, broken=True)

        elif periodicity == 'Quarterly':
            # Specifying conditions of the range
            condition_1 = quarter_range(last_incrementation_date)[0] <= datetime.date.today()
            condition_2 = datetime.date.today() <= quarter_range(last_incrementation_date)[1]

            # if this habit isn't last_incrementation_date wasn't in the range, then it's broken
            if not condition_1 and condition_2:
                delete_habit(db, habit_id, broken=True)

        elif periodicity == 'Twice a year':
            # Specifying conditions of the range
            condition_1 = semester_range(last_incrementation_date)[0] <= datetime.date.today()
            condition_2 = datetime.date.today() <= semester_range(last_incrementation_date)[1]

            # if this habit isn't last_incrementation_date wasn't in the range, then it's broken
            if not condition_1 and condition_2:
                delete_habit(db, habit_id, broken=True)

        else:
            # if this habit isn't last_incrementation_date wasn't in this year, then it's broken
            if not last_incrementation_date.year == datetime.date.today().year:
                delete_habit(db, habit_id, broken=True)
