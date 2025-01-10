# type: ignore
import csv, pprint, datetime
from task_manager import Task

class ListManager:
    def __init__(self, csv_filename):
        self.csv_file = csv_filename
        self.initial_task_list = self.read_task_list_from_csv()
        self.task_list = []
        for task in self.initial_task_list:
            # print(task)
            new_task = self.update_due_date_if_past_due(task)
            self.task_list.append(new_task)

    # Read task list from CSV file
    def read_task_list_from_csv(self):
        """Read tasks from a CSV file.

        The CSV file is expected to have columns labeled "task name", "task freq", "task due", and "day of week".

        Args:
            file_path (str): The path to the CSV file.

        Returns:
            list: A list of tasks, where each task is a dict with the keys "task name", "task freq", "task due", and "day of week".
        """

        tasks = []
        # Open the CSV file and read the tasks
        with open(self.csv_file, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                tasks.append({
                    'task name': row['task name'],
                    'task freq': row['task freq'],
                    'task due': row['task due'],
                    'day of week': row['day of week']
                })
        return tasks

    
    def write_task_list_to_csv(self):
        """
        Write the updated task list to the CSV file.
        """
        with open(self.csv_file, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['task name', 'task freq', 'task due', 'day of week'])
            writer.writeheader()
            writer.writerows(task.to_dict() if isinstance(task, Task) else task for task in self.task_list)
            print('Task list updated')


    def print_tasks(self):
        #TODO: Something's not working here
        """
        Print the task list.

        This function prints the current task list in a human-readable format using pretty-printing.
        """

        pprint.pprint(self.task_list)
        # pprint.pprint([task.to_dict() for task in self.task_list])


    def enumerate_tasks(self):
        """
        Enumerate the tasks in the task list and return the task number and Task object of the selected task.

        Asks the user to select a task from the task list and return the task number and the selected Task object.

        Returns:
            tuple: A tuple containing the task number and the selected Task object.
        """

        print('\nTask List:')
        for i, task in enumerate(self.task_list, start=1):
            print(f'{i}. {task["task name"]}: Due {task["task due"]} every {task["task freq"]} days')
        while True:
            try:
                task_num = int(input(f'\nEnter the task number to edit/delete: '))
                if 1 <= task_num <= len(self.task_list):
                    selected_task = Task(task_name=self.task_list[task_num - 1]['task name'], task_freq=self.task_list[task_num - 1]['task freq'], task_due=datetime.datetime.strptime(self.task_list[task_num - 1]['task due'], '%m/%d/%Y').date() if isinstance(self.task_list[task_num - 1]['task due'], str) else self.task_list[task_num - 1]['task due'], day_of_week=self.task_list[task_num - 1]['day of week'])
                    break
                else:
                    print(f'Invalid task number. Please enter a number between 1 and {len(self.task_list)}.')
            except ValueError:
                print(f'Invalid input. Please enter a number between 1 and {len(self.task_list)}.')
        return task_num, selected_task
    

    def add_new_task(self):
        """
        Add a new task to the task list.

        Asks the user to select a task name, frequency, due date, and day of week.

        Args:
            None

        Returns:
            None
        """

        task_name = Task()

        # Add the task to the list
        task_name.to_dict()
        pprint.pprint(task_name.to_dict())
        self.task_list.append(task_name)
        print(f'{task_name} added to task list')


    def delete_task(self, task_num=None):
        """
        Delete a task from the task list.

        If task_num is None, asks the user to select a task from the task list and then deletes it.
        If task_num is an integer, deletes the task at that index in the task list (1-indexed).

        Args:
            task_num (int or None): The number of the task to delete, or None to ask the user to select a task.

        Returns:
            None
        """
        if task_num is None:
            task_num, selected_task = self.enumerate_tasks()
            del self.task_list[task_num - 1]
            print(f'Task {task_num}, {selected_task.task_name} deleted.')
        else:
            selected_task = self.task_list[task_num - 1]
            del self.task_list[task_num - 1]
            print(f'Task {task_num}, {selected_task.task_name} deleted.')


    def update_list(self, task_num, selected_task):
        """
        Update the task list with the new task information.

        Args:
            task_num (int): The number of the task to update in the task list (1-indexed).
            selected_task (Task): The updated Task object.

        Returns:
            None
        """

        self.delete_task(task_num)
        self.task_list.append(selected_task)
        self.write_task_list_to_csv()
                # pprint.pprint(selected_task.from_dict(selected_task))    
    
    def edit_task(self):
        """
        Allows the user to edit a task in the task list.

        Asks the user to select a task from the task list and then asks what they want to edit about the task: the task name, due date, frequency, or all of the above.

        Args:
            None

        Returns:
            None
        """
        task_num, selected_task = self.enumerate_tasks()

        while True:
            edit_what = input(f'Would you like to edit the task name, due date, frequency, or all of the above for {selected_task.task_name}? (n/d/f/a): ').lower()
            if edit_what == 'n':
                selected_task.task_name = selected_task.get_task_name()
                self.update_list(task_num, selected_task)
                break
            elif edit_what == 'd':
                selected_task.task_due = selected_task.get_task_due()
                self.update_list(task_num, selected_task)
                break
            elif edit_what == 'f':
                selected_task.task_freq = selected_task.get_task_freq()
                self.update_list(task_num, selected_task)
                break
            elif edit_what == 'a':
                selected_task.task_name = selected_task.get_task_name()
                selected_task.task_due = selected_task.get_task_due()
                selected_task.task_freq = selected_task.get_task_freq()
                self.update_list(task_num, selected_task)
                break
            else:
                print("Invalid input. Please enter 'n','d', 'f', or 'a'.")

    def update_due_date_if_past_due(self, task):
        """
        Update the due date of a task based on its frequency.

        This function takes a task dictionary with a due date and frequency,
        then adjusts the due date forward in time by increments of the frequency
        (in days) until the due date is on or after the current date. The 
        modified task dictionary is returned with the updated due date.

        Args:
            task (dict): A dictionary representing a task with keys 'task freq' and 'task due'.

        Returns:
            dict: The updated task dictionary with the new 'task due' date.
        """

        frequency = task['task freq']
        # print(frequency)
        task_due_date = datetime.datetime.strptime(task['task due'], '%m/%d/%Y').date()
        while task_due_date < datetime.date.today():
            task_due_date += datetime.timedelta(days=int(frequency))
            task['task due'] = task_due_date.strftime('%m/%d/%Y')
        return task
