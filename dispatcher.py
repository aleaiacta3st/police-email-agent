import os
from dotenv import load_dotenv
from agents import Agent, Runner, SQLiteSession
import asyncio
from email_client import send_email

load_dotenv(override=True)

MODEL_NAME = "gpt-5.4-mini"

instructions = """
You are a police dispatcher who is the first point of contact 
to anyone who contacts the police through email. Your email style 
is very cop-like and clinical and your goal is to extract information 
as smoothly as possible from the citizens and decide on what to do next.
"""

dispatcher_agent = Agent(name="Dispatcher Agent", instructions=instructions, model=MODEL_NAME)

if __name__ == "__main__":
    async def main():
        session = SQLiteSession("case_001", "memory.db")
        result = await Runner.run(
            dispatcher_agent,
            input="Someone stole my laptop from a coffee shop",
            session=session,
        )
        send_email("invicinc@gmail.com", "Crime Report Received", result.final_output, "")
        print("Email sent!")

    asyncio.run(main())




