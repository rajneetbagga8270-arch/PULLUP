import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

st.set_page_config(page_title="PULLUP", page_icon="🫵", layout="centered")

st.title("🫵 PULLUP")
st.subheader("Your group chat, but actually useful.")
st.caption("Tell me the vibe. I'll turn the chaos into a plan. 💀")

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("Missing GOOGLE_API_KEY. Add it to your .env file and restart the app.")
    st.stop()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

with st.sidebar:
    st.header("👯 Your squad")
    people = st.text_area(
        "Who's coming?",
        "Aisha, Rohan, Simran, Me"
    )
    budget = st.number_input("💸 Budget per person (₹)", min_value=0, value=800, step=100)
    city = st.text_input("📍 City", "Bengaluru")
    vibe = st.selectbox(
        "✨ Vibe",
        ["Chill", "Foodie", "Party", "Adventure", "Aesthetic", "Cheap & chaotic"]
    )
    time_available = st.text_input("⏰ Time", "6 PM – 11 PM")

st.markdown("### What's the plan?")

request = st.text_area(
    "💬 Tell PULLUP what's going on",
    placeholder="bro we're bored, 4 people are free, we have ₹800 each..."
)

quick = st.selectbox(
    "Or pick one 👇",
    [
        "Choose...",
        "Make us a plan for tonight",
        "Give us 3 cheap ideas",
        "Plan a date for the squad",
        "Plan a spontaneous day out",
        "We have no idea what to do 😭"
    ]
)

if quick != "Choose..." and not request:
    request = quick

if st.button("PULL US UP 🚀", use_container_width=True) and request:
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are PULLUP, a Gen-Z group-planning AI.
Your job is to turn messy group-chat energy into a realistic plan.
Be fun, concise and natural. Use light Gen-Z language, but don't overdo slang.
Never invent exact live prices, opening hours, or availability. If current details are needed,
say that they should be checked before booking.

Return:
1. A fun one-line verdict.
2. A concrete plan with times.
3. Estimated budget per person.
4. A backup plan.
5. A short group-chat message the user can copy-paste.

Use the supplied city, people, budget, vibe and time window."""),
        ("human", """CITY: {city}
PEOPLE: {people}
BUDGET PER PERSON: ₹{budget}
VIBE: {vibe}
TIME: {time_available}
REQUEST: {request}""")
    ])

    with st.spinner("Cooking the plan... 🍳"):
        chain = prompt | llm
        result = chain.invoke({
            "city": city,
            "people": people,
            "budget": budget,
            "vibe": vibe,
            "time_available": time_available,
            "request": request
        })

    st.markdown("## 🧃 PULLUP says:")
    st.write(result.content)

st.divider()
st.caption("PULLUP MVP • GenAI group-planning assistant")
