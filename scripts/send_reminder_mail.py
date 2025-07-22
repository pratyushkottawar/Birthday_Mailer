import csv, datetime, os
from config import CSV_FILE_PATH
from utils import send_html_email, load_template

EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('EMAIL_PASSWORD')

today = datetime.datetime.now().strftime("%d-%m")
TEMPLATE_PATH = "../mail_templates/reminder_mail.html"

birthday_names = []
members_to_notify = []

with open('../CSV_FILE_PATH', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row.get('birthday') == today and row.get('category') in ['surbhikunj']:
            birthday_names.append(row.get('name'))
        elif row.get('category') == 'surbhikunj':
            members_to_notify.append(row.get('email'))

if birthday_names:
    html_body = load_template(TEMPLATE_PATH).replace("{{names}}", "<br>".join(birthday_names))
    for email in members_to_notify:
        send_html_email(
            "📢 Birthday Reminder",
            email,
            html_body,
            EMAIL,
            PASSWORD
        )