# Importing necessary functions and modules from other files
from db import get_db, habit_breaking_check
from db import add_habit, increment_habit, edit_habit, reset_habit, delete_habit
from analysis import show_habits_with_same_periodicity, show_longest_streak_of_a_habit, show_longest_streak
from analysis import show_habits_active, show_habits_broken
import questionary

# Designing the function
def cli():
    # Retrieving database connection
    db = get_db()

    # Checking if any habits are overdue
    habit_breaking_check(db)

    # Printing a welcome message
    print("=========================================================================")
    print("|                                                                       |")
    print("|                                Betto                                  |")
    print("|                  Your way to greatness starts here                    |")
    print("|                                                                       |")
    print("=========================================================================")

    while True:
        # Displaying a menu to the user and prompting for a choice
        choice = questionary.select('What do you want to do ?',
                                    choices=["Analyze", "Create", "Edit", "Increment", "Reset", "Delete", "Exit"]
                                    ).ask()

        if choice == "Analyze":
            stick = False

            while not stick:
                # Displaying a submenu to the user and prompting for a choice
                user_choice = questionary.select("What would you like to see?",
                                                 choices=['Show active habits',
                                                          'Show broken habits',
                                                          'Show habits with the same periodicity',
                                                          'Show the longest streak of a habit',
                                                          'Show the longest streak ever made',
                                                          'Back']
                                                 ).ask()

                if user_choice == 'Show active habits':
                    # Showing active habits
                    print(show_habits_active(db))

                    # Prompting the user if they want to do anything else
                    question = questionary.confirm("Anything else").ask()

                    # if the user quits, prints a message and breaks the loop
                    if not question:
                        break

                elif user_choice == 'Show broken habits':
                    # Showing habits that have been broken in the past
                    print(show_habits_broken(db))

                    # Prompting the user if they want to do anything else
                    question = questionary.confirm("Anything else").ask()

                    # if the user quits, prints a message and breaks the loop
                    if not question:
                        break

                elif user_choice == 'Show habits with the same periodicity':
                    # Prompting the user to choose a periodicity and showing habits with that periodicity
                    periodicity = questionary.select("Choose the periodicity :",
                                                     choices=["Daily", "Weekly", "Twice a month", "Monthly",
                                                              "Quarterly", "Twice a year", "Yearly"]
                                                     ).ask()

                    # Shows all the habits with the same periodicity in the database
                    show_habits_with_same_periodicity(db, periodicity)

                    # Prompting the user if they want to do anything else
                    question = questionary.confirm("Anything else").ask()

                    # if the user quits, prints a message and breaks the loop
                    if not question:
                        break

                elif user_choice == 'Show the longest streak of a habit':
                    # Preparing the dataframe
                    data = show_habits_active(db)

                    # Prompting the user to choose a habit and showing the longest streak for that habit
                    habit_name = questionary.select("What's the name of this habit",
                                                    choices=list(data['HABIT_NAME'].unique())
                                                    ).ask()

                    # Show the longest streak the user has reached with this habit
                    print(show_longest_streak_of_a_habit(db, habit_name))

                    # Prompting the user if they want to do anything else
                    question = questionary.confirm("Anything else").ask()

                    # if the user quits, prints a message and breaks the loop
                    if not question:
                        break

                elif user_choice == 'Show the longest streak ever made':
                    # Showing the longest streak for any habit
                    print(show_longest_streak(db))

                    # Prompting the user if they want to do anything else
                    question = questionary.confirm("Anything else").ask()

                    # if the user quits, prints a message and breaks the loop
                    if not question:
                        break

                else:
                    stick = True

        elif choice == "Create":
            sub_choice = questionary.select("Choose a habit, you can create a new habit by choosing Custom.",
                                            choices=["Drink water", "Go sleep early",
                                                     "Work", "Meditation", "Workout",
                                                     "Custom"
                                                     ]
                                            ).ask()

            if sub_choice == "Custom":
                # Ask the user for the name and periodicity of the new habit they want to create
                name = questionary.text("What is the name of this habit:").ask()
                periodicity = questionary.select("How frequent are you willing to do this habit?",
                                                 choices=["Daily", "Weekly", "Twice a month",
                                                          "Monthly", "Quarterly", "Twice a year", "Yearly"]
                                                 ).ask()

                # Call the add_habit function to create the new habit in the database
                add_habit(db, name, periodicity)

            elif sub_choice == "Drink water":
                # Call the add_habit function to create the new habit in the database
                add_habit(db, "Drink water", "Daily")

            elif sub_choice == "Go sleep early":
                # Call the add_habit function to create the new habit in the database
                add_habit(db, "Go sleep early", "Daily")

            elif sub_choice == "Work":
                # Call the add_habit function to create the new habit in the database
                add_habit(db, "Work", "Daily")

            elif sub_choice == "Workout":
                # Call the add_habit function to create the new habit in the database
                add_habit(db, "Workout", "Daily")

            else:
                # Call the add_habit function to create the new habit in the database
                add_habit(db, "Meditation", "Weekly")

            # Prompting the user if they want to do anything else
            question = questionary.confirm("Anything else").ask()

            # if the user quits, prints a message and breaks the loop
            if not question:
                break

        elif choice == "Edit":
            # Show the user a list of active habits and ask them which one they want to edit
            print(show_habits_active(db))
            habit_id = questionary.select("Alright, Choose the ID of the habit:",
                                          choices=[str(i) for i in list(show_habits_active(db).index)]
                                          ).ask()
            # Ask the user which aspect of the habit they want to change (name or periodicity)
            column = questionary.select("What are you going to change?",
                                        choices=['HABIT_NAME', 'PERIODICITY']
                                        ).ask()

            # Depending on the user's choice, ask for a new name or periodicity and call the edit_habit function
            if column == "PERIODICITY":
                new_value = questionary.select("Almost there, choose the frequency you want",
                                               choices=["Daily", "Weekly", "Twice a month",
                                                        "Monthly", "Quarterly", "Twice a year", "Yearly"]
                                               ).ask()

            else:
                new_value = questionary.text("Almost there, type in what do you want").ask()

            edit_habit(db, habit_id, column, new_value)

            # Prompting the user if they want to do anything else
            question = questionary.confirm("Anything else").ask()

            # if the user quits, prints a message and breaks the loop
            if not question:
                break

        elif choice == "Increment":
            # Show the user a list of active habits and ask them which one they want to increment
            print(show_habits_active(db))

            habit_id = questionary.select("Alright, Choose the ID of the habit:",
                                          choices=[str(i) for i in list(show_habits_active(db).index)]
                                          ).ask()

            # Call the increment_habit function to increment the selected habit's count
            increment_habit(db, habit_id)

            # Prompting the user if they want to do anything else
            question = questionary.confirm("Anything else").ask()

            # if the user quits, prints a message and breaks the loop
            if not question:
                break

        elif choice == "Reset":
            # prints the active habits in the database
            print(show_habits_active(db))

            # prompts the user to select an ID of the habit to reset
            habit_id = questionary.select("Alright, Choose the ID of the habit:",
                                          choices=[str(i) for i in list(show_habits_active(db).index)]
                                          ).ask()

            # resets the habit with the selected ID
            reset_habit(db, habit_id)

            # Prompting the user if they want to do anything else
            question = questionary.confirm("Anything else").ask()

            # if the user quits, prints a message and breaks the loop
            if not question:
                break

        elif choice == "Delete":
            # prints the active habits in the database
            print(show_habits_active(db))

            # prompts the user to select an ID of the habit to delete
            habit_id = questionary.select("Alright, Choose the ID of the habit:",
                                          choices=[str(i) for i in list(show_habits_active(db).index)]
                                          ).ask()

            # deletes the habit with the selected ID
            delete_habit(db, habit_id)

            # Prompting the user if they want to do anything else
            question = questionary.confirm("Anything else").ask()

            # if the user quits, prints a message and breaks the loop
            if not question:
                break

        else:
            # Prints a message and break the loop
            print("We'll miss you here, comeback soon!")
            break


# Launching the application
if __name__ == "__main__":
    cli()
