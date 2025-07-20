import csv
import smtplib
from email.message import EmailMessage
from datetime import datetime
import os

EMAIL_ADDRESS = os.environ['EMAIL']
EMAIL_PASSWORD = os.environ['EMAIL_PASSWORD']

today = datetime.now().strftime('%d-%m')

birthday_people = []
others = []

# Load data
with open('birthdays.csv') as f:
    reader = csv.DictReader(f)
    data = list(reader)

for person in data:
    if person['birthday'] == today:
        birthday_people.append(person)
    else:
        others.append(person)

# Exit early if no birthdays today
if not birthday_people:
    print("No birthdays today. Exiting.")
    exit(0)

# Send mail to birthday people
for person in birthday_people:
    msg = EmailMessage()
    msg['Subject'] = f"🎉 Happy Birthday {person['name']}!"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = person['email']
    msg.set_content(f"Dear {person['name']},\n\nWishing you a fantastic birthday filled with joy and success!\n\nBest regards,\nYour Birthday Group 🥳")
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print(f"Sent birthday mail to {person['name']}")

# Send mail to others as reminder
for other in others:
    msg = EmailMessage()
    msg['Subject'] = f"Reminder: It's {', '.join(p['name'] for p in birthday_people)}'s birthday today!"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = other['email']
    msg.set_content(f"Hey {other['name']},\n\nJust a reminder that today is {', '.join(p['name'] for p in birthday_people)}'s birthday!\nDon't forget to send your wishes 🎈")
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print(f"Sent reminder to {other['name']}")