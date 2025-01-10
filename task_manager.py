# type: ignore
import datetime


class Task:
    def __init__(self, task_name=None, task_freq=None, task_due=None, day_of_week=None):
        """
        Initialize a new Task object.

        If any of the parameters are None, will prompt the user for input.

        Parameters:
            task_name (str): The name of the task.
            task_freq (int): The frequency of the task in days.
            task_due (str or datetime.date): The due date of the task in MM/DD/YYYY format, or a datetime.date object.
            day_of_week (str): The day of the week that the task is due.

        Returns:
            None
        """
        if task_name is None:
            task_name = self.get_task_name()
            # task_name = input('Enter new task name: ')
        self.task_name = task_name

        if task_freq is None:
            task_freq = self.get_task_freq()
            # task_freq = input('Enter task frequency (days): ')
            # task_due = input('Enter due date for {} (MM/DD/YYYY): '.format(task_name))
        self.task_freq = task_freq
        
        if task_due is None:
            task_due = self.get_task_due()
        self.task_due = datetime.datetime.strptime(task_due, '%m/%d/%Y').date() if isinstance(task_due, str) else task_due
        
        if day_of_week is None:
            day_of_week = self.get_day_of_week()
            # day_of_week = input('Enter day of week (e.g. Monday): ')
        self.day_of_week = day_of_week

    def get_task_name(self):
    """
    Prompt the user to enter a valid task name.

    Continuously asks the user to input a task name that contains at least one
    letter and one alphanumeric character. Provides feedback to the user if the
    input is invalid. Returns the validated task name as a string.

    Returns:
        str: The validated task name.
    """

        while True:
            task_name = input('Enter new task name: ')
            if any(char.isalpha() for char in task_name) and any(char.isalnum() for char in task_name):
                break
            else:
                print("Please enter a string containing at least one letter.")
        return task_name
   
    
    def get_task_due(self):
    """
    Prompt the user to enter a valid due date for the task.

    Continuously asks the user to input a due date in the format MM/DD/YYYY.
    Ensures that the input date is valid and not in the past. If the date is 
    valid and today or in the future, it returns the date as a datetime.date object. 
    Provides feedback to the user if the input is invalid or the date is in the past.

    Returns:
        datetime.date: The validated due date of the task.
    """

        while True:
            task_due = input(f'Enter due date for {self.task_name} (MM/DD/YYYY): ')
            # task_due = input(f'Enter new due date for {selected_task["task name"]} (MM/DD/YYYY): ')
            try:
                # task_due_date = datetime.datetime.strptime(task_due, '%m/%d/%Y').date()
                task_due_date = datetime.datetime.strptime(task_due, '%m/%d/%Y').date()
                if task_due_date >= datetime.date.today():
                    break
                else:
                    print("Please enter a date that is today or in the future.")
            except ValueError:
                print("Invalid date format. Please enter the date in MM/DD/YYYY format.")
        return task_due_date


    def get_task_freq(self):
    """
    Prompt the user to enter a valid task frequency in days.

    Continuously asks the user to input a positive integer representing the number of days
    between task occurrences. The function ensures the input is a positive integer and 
    returns it as a string once validated.

    Returns:
        str: The task frequency in days as a string.
    """

        while True:
            task_freq = input('Enter task frequency (days): ')
            if task_freq.isdigit() and int(task_freq) > 0:
                break
            else:
                print("Please enter a positive integer for the frequency.")
        return task_freq
    
    
    def get_day_of_week(self):
    """
    Determine and confirm the day of the week for the task due date.

    If the task frequency is a multiple of 7, this function calculates the day of the week
    for the task's due date and prompts the user to confirm its accuracy. If the user disagrees,
    they are asked to re-enter the due date until the correct day of the week is confirmed.
    If the task frequency is not a multiple of 7, the day of the week is set to 'Varies'.

    Returns:
        str: The confirmed day of the week or 'Varies' if the frequency is not a multiple of 7.
    """

        # Check if the frequency is a multiple of 7
        if int(self.task_freq) % 7 == 0:
            # Calculate the day of the week for the due date
            # task_due_date = datetime.datetime.strptime(self.task_due, '%m/%d/%Y').date()
            day_of_week = self.task_due.strftime('%A')
            # self.day_of_week = task_due_date.strftime('%A')
            print(day_of_week)

            # Confirm with the user that the day of the week is correct
            while True:
                confirm = input(f'{self.task_name} is due on {day_of_week}. Is this correct? (y/n): ').lower()
                if confirm == 'y':
                    break
                elif confirm == 'n':
                        print('Please try again.')
                        break
                else:
                    print("Invalid input. Please enter 'y' for yes or 'n' for no.")
            while confirm == 'n':
                self.task_due = self.get_task_due()
                day_of_week = self.task_due.strftime('%A') # task_due_date.strftime('%A')
                # TODO: I'm not sure why the below while loop is needed. Should be able to get rid of this somehow to shorten the code.
                while True:
                    confirm = input(f'{self.task_name} is due on {day_of_week}. Is this correct? (y/n): ').lower()
                    if confirm == 'y':
                        break
                    elif confirm == 'n':
                        print('Please try again.')
                        break
                    else:
                        print('Invalid input. Please enter (y/n).')
        else:
            day_of_week = 'Varies' 
        return day_of_week
              

    def to_dict(self):
        """
        Return a dictionary representation of the task.

        The dictionary will have the keys "task name", "task freq", "task due", and "day of week", and the
        corresponding values for the task.

        Returns:
            dict: A dictionary representation of the task.
        """
        return {
            'task name': self.task_name,
            'task freq': str(self.task_freq),
            'task due': self.task_due.strftime('%m/%d/%Y'),
            'day of week': self.day_of_week
        }

    def from_dict(self, task_dict):
    """
    Update the task's attributes based on a dictionary representation.

    Extracts the task name, frequency, due date, and day of the week from
    a provided dictionary and assigns these values to the task's attributes.

    Args:
        task_dict (dict): A dictionary containing task information with keys
                          'task name', 'task freq', 'task due', and 'day of week'.
    """

        self.task_name = task_dict['task name']
        self.task_freq = int(task_dict['task freq'])
        self.task_due = datetime.datetime.strptime(task_dict['task due'], '%m/%d/%Y').date()
        self.day_of_week = task_dict['day of week']
    

    def new_task(self):
        pass