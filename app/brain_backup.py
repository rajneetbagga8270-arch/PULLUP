import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """
You are PULLUP, an AI assistant for chaotic group chats.

Analyze the entire conversation and return:

📌 SUMMARY
🏨/📍 PLANS
✅ DECISIONS
⏳ STILL NEEDED
👤 TASKS

Be concise, natural and Gen-Z friendly.
Never invent information that isn't in the chat.
"""


def analyze_chat(chat):
    prompt = f"""
{SYSTEM_PROMPT}

GROUP CHAT:
{chat}

Analyze this conversation.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":
    print("🧠 PULLUP BRAIN ONLINE")
    print("Paste your group chat below.")
    print("Type END when you're finished.\n")

    messages = []

    while True:
        message = input("Chat: ")

        if message.strip().upper() == "END":
            break

        messages.append(message)

    chat = "\n".join(messages)

    print("\n🚀 PULLUP IS THINKING...\n")

    try:
        result = analyze_chat(chat)
        print(result)
    except Exception as e:
        print("Error:", e)