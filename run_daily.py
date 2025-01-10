# type: ignore
import datetime, os
from list_manager import ListManager
from task_manager import Task
from notification_manager import NotificationManager

MY_EMAIL = os.getenv('MY_EMAIL')
MY_PASSWORD = os.getenv('MY_PASSWORD')
MY_PHONE = os.getenv('MY_PHONE')    

def run_daily():
        # TODO: Make this run once a day at 7am. Added to Microsoft scheduled tasks, but not working. Fix this.
        today = datetime.date.today().strftime('%m/%d/%Y')
        print(today)
        # Initialize the ListManager object which also updates any past due tasks.
        list_manager = ListManager('task_list.csv')
        list_manager.print_tasks()
        list_manager.write_task_list_to_csv()

        notification_manager = NotificationManager(MY_EMAIL, MY_PASSWORD)
        # Send text messages for tasks due today
        #TODO: Add this as class method in task manager
        for task in list_manager.task_list:
            if task['task due'] == today:
                notification_manager.send_text_via_email(MY_PHONE,'verizon', task['task name'] + ' is due today')
                print(task['task name'] + ' is due today')
        # notification_manager.send_text_via_email(MY_PHONE, 'verizon', 'Tasks have been updated.')

if __name__ == "__main__":
    run_daily()