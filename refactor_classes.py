# type: ignore
import csv
import pprint
import smtplib
import datetime
import os
from email.mime.text import MIMEText

class Task:
    def __init__(self, name, freq, due, day_of_week):
        self.name = name
        self.freq = int(freq)
        self.due = datetime.datetime.strptime(due, '%m/%d/%Y').date()
        self.day_of_week = day_of_week

    def update_due_date(self):
        while self.due < datetime.date.today():
            self.due += datetime.timedelta(days=self.freq)
        return self

    def to_dict(self):
        return {
            'task name': self.name,
            'task freq': str(self.freq),
            'task due': self.due.strftime('%m/%d/%Y'),
            'day of week': self.day_of_week
        }

class TaskManager:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.tasks = self.read_tasks_from_csv()

    def read_tasks_from_csv(self):
        tasks = []
        with open(self.csv_file, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                task = Task(row['task name'], row['task freq'], row['task due'], row['day of week'])
                tasks.append(task)
        return tasks

    def update_all_due_dates(self):
        for task in self.tasks:
            task.update_due_date()

    def write_tasks_to_csv(self):
        with open(self.csv_file, 'w', newline='') as csv_file:
            fieldnames = ['task name', 'task freq', 'task due', 'day of week']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for task in self.tasks:
                writer.writerow(task.to_dict())

    def print_tasks(self):
        pprint.pprint([task.to_dict() for task in self.tasks])

class NotificationManager:
    CARRIERS = {
        'att': '@txt.att.net',
        'verizon': '@vtext.com',
        'sprint': '@messaging.sprintpcs.com',
        'tmobile': '@tmomail.net'
    }

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def send_text_via_email(self, to_number, carrier, message):
        to_address = f"{to_number}{self.CARRIERS[carrier]}"
        msg = MIMEText(message, 'plain')
        msg['From'] = self.email
        msg['To'] = to_address
        msg['Subject'] = ""

        with smtplib.SMTP("smtp.mail.yahoo.com", 587) as server:
            server.starttls()
            server.login(self.email, self.password)
            server.sendmail(self.email, to_address, msg.as_string())
            print('Text message sent')

# Environment variables
MY_EMAIL = os.getenv('MY_EMAIL')
MY_PASSWORD = os.getenv('MY_PASSWORD')
MY_PHONE = os.getenv('MY_PHONE')

# Main execution
if __name__ == "__main__":
    task_manager = TaskManager('task_list.csv')
    task_manager.update_all_due_dates()
    task_manager.print_tasks()
    task_manager.write_tasks_to_csv()

    notification_manager = NotificationManager(MY_EMAIL, MY_PASSWORD)
    notification_manager.send_text_via_email(MY_PHONE, 'verizon', 'Tasks have been updated.')