import os
from dotenv import load_dotenv
from agents import Agent, Runner, SQLiteSession
import asyncio
from email_client import send_email

load_dotenv(override=True)

MODEL_NAME = "gpt-5.4-mini"

instruct_dispatcher = """
You are a police dispatcher who is the first point of contact 
to anyone who contacts the police through email. Your email style 
is very cop-like and clinical. You tell the victim to hang on.
 You read the victim's email and decide which agent should take over next.
 Tell them that they will now be talking to the officer dealing with those kind of crimes.
"""

instruct_assault = """
You are a cop who deals with assault, battery those genre of crimes. Talk to the victim
and get the relevant details.
"""

instruct_cybercrime = """
You are a cop who deals with cybercrimes. Talk to the victim
and get the relevant details.
"""

instruct_theft = """
You are a cop who deals with theft and robbery. Talk to the victim
and get the relevant details.
"""


dispatcher_agent = Agent(name="Dispatcher Agent", instructions=instruct_dispatcher, model=MODEL_NAME)
assault_agent = Agent(name="Assault Agent", instructions=instruct_assault, model=MODEL_NAME)
cybercrime_agent = Agent(name="Cybercrime Agent", instructions=instruct_cybercrime, model=MODEL_NAME)
theft_agent = Agent(name="Theft Agent", instructions=instruct_theft, model=MODEL_NAME)

if __name__ == "__main__":
    async def main():
        victim_email = "invicinc@gmail.com"
        session = SQLiteSession(victim_email, "memory.db")
        result = await Runner.run(
            dispatcher_agent,
            input="Someone stole my laptop from a coffee shop",
            session=session,
        )
        send_email(victim_email, "Crime Report Received", result.final_output, "")
        print("Email sent!")

    asyncio.run(main())




