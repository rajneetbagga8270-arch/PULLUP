import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Gemini API key not found")
    exit()

print("✅ Gemini API key found")
print("Key starts with:", api_key[:6] + "...")


client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Say exactly: PULLUP is alive!"
    )

    print("\n🤖 Gemini says:")
    print(response.text)

except Exception as e:
    print("\n❌ Gemini error:")
    print(e)