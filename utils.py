import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

def load_template(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()

def send_html_email(subject, to_email, html_body, email_user, email_pass, image_path=None):
    msg = MIMEMultipart("related")
    msg['Subject'] = subject
    msg['From'] = email_user
    msg['To'] = to_email

    msg.attach(MIMEText(html_body, 'html'))

    if image_path:
        try:
            with open(image_path, "rb") as img:
                mime_img = MIMEImage(img.read())
                mime_img.add_header("Content-ID", "<birthdayimage>")
                msg.attach(mime_img)
        except Exception as e:
            print(f"⚠️ Could not attach image: {e}")

    try:
        print(f"📤 Sending mail to {to_email}")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=20) as server:
            server.login(email_user, email_pass)
            server.send_message(msg)
        print(f"✅ Mail sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send mail to {to_email}. Error: {e}")