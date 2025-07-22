import smtplib
import csv
import datetime
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os

def send_birthday_email(name, to_email, email_user, email_pass):
    msg = MIMEMultipart("related")
    msg['Subject'] = f"🎉 Happy Birthday {name}!"
    msg['From'] = email_user
    msg['To'] = to_email

    # HTML body with embedded image reference
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif;">
        <h2>🎂 Happy Krishna Conscious Birthday, {name} 🎂</h2>
        <p>Whether you're still at <span style="font-weight: bold; color: #1b5e20; font-style: italic;">Surbhikunj VOICE</span> or were part of it before, you're always one of us. The bond we’ve shared in this beautiful space built on service, association, and smiles stays forever.</p>
        <p>On this special day, we all pray that you make swift advancement in Krishna consciousness. </p>
        <p>🙏 May SSRKB, SSGN, Srila Prabhupada, and all the Vaishnavas bless you with their choicest blessings.</p>
        <img src="cid:birthdayimage" width="400" style="border-radius: 10px;" />
        <div style="margin-top: 30px; padding: 15px; border-left: 4px solid #4CAF50; background-color: #f1f8f4;">
            <p style="margin: 0; font-size: 16px; font-weight: bold; color: #2e7d32;">
            — Your <span style="font-family: 'Georgia', serif; font-style: italic; color: #1b5e20;">Surbhikunj VOICE</span> Family
            </p>
        </div>
      </body>
    </html>
    """

    msg.attach(MIMEText(html, 'html'))

    try:
        with open("birthday_image.jpg", "rb") as img:
            mime_img = MIMEImage(img.read())
            mime_img.add_header("Content-ID", "<birthdayimage>")
            msg.attach(mime_img)
    except Exception as e:
        print(f"⚠️ Could not attach image: {e}")

    try:
        print(f"📤 Sending birthday email to {to_email}")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=20) as server:
            server.login(email_user, email_pass)
            server.send_message(msg)
            print(f"✅ Birthday mail sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send birthday email to {to_email}. Error: {e}")


def send_text_email(subject, body, to_email, email_user, email_pass):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = email_user
    msg['To'] = to_email

    try:
        print(f"📤 Sending reminder email to {to_email}")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=20) as server:
            server.login(email_user, email_pass)
            server.send_message(msg)
            print(f"✅ Reminder mail sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send reminder mail to {to_email}. Error: {e}")


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

    with open('birthdays_test.csv', newline='') as csvfile:
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
        send_birthday_email(person['name'], person['email'], email_user, email_pass)

    # Send reminder to others
    reminder_subject = "📢 Birthday Reminder"
    reminder_body = "Hare Krishna 😁,\n\nJust a reminder that today is the birthday 🎂 of:\n"
    reminder_body += '\n'.join([f"- {p['name']}" for p in birthday_people])
    reminder_body += "\n\nDon't forget to wish them! 🎉"

    for member in other_members:
        send_text_email(reminder_subject, reminder_body, member['email'], email_user, email_pass)

    print("✅ All mails processed. Job complete.")


if __name__ == "__main__":
    main()