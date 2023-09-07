"""
Adalberto Acosta - 9/6/23
This is a sms and mms module for sending texts to the specified phone number.
SMS: Short Message Service    |     MMS: Multimedia Messaging Service
The basic difference is that mms includes multimedia along with the text, like an image.
It uses email to SMS gateways provided by most major service providers. A short
list of some provider sms and mms emails is provided at providers.py

NOTE:
    If you want to use this, make sure to change the "sender_credentials" default param
    or alternatively pass in an argument when calling the function
"""

import smtplib, ssl
from providers import PROVIDERS

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from os.path import basename


# Function for sending sms texts, takes in a cell phone number, text message, service provider
# subject (since this is an email), and credentials of the sender. The gmail server and port are provided
def send_sms_via_email(number: str, message: str, provider: str, subject: str = "sent using python", sender_credentials: tuple = ("your@email.com", "emailpassword2001#"), smtp_server: str = "smtp.gmail.com", smtp_port: int = 465):

    sender_email, email_password = sender_credentials
    receiver_email = f"{number}@{PROVIDERS.get(provider).get('sms')}"  # Applying sms gateway email template to the phone number
    email_message = f"Subject:{subject}\nTo:{receiver_email}\n{message}"  # Message to be sent

    # Using smtp library to login and send email to gateway
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=ssl.create_default_context()) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email, email_message)


# Function for sending mms using the same parameters as sms with some extra additions:
# The mime types for mms and the file to be sent in the mms message.
def send_mms_via_email(
        number: str,
        message: str,
        file_path: str,
        mime_maintype: str,
        mime_subtype: str,
        provider: str,
        subject: str = "sent using python",
        sender_credentials: tuple = ("your@email.com", "emailpassword2001#"),
        smtp_server: str = "smtp.gmail.com",
        smtp_port: int = 465,
):
    sender_email, email_password = sender_credentials
    receiver_email = f"{number}@{PROVIDERS.get(provider).get('mms')}"  # Applying mms gateway email template to the phone number

    # Basic formatting for the mms message
    email_message = MIMEMultipart()
    email_message["Subject"] = subject
    email_message["To"] = receiver_email
    email_message["From"] = sender_email
    email_message.attach(MIMEText(message, "plain"))

    # Attaching multimedia to image
    with open(file_path, "rb") as attachment:
        part = MIMEBase(mime_maintype, mime_subtype)
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition", f"attachment; filename={basename(file_path)}"
        )

        email_message.attach(part)
    text = email_message.as_string()  # Final text to be sent in message

    # Using smtp library to login and send email to gateway
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=ssl.create_default_context()) as email:
        email.login(sender_email, email_password)
        email.sendmail(sender_email, receiver_email, text)
