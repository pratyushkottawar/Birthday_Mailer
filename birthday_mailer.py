import csv
import os
from datetime import datetime
from email.message import EmailMessage
import smtplib

def send_email(to, subject, body):
    msg = EmailMessage()
    msg['From'] = os.environ['EMAIL']
    msg['To'] = to
    msg['Subject'] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.environ['EMAIL'], os.environ['EMAIL_PASSWORD'])
            smtp.send_message(msg)
            print(f"Email sent to {to}")
    except Exception as e:
        print(f"Error sending email to {to}: {e}")

def check_and_send():
    today = datetime.now().strftime('%d-%m')
    with open('birthdays.csv') as f:
        reader = csv.DictReader(f)
        people = list(reader)

    for person in people:
        if person['birthday'] == today:
            birthday_person = person
            others = [p for p in people if p != person]

            # 🎉 Send birthday mail
            send_email(
                birthday_person['email'],
                f"Happy Birthday {birthday_person['name']}! 🎉",
                f"Hey {birthday_person['name']},\n\nWishing you an amazing birthday filled with joy and blessings!\n\n– Your Team"
            )

            # ⏰ Send reminder to others
            for other in others:
                send_email(
                    other['email'],
                    f"{birthday_person['name']}'s Birthday Today 🎂",
                    f"Hey {other['name']},\n\nToday is {birthday_person['name']}'s birthday! Don’t forget to wish them. 🎉"
                )

if __name__ == "__main__":
    check_and_send()