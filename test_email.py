import os
from dotenv import load_dotenv
import resend

load_dotenv(override=True)

resend.api_key = os.getenv("RESEND_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")

print(f"FROM: {EMAIL_FROM}")
print(f"TO: {EMAIL_TO}")

resend.Emails.send({
    "from": EMAIL_FROM,
    "to": EMAIL_TO,
    "subject": "Reporting a crime",
    "text": "Describe the perpetrator",
})

print("Email sent!")