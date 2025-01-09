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

    def __init__(self, email, password):
        self.email = email
        self.password = password

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
