from fastapi import FastAPI, Request
import os
from dotenv import load_dotenv
import resend
import requests
from agents import Agent, Runner, SQLiteSession
import asyncio
from dispatcher import dispatcher_agent
from email_client import send_email

load_dotenv(override=True)
resend.api_key = os.getenv("RESEND_API_KEY")


app=FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    email_id = data['data']['email_id']
    sender = data['data']['from']
    subject = data['data']['subject']

    email_content = resend.Emails.Receiving.get(email_id=email_id)
    session = SQLiteSession(sender, "memory.db")
    body=email_content['text']
    result = await Runner.run(dispatcher_agent, input=body, session=session)
    send_email(sender, f"Re: {subject}", result.final_output, "")

    return {"status": "ok"}



if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


