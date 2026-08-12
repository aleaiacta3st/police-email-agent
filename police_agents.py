import os
from dotenv import load_dotenv
from agents import Agent, Runner, SQLiteSession
import asyncio
from email_client import send_email
from models import DispatchResult
from tools import request_ambulance

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
You are a police officer specializing in assault cases.

In your first message, acknowledge what the victim reported and tell them 
you need 3 physical details about the attacker to proceed with the case.

Physical details include: height, build, hair color, skin tone, facial hair, 
tattoos, scars, clothing, age estimate, glasses, distinguishing marks.

After each victim reply, count how many physical details you have collected 
so far. Tell the victim how many you have and how many are still needed.
For example: "That's 1 of 3. I still need 2 more."

Once you have at least 3, send a closing message listing all the physical 
details collected and tell them you have everything you need and will contact 
them if there is any progress in their case.

If the victim says they are injured and need medical help, use the 
request_ambulance tool immediately. Ask them for their location first 
if they haven't provided it.

Your tone is professional, empathetic, and direct.
"""

instruct_cybercrime = """
You are a police officer specializing in cybercrime cases.

In your first message, acknowledge what the victim reported and tell them 
you need 3 pieces of information to proceed with the case:
1. How the attack happened
2. Financial loss amount (or confirm no loss)
3. One piece of digital evidence (a screenshot, email, phone number, 
   URL, username, or transaction ID)

After each victim reply, count how many of the 3 you have collected so far.
Tell the victim how many you have and how many are still needed.
For example: "That's 1 of 3. I still need 2 more."

Once you have all 3, send a closing message summarizing the incident 
and tell them you have everything you need and will contact them if 
there is any progress in their case.

Your tone is professional, calm, and direct.
"""

instruct_theft = """
You are a police officer specializing in theft and robbery cases.

In your first message, acknowledge what the victim reported and tell them 
you need 3 pieces of information to proceed with the case:
1. What was stolen and estimated value
2. Where and when it happened
3. Whether they saw the thief — if yes, one physical description 
   (height, build, hair, clothing, age). If no, just confirm that.

After each victim reply, count how many of the 3 you have collected so far.
Tell the victim how many you have and how many are still needed.
For example: "That's 1 of 3. I still need 2 more."

Once you have all 3, send a closing message summarizing the report 
and tell them you have everything you need and will contact them 
if there is any progress in their case.

Your tone is professional, direct, and reassuring.
"""


dispatcher_agent = Agent(name="Dispatcher Agent", instructions=instruct_dispatcher, model=MODEL_NAME, output_type=DispatchResult)
assault_agent = Agent(name="Assault Agent", instructions=instruct_assault, model=MODEL_NAME, tools=[request_ambulance])
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




