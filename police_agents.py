import os
from dotenv import load_dotenv
from agents import Agent, Runner, SQLiteSession
import asyncio
from email_client import send_email
from models import DispatchResult

load_dotenv(override=True)

MODEL_NAME = "gpt-5.4-mini"

instruct_dispatcher = """
You are a police dispatcher. Read the victim's email and classify the crime.

For the category field, respond with exactly one of: assault, cybercrime, theft

For the message field:
- Quote the victim's original message back to them
- Include the date and time the complaint was received
- Tell them they are being routed to the specific unit handling their case 
  (e.g. "assault unit", "cybercrime unit", "theft unit" based on the category)
Your tone is cop-like and clinical.
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


dispatcher_agent = Agent(name="Dispatcher Agent", instructions=instruct_dispatcher, model=MODEL_NAME, output_type=DispatchResult)
assault_agent = Agent(name="Assault Agent", instructions=instruct_assault, model=MODEL_NAME)
cybercrime_agent = Agent(name="Cybercrime Agent", instructions=instruct_cybercrime, model=MODEL_NAME)
theft_agent = Agent(name="Theft Agent", instructions=instruct_theft, model=MODEL_NAME)

officers={
    "assault":assault_agent, 
    "cybercrime":cybercrime_agent,
    "theft":theft_agent
}

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




