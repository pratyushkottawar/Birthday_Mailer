import csv
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Load environment variables
EMAIL_ADDRESS = os.environ.get("EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")

# Validate email format (basic)
def is_valid_email(email):
    return "@" in email and "." in email

# Send birthday email to the birthday person
def send_birthday_email(name, email):
    subject = "🎉 Happy Birthday!"
    body = f"Dear {name},\n\nWishing you a very Happy Birthday! 🎂🥳\n\nHave a wonderful year ahead!\n\n– Team"

    send_email(email, subject, body)

# Send reminder email to other members
def send_reminder_email(name, email, birthday_people):
    birthday_names = ", ".join([p['name'] for p in birthday_people])
    subject = "🎈 Birthday Reminder"
    body = f"Hi {name},\n\nToday is the birthday of: {birthday_names}.\nDon't forget to send your wishes! 😊\n\n– Team"

    send_email(email, subject, body)

# Core email sending logic
def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

# Main execution
def main():
    today = datetime.now().strftime("%d-%m")
    birthday_people = []
    others = []

    with open("birthdays.csv") as file:
        reader = csv.DictReader(file)
        all_people = list(reader)

    for person in all_people:
        name = person["name"]
        email = person["email"].strip()
        birthday = datetime.strptime(person["birthday"], "%Y-%m-%d").strftime("%d-%m")

        if birthday == today:
            if is_valid_email(email):
                birthday_people.append({"name": name, "email": email})
            else:
                print(f"Skipping birthday email for {name} (invalid or missing email)")
        else:
            if is_valid_email(email):
                others.append({"name": name, "email": email})

    # Send birthday emails
    for person in birthday_people:
        send_birthday_email(person["name"], person["email"])

    # Send reminders to others
    for person in others:
        send_reminder_email(person["name"], person["email"], birthday_people)

if __name__ == "__main__":
    main()
