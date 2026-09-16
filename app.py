import os

import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


# Load the .env file
load_dotenv()


# Streamlit page settings
st.set_page_config(
    page_title="PULLUP",
    page_icon="🫵",
    layout="centered"
)


# App heading
st.title("🫵 PULLUP")
st.subheader("Your group chat, but actually useful.")
st.caption("Tell me the vibe. I'll turn the chaos into a plan. 💀")


# Read Google API key
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error(
        "Missing GOOGLE_API_KEY. Add GOOGLE_API_KEY to your .env file "
        "and restart the app."
    )
    st.stop()


# Gemini model
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0.7,
    google_api_key=api_key
)


# Sidebar
with st.sidebar:
    st.header("👯 Your squad")

    people = st.text_area(
        "Who's coming?",
        value="Aisha, Rohan, Simran, Me"
    )

    budget = st.number_input(
        "💸 Budget per person (₹)",
        min_value=0,
        value=800,
        step=100
    )

    city = st.text_input(
        "📍 City",
        value="Bengaluru"
    )

    vibe = st.selectbox(
        "✨ Vibe",
        [
            "Chill",
            "Foodie",
            "Party",
            "Adventure",
            "Aesthetic",
            "Cheap & chaotic"
        ]
    )

    time_available = st.text_input(
        "⏰ Time",
        value="6 PM – 11 PM"
    )


# Main request area
st.markdown("### What's the plan?")

request = st.text_area(
    "💬 Tell PULLUP what's going on",
    placeholder=(
        "bro we're bored, 4 people are free, "
        "we have ₹800 each..."
    )
)


# Quick request options
quick_request = st.selectbox(
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

if quick_request != "Choose..." and not request.strip():
    request = quick_request


# One unique button only
generate_clicked = st.button(
    "PULL US UP 🚀",
    use_container_width=True,
    key="pullup_generate_button"
)


if generate_clicked:

    if not request.strip():
        st.warning("Please tell PULLUP what is going on first.")

    else:

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
You are PULLUP, a Gen-Z group-planning AI.

Turn messy group-chat energy into a realistic and useful plan.

Be fun, concise and natural. Use light Gen-Z language,
but do not overdo slang.

Never invent exact live prices, opening hours, availability,
bookings, addresses, or facts that were not provided by the user.

If current details are needed, clearly say that the user
should check them before going.

Return only clean, human-readable Markdown.

Do not return JSON.
Do not return Python objects.
Do not include fields such as type, text, extras, svg, or signature.

Use exactly these sections:

## Verdict
One fun one-line verdict.

## Plan
A practical plan with times.

## Estimated Budget
Estimated spending per person. Clearly label all estimates.

## Backup Plan
One alternative plan.

## Group Chat Message
A short message the user can copy and paste.

Use the supplied city, people, budget, vibe and time window.
Stay within the user's budget where possible.
"""
                ),
                (
                    "human",
                    """
CITY: {city}

PEOPLE: {people}

BUDGET PER PERSON: ₹{budget}

VIBE: {vibe}

TIME: {time_available}

REQUEST: {request}
"""
                )
            ]
        )

        with st.spinner("Cooking the plan... 🍳"):

            chain = prompt | llm

            result = chain.invoke(
                {
                    "city": city,
                    "people": people,
                    "budget": budget,
                    "vibe": vibe,
                    "time_available": time_available,
                    "request": request
                }
            )

        st.markdown("## 🧃 PULLUP says:")

        # Extract only the actual text from the model response
        answer = result.content

        if isinstance(answer, list):

            text_parts = []

            for item in answer:

                if isinstance(item, dict):
                    text_value = item.get("text", "")

                    if text_value:
                        text_parts.append(str(text_value))

                elif isinstance(item, str):
                    text_parts.append(item)

            answer = "\n\n".join(text_parts)

        elif isinstance(answer, dict):
            answer = answer.get("text", "")

        else:
            answer = str(answer)

        if not answer.strip():
            st.error("PULLUP returned an empty response. Please try again.")

        else:
            st.markdown(answer)