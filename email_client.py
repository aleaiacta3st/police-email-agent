import os
from dotenv import load_dotenv
import resend

load_dotenv(override=True)

resend.api_key = os.getenv("RESEND_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")

def send_email(to, subject, text_body, html_body):
    resend.Emails.send({
        "from": EMAIL_FROM,
        "to": to,
        "subject": subject,
        "text": text_body,
        "html": html_body,
    })

