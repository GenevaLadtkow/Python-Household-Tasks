# type: ignore
import csv, pprint, smtplib, datetime, os
import smtplib
from email.mime.text import MIMEText

today = datetime.date.today().strftime('%m/%d/%Y')
print(today)

# Carrier email-to-SMS gateway domain
CARRIERS = {
    'att':    '@txt.att.net',
    'verizon': '@vtext.com',
    'sprint':  '@messaging.sprintpcs.com',
    'tmobile': '@tmomail.net'
}

# Environment variables
MY_EMAIL = os.getenv('MY_EMAIL')
MY_PASSWORD = os.getenv('MY_PASSWORD')
MY_PHONE = os.getenv('MY_PHONE')


# Read task list from CSV file
def read_task_list_from_csv(file_path='task_list.csv'):
    """Read tasks from a CSV file.

    The CSV file is expected to have columns labeled "task name", "task freq", "task due", and "day of week".

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        list: A list of tasks, where each task is a dict with the keys "task name", "task freq", "task due", and "day of week".
    """

    tasks = []
    # Open the CSV file and read the tasks
    with open(file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            tasks.append({
                'task name': row['task name'],
                'task freq': row['task freq'],
                'task due': row['task due'],
                'day of week': row['day of week']
            })
    return tasks

tasks = read_task_list_from_csv()

def update_due_date(task):
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


new_task_list = []
for task in tasks:
    # print(task)
    new_task = update_due_date(task)
    new_task_list.append(new_task)
    # print(task)
    # print(new_task_list)

# print(new_task_list)
pprint.pprint(new_task_list)

def write_task_list_to_csv(task_list):
    """
    Write the updated task list to the CSV file.
    """
    with open('task_list.csv', 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['task name', 'task freq', 'task due', 'day of week'])
        writer.writeheader()
        writer.writerows(task_list)
        print('Task list updated')

write_task_list_to_csv(new_task_list)

def send_text_via_email(to_number, carrier, message):
    """
    Sends a text message via email to a specified phone number using the carrier's email-to-SMS gateway.

    Args:
        to_number (str): The recipient's phone number.
        carrier (str): The recipient's carrier name, used to determine the email-to-SMS gateway domain.
        message (str): The text message to be sent.

    This function logs into the email server using provided credentials, creates an email message with the specified 
    content, and sends it to the constructed email address corresponding to the recipient's phone number and carrier. 
    """

    # Construct the email address to send the text message
    to_address = f'{to_number}{CARRIERS[carrier]}'
    msg = MIMEText(message, 'plain')
    msg['From'] = MY_EMAIL
    msg['To'] = to_address
    msg['Subject'] = ''

    # Send the message via SMTP
    with smtplib.SMTP('smtp.mail.me.com', 587) as server:
        server.starttls()
        server.login(MY_EMAIL, MY_PASSWORD)
        server.sendmail(MY_EMAIL, to_address, msg.as_string())
        print('Text message sent')


# Send text messages for tasks due today
# for task in tasks:
#     if task['task due'] == today:
#         send_text_via_email(MY_PHONE,'verizon', task['task name'] + ' is due today')
#         print(task['task name'] + ' is due today')


def add_new_task():
    """
    Adds a new task to the task list by prompting the user for the task name, frequency, and due date.

    The user is asked to enter the task name, frequency in days, and due date in MM/DD/YYYY format. If the frequency is a
    multiple of 7, the program asks the user to confirm that the day of the week is correct. If the user answers 'y', the
    program adds the task to the list with the correct day of the week. If the user answers 'n', the program asks the user
    to re-enter the due date and confirm the day of the week again. If the frequency is not a multiple of 7, the program
    adds the task to the list with 'Varies' as the day of the week.

    Args:
        None

    Returns:
        None
    """
    
    while True:
        task_name = input('Enter new task name: ')
        if any(char.isalpha() for char in task_name) and any(char.isalnum() for char in task_name):
            break
        else:
            print("Please enter a string containing at least one letter.")
    while True:
        task_freq = input('Enter task frequency (days): ')
        if task_freq.isdigit() and int(task_freq) > 0:
            break
        else:
            print("Please enter a positive integer for the frequency.")
    while True:
        task_due = input(f'Enter due date for {task_name} (MM/DD/YYYY): ')
        try:
            task_due_date = datetime.datetime.strptime(task_due, '%m/%d/%Y').date()
            break
        except ValueError:
            print("Invalid date format. Please enter the date in MM/DD/YYYY format.")

    # Check if the frequency is a multiple of 7
    if int(task_freq) % 7 == 0:
        # Calculate the day of the week for the due date
        task_due_date = datetime.datetime.strptime(task_due, '%m/%d/%Y').date()
        day_of_week = task_due_date.strftime('%A')

        # Confirm with the user that the day of the week is correct
        while True:
            confirm = input(f'{task_name} is due on {day_of_week}. Is this correct? (y/n): ').lower()
            if confirm == 'y':
                break
            elif confirm == 'n':
                    print('Please try again.')
                    break
            else:
                print("Invalid input. Please enter 'y' for yes or 'n' for no.")
        while confirm == 'n':
            while True:
                task_due = input(f'Enter due date for {task_name} (MM/DD/YYYY): ')
                try:
                    task_due_date = datetime.datetime.strptime(task_due, '%m/%d/%Y').date()
                    break
                except ValueError:
                    print("Invalid date format. Please enter the date in MM/DD/YYYY format.")
            task_due_date = datetime.datetime.strptime(task_due, '%m/%d/%Y').date()
            day_of_week = task_due_date.strftime('%A')
            while True:
                confirm = input(f'{task_name} is due on {day_of_week}. Is this correct? (y/n): ').lower()
                if confirm == 'y':
                    break
                elif confirm == 'n':
                    print('Please try again.')
                    break
                else:
                    print('Invalid input. Please enter (y/n).')

        # Add the task to the list
        new_task = {'task name': task_name, 'task freq': task_freq, 'task due': task_due, 'day of week': day_of_week}
        new_task_list.append(new_task)
        print(f'{task_name} added to task list')
    else:
        # Add the task to the list
        new_task = {'task name': task_name, 'task freq': task_freq, 'task due': task_due, 'day of week': 'Varies'}
        new_task_list.append(new_task)
        print(f'{task_name} added to task list')


add_new_task()
# pprint.pprint(new_task_list)

# Write updated task list to CSV file
write_task_list_to_csv(new_task_list)


def delete_task(task_list):
    """
    Asks the user to select a task from the task list and confirm deletion before removing it.

    Args:
        task_list (list): A list of tasks, where each task is a dict with keys "task name", "task freq", "task due", and "day of week".

    Returns:
        None
    """

    print('\nTask List:')
    for i, task in enumerate(task_list, start=1):
        print(f'{i}. {task["task name"]}: Due {task["task due"]} every {task["task freq"]} days')
    while True:
        try:
            task_num = int(input(f'\nEnter the task number to delete: '))
            if 1 <= task_num <= len(task_list):
                selected_task = task_list[task_num - 1]
                while True:
                    confirm = input(f'Are you sure you want to delete "{selected_task["task name"]}"? (y/n): ').lower()
                    if confirm == 'y':
                        del task_list[task_num - 1]
                        print(f'Task {task_num} deleted.')
                        break
                    elif confirm == 'n':
                        print('Task deletion canceled. Please try again.')
                        break
                    else:
                        print("Invalid input. Please enter 'y' for yes or 'n' for no.")
                if confirm == 'y':
                    break
            else:
                print(f'Invalid task number. Please enter a number between 1 and {len(task_list)}.')
        except ValueError:
            print(f'Invalid input. Please enter a number between 1 and {len(task_list)}.')


delete_task(new_task_list)
# pprint.pprint(new_task_list)
write_task_list_to_csv(new_task_list)
