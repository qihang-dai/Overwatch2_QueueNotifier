import smtplib
import ssl
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from utils import logger

def send(sender_email, password, receiver_email):
    load_dotenv()
    if not receiver_email:
        logger.error("no receiver email")
        return
    # Email parameters from .env
    if not sender_email:
        sender_email = os.getenv('SENDER_EMAIL')
    # receiver_email = os.getenv('RECEIVER_EMAIL')
    if not password:
        password = os.getenv('PASSWORD')
    subject = "Game Found"
    body = "Hello, game has been found!"
    print(sender_email, password, receiver_email)
    print("sending email to", receiver_email, "from", sender_email)
    logger.info("sending email to %s from %s", receiver_email, sender_email)
    logger.debug("debugging")

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
