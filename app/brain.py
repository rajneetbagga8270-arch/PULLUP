import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

SYSTEM_PROMPT = """
You are PULLUP, an AI assistant for chaotic group chats.

You remember the conversation and help users understand what is happening.

For every request:
- summarize important information
- identify plans
- identify decisions
- identify pending/unanswered things
- identify tasks and who is responsible
- identify dates, times and locations
- never invent information

Style:
- Gen-Z but natural
- concise
- friendly
- useful
- occasional emojis
"""


def ask_pullup(conversation, user_message):

    prompt = f"""
{SYSTEM_PROMPT}

CONVERSATION MEMORY:
{conversation}

NEW USER MESSAGE:
{user_message}

Use the conversation memory to answer the new message.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":

    print("🧠 PULLUP BRAIN ONLINE")
    print("Type messages normally.")
    print("Type 'exit' to quit.\n")

    conversation = ""

    while True:

        user_message = input("You: ")

        if user_message.lower().strip() == "exit":
            print("\nPULLUP: Catch you later 👋")
            break

        conversation += f"\nUser: {user_message}"

        try:
            answer = ask_pullup(conversation, user_message)

            print("\nPULLUP:", answer)
            print()

            conversation += f"\nPULLUP: {answer}"

        except Exception as e:
            print("\n❌ Error:", e)