import smtplib
import ssl
from email.message import EmailMessage
import os
from dotenv import load_dotenv


def send():
    load_dotenv()

    # Email parameters from .env
    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = os.getenv('RECEIVER_EMAIL')
    password = os.getenv('PASSWORD')

    # print the above 3
    print(sender_email)
    print(receiver_email)
    print(password)

    subject = "Game Found"
    body = "Hello, game has been found!"

    # Create email message
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Create SMTP session with SSL
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.send_message(msg)

if __name__ == "__main__":
    send()