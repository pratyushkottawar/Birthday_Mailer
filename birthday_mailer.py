import smtplib
import csv
import datetime
from email.message import EmailMessage
import os

def send_email(subject, body, to_email, email_user, email_pass):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = email_user
    msg['To'] = to_email

    try:
        print(f"Connecting to SMTP server for {to_email}")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=20) as server:
            server.login(email_user, email_pass)
            server.send_message(msg)
            print(f"✅ Mail sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send mail to {to_email}. Error: {e}")

def main():
    print("🔁 Script started...")
    email_user = os.environ.get('EMAIL')
    email_pass = os.environ.get('EMAIL_PASSWORD')

    if not email_user or not email_pass:
        print("❗ Email credentials not found in environment variables.")
        return

    today = datetime.datetime.now().strftime("%d-%m")
    print(f"📅 Today's date: {today}")

    birthday_people = []
    other_members = []

    with open('birthdays.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row.get('name')
            email = row.get('email')
            birthday = row.get('birthday')

            if not email:
                print(f"⚠️ Skipping {name} - no email address provided.")
                continue

            if birthday == today:
                birthday_people.append({'name': name, 'email': email})
            else:
                other_members.append({'name': name, 'email': email})

    if not birthday_people:
        print("📭 No birthdays today. Exiting.")
        return

    for person in birthday_people:
        subject = f"🎉 Happy Birthday {person['name']}!"
        body = f"Dear {person['name']},\n\nWishing you a very Happy Birthday! 🎂🎈🎁\n\nHave a wonderful year ahead!\n\nBest wishes,\nThe Team"
        send_email(subject, body, person['email'], email_user, email_pass)

    reminder_subject = "📢 Birthday Reminder"
    reminder_body = "Hi all,\n\nJust a reminder that today is the birthday of:\n"
    reminder_body += '\n'.join([f"- {p['name']}" for p in birthday_people])
    reminder_body += "\n\nDon't forget to wish them! 🎉"

    for member in other_members:
        send_email(reminder_subject, reminder_body, member['email'], email_user, email_pass)

    print("✅ All mails processed. Job complete.")

if __name__ == "__main__":
    main()
