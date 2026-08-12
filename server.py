from fastapi import FastAPI, Request
import os
import uuid
from dotenv import load_dotenv
import resend
from agents import Agent, Runner, SQLiteSession
from police_agents import dispatcher_agent, assault_agent, cybercrime_agent, theft_agent, officers
from email_client import send_email
from utils import extract_case_id, clean_subject, extract_category
from datetime import datetime


load_dotenv(override=True)
resend.api_key = os.getenv("RESEND_API_KEY")

app = FastAPI()



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
        timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        dispatcher_input = f"[Received: {timestamp}]\n\n{body}"
        result = await Runner.run(dispatcher_agent, input=dispatcher_input)
        original_subject = clean_subject(subject)
        category=result.final_output.category
        reply_subject = f"Re: [Case #{case_id}] [{category}] {original_subject}"
        send_email(sender, reply_subject, result.final_output.message, "", message_id)

        session = SQLiteSession(case_id, "memory.db")
        result=await Runner.run(officers[category], input=body, session=session)
        send_email(sender, reply_subject, result.final_output, "", message_id)
    else:
        category = extract_category(subject)
        session = SQLiteSession(case_id, "memory.db")
        result = await Runner.run(officers[category], input=body, session=session)
        original_subject = clean_subject(subject)
        reply_subject = f"Re: [Case #{case_id}] [{category}] {original_subject}"
        send_email(sender, reply_subject, result.final_output, "", message_id)


    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


