import smtplib
import time

def send_email(subject, message, recipient):
    # Gmail account info
    gmail_user = "your_email@gmail.com"
    gmail_password = "your_gmail_password"

    # Compose email
    message = "Subject: {}\n\n{}".format(subject, message)

    # Send email
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, recipient, message)
        server.close()
        print("Email sent!")
    except Exception as e:
        print("Failed to send email: ", e)

def check_queue():
    # Replace this with code to check the Overwatch queue status

    # Example: return False if the queue is still active, True if it's finished
    return True

# Loop until the Overwatch queue is finished
while not check_queue():
    time.sleep(60)  # Check queue status every minute

# Send email notification
send_email("Overwatch queue finished", "The Overwatch queue has finished!", "recipient_email@gmail.com")


