import csv, datetime, os
from config import CSV_FILE_PATH
from utils import send_html_email, load_template

EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('EMAIL_PASSWORD')

today = datetime.datetime.now().strftime("%d-%m")
TEMPLATE_PATH = "../mail_templates/surbhikunj_members_birthday_mail.html"

with open('../CSV_FILE_PATH', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row.get('birthday') == today and row.get('category') == 'surbhikunj':
            name = row.get('name')
            to_email = row.get('email')
            html = load_template(TEMPLATE_PATH).replace("{{name}}", name)
            send_html_email(
                f"🎉 Happy Krishna Conscious Birthday {name}!",
                to_email,
                html,
                EMAIL,
                PASSWORD,
                image_path="../images/birthday_image.jpg"
            )