# type: ignore
import datetime


class Task:
    def __init__(self, task_name, task_freq, task_due, day_of_week):
        self.task_name = task_name
        self.task_freq = task_freq
        self.task_due = task_due
        self.day_of_week = day_of_week

    def to_dict(self):
        return {
            'task name': self.name,
            'task freq': str(self.freq),
            'task due': self.due.strftime('%m/%d/%Y'),
            'day of week': self.day_of_week
        }
    

    def new_task(self):
        pass