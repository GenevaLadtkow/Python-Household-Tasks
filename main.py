# type: ignore
import datetime, os
from list_manager import ListManager
from task_manager import Task
from notification_manager import NotificationManager

# Environment variables
MY_EMAIL = os.getenv('MY_EMAIL')
MY_PASSWORD = os.getenv('MY_PASSWORD')
MY_PHONE = os.getenv('MY_PHONE')

# Main execution
if __name__ == "__main__":
    # TODO: Make this run once a day at 7am. Add to crontab? Make the user input part below not run at that time.
    today = datetime.date.today().strftime('%m/%d/%Y')
    print(today)
    list_manager = ListManager('task_list.csv')
    list_manager.print_tasks()
    list_manager.write_task_list_to_csv()

    notification_manager = NotificationManager(MY_EMAIL, MY_PASSWORD)
    # Send text messages for tasks due today
    # TODO: Add this as class method in task manager
    # for task in list_manager.task_list:
    #     if task['task due'] == today:
    #         notification_manager.send_text_via_email(MY_PHONE,'verizon', task['task name'] + ' is due today')
    #         print(task['task name'] + ' is due today')
    # notification_manager.send_text_via_email(MY_PHONE, 'verizon', 'Tasks have been updated.')


    # TODO: Make this repeatable for multiple additions or deletions. Only run this part if the user wants to.
    action = input('Would you like to add or delete a new task? (add/delete/quit): ').lower()
    if action == 'add':
        list_manager.add_new_task()
        list_manager.write_task_list_to_csv()
    elif action == 'delete':
        list_manager.delete_task()
        list_manager.write_task_list_to_csv()
    elif action == 'quit':
        print('Goodbye!')
