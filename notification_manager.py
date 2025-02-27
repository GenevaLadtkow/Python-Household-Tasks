# type: ignore
import smtplib
from email.mime.text import MIMEText

class NotificationManager:
    # Carrier email-to-SMS gateway domain
    CARRIERS = {
        'att': '@txt.att.net',
        'verizon': '@vtext.com',
        'sprint': '@messaging.sprintpcs.com',
        'tmobile': '@tmomail.net'
    }

    # MY_EMAIL = os.getenv('MY_EMAIL')
    # MY_PASSWORD = os.getenv('MY_PASSWORD')
    # MY_PHONE = os.getenv('MY_PHONE')

    def __init__(self, email, password):
        """
        Initializes a NotificationManager object with the specified email and password.

        Args:
            email (str): The email address to use for sending the text message.
            password (str): The password associated with the email address.

        """
        self.email = email
        self.password = password
        # self.phone = MY_PHONE

    def send_text_via_email(self, to_number, carrier, message):
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
        to_address = f'{to_number}{self.CARRIERS[carrier]}'
        msg = MIMEText(message, 'plain')
        msg['From'] = self.email
        msg['To'] = to_address
        msg['Subject'] = ''

        # Send the message via SMTP
        with smtplib.SMTP('smtp.mail.me.com', 587) as server: # only works with icloud email addresses (@icloud.com or @me.com)
            server.starttls()
            server.login(self.email, self.password)
            server.sendmail(self.email, to_address, msg.as_string())
            print('Text message sent')


    def run_daily(self):
        # TODO: Make this run once a day at 7am. Add to crontab? Make the user input part below not run at that time.
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
        notification_manager.send_text_via_email(MY_PHONE, 'verizon', 'Tasks have been updated.')