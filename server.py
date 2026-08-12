from fastapi import FastAPI, Request
import os
import re
import uuid
from dotenv import load_dotenv
import resend
from agents import Agent, Runner, SQLiteSession
from police_agents import dispatcher_agent
from email_client import send_email

load_dotenv(override=True)
resend.api_key = os.getenv("RESEND_API_KEY")

app = FastAPI()

def extract_case_id(subject):
    match = re.search(r'\[Case #([a-f0-9-]+)\]', subject)
    if match:
        return match.group(1)
    return None

def clean_subject(subject):
    cleaned = re.sub(r'\[Case #[a-f0-9-]+\]', '', subject)
    cleaned = re.sub(r'^(Re:\s*)+', '', cleaned, flags=re.IGNORECASE)
    return cleaned.strip()

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    email_id = data['data']['email_id']
    sender = data['data']['from']
    subject = data['data']['subject']
    message_id = data['data']['message_id']

    email_content = resend.Emails.Receiving.get(email_id=email_id)
    body = email_content['text']

    case_id = extract_case_id(subject)
    if not case_id:
        case_id = str(uuid.uuid4())

    session = SQLiteSession(case_id, "memory.db")
    result = await Runner.run(dispatcher_agent, input=body, session=session)

    original_subject = clean_subject(subject)
    reply_subject = f"Re: [Case #{case_id}] {original_subject}"
    send_email(sender, reply_subject, result.final_output, "", message_id)

    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


