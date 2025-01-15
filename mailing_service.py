from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MailingService():
    def __init__(self):
        load_dotenv()
        self.email_address = os.getenv("EMAIL_ADDRESS")
        self.email_password = os.getenv("EMAIL_PASSWORD")
    #Eventually this will attach an RGB image to the embedded in the message to capture what caused the movement, and maybe some bounding box stuff.
    def send_alert(self):
        msg = MIMEMultipart()
        msg['From'] = self.email_address
        msg['To'] = self.email_password
        msg['Subject'] = "MOVEMENT DETECTED"

        body = "MOVEMENT HAS BEEN DETECTED"
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.email_address, self.email_password)
                server.sendmail(self.email_address, self.email_address, msg.as_string())
        except Exception as e:
            print(e)
