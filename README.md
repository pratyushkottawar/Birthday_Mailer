# Birthday Mailer 🎉

This project automatically sends birthday wishes and reminder emails using GitHub Actions.

## 📅 Features
- Sends a custom birthday mail to the birthday person
- Sends a reminder to the rest of the group
- Uses GitHub Actions to run daily without a PC

## 📂 File Structure
- `birthdays.csv` – List of group members with names, emails, and birthdays
- `birthday_mailer.py` – Python script to process birthdays and send emails
- `.github/workflows/birthday.yml` – GitHub Actions workflow to run the script daily

## 🔐 Secrets Required
Set the following secrets in your GitHub repository:
- `EMAIL`
- `EMAIL_PASSWORD`