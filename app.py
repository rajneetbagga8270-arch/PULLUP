import os
import re

import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


# --------------------------------------------------
# Setup
# --------------------------------------------------

load_dotenv()

st.set_page_config(
    page_title="PULLUP",
    page_icon="🫵",
    layout="centered",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# Custom styling
# --------------------------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background: linear-gradient(
            135deg,
            #fff1f8 0%,
            #f3e8ff 48%,
            #e0f2fe 100%
        );
    }

    .main-title {
        text-align: center;
        font-size: 58px;
        font-weight: 800;
        color: #7c3aed;
        margin-top: 10px;
        margin-bottom: 0;
    }

    .subtitle {
        text-align: center;
        color: #4b5563;
        font-size: 17px;
        margin-bottom: 24px;
    }

    .intro-card {
        background: rgba(255, 255, 255, 0.82);
        border: 1px solid rgba(124, 58, 237, 0.15);
        border-radius: 24px;
        padding: 22px;
        margin-bottom: 24px;
        box-shadow: 0 8px 24px rgba(124, 58, 237, 0.08);
    }

    .intro-card h3 {
        color: #6d28d9;
        margin-top: 0;
    }

    .small-note {
        color: #6b7280;
        font-size: 13px;
    }

    .stButton > button {
        border: none;
        border-radius: 18px;
        background: linear-gradient(90deg, #7c3aed, #ec4899);
        color: white;
        font-weight: 700;
        font-size: 16px;
        padding: 12px;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        transform: scale(1.02);
        color: white;
        background: linear-gradient(90deg, #6d28d9, #db2777);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f5f3ff, #fce7f3);
    }

    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 16px;
        padding: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    '<div class="main-title">🫵 PULLUP</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your group chat, but actually useful. 💀</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="intro-card">
        <h3>✨ From chaotic chats to actual plans</h3>
        <p>
        Tell PULLUP your city, budget, squad and vibe.
        It will turn the chaos into a practical plan with timings,
        estimated spending, a backup option and a ready-to-send message.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# API key
# --------------------------------------------------

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error(
        "Missing GOOGLE_API_KEY. Add it to your .env file and restart the app."
    )
    st.stop()


# --------------------------------------------------
# Gemini model
# --------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0.7,
    google_api_key=api_key
)


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:
    st.header("👯 Your squad")

    people = st.text_area(
        "Who's coming?",
        value="Aisha, Rohan, Simran, Me"
    )

    budget = st.number_input(
        "💸 Budget per person",
        min_value=0,
        value=800,
        step=100
    )

    st.caption(f"Your budget: ₹{budget} per person")

    budget_progress = min(int((budget / 2000) * 100), 100)

    st.progress(
        budget_progress,
        text="Budget level"
    )

    city = st.text_input(
        "📍 City",
        value="Bengaluru"
    )

    vibe = st.selectbox(
        "✨ What's the vibe?",
        [
            "🌿 Chill",
            "🍔 Foodie",
            "🪩 Party",
            "🏔️ Adventure",
            "📸 Aesthetic",
            "💀 Cheap & chaotic"
        ]
    )

    time_available = st.text_input(
        "⏰ Available time",
        value="6 PM – 11 PM"
    )


# --------------------------------------------------
# Main request
# --------------------------------------------------

st.markdown("### 💬 What's happening?")

request = st.text_area(
    "Tell PULLUP what your group wants",
    placeholder=(
        "bro we're bored, 4 people are free, "
        "we have ₹800 each and want food and games..."
    ),
    height=130
)


# --------------------------------------------------
# Example prompts
# --------------------------------------------------

st.markdown("#### Need inspiration? Try one 👇")

col1, col2, col3 = st.columns(3)

with col1:
    food_clicked = st.button("🍔 Food plan", key="food_example")

with col2:
    games_clicked = st.button("🎮 Games night", key="games_example")

with col3:
    photo_clicked = st.button("📸 Photo day", key="photo_example")

if food_clicked:
    request = "Plan an affordable food outing for our group."

elif games_clicked:
    request = "Plan a fun games and food evening."

elif photo_clicked:
    request = "Plan an aesthetic day out with good photo opportunities."


# --------------------------------------------------
# Generate button
# --------------------------------------------------

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
You are PULLUP, a fun and practical Gen-Z group-planning AI.

Turn messy group-chat energy into a realistic plan.

Be friendly, concise and natural. Use light Gen-Z language,
but do not overdo slang.

Never invent exact live prices, opening hours, availability,
bookings, addresses or facts that were not provided by the user.

If current information is needed, clearly tell the user to check it.

Use the user's city, people, budget, vibe and available time.

Return only clean, human-readable Markdown.

Do not return JSON.
Do not return Python objects.
Do not include fields such as type, text, extras, svg or signature.

Use exactly these sections:

## Verdict
One fun one-line verdict.

## Plan
A practical plan with timings.

## Estimated Budget
Estimated spending per person. Clearly label estimates.

## Backup Plan
One alternative plan.

## Group Chat Message
A short message that can be copied and sent to the group chat.

Stay within the given budget where possible.
"""
                ),
                (
                    "human",
                    """
CITY: {city}

PEOPLE: {people}

BUDGET PER PERSON: ₹{budget}

VIBE: {vibe}

TIME AVAILABLE: {time_available}

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

        # --------------------------------------------------
        # Extract only the actual text response
        # --------------------------------------------------

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

        # Remove accidental JSON-style wrappers if they appear
        answer = answer.strip()

        answer = re.sub(
            r'^\s*\[\s*\{\s*"type"\s*:\s*"text"\s*,\s*"text"\s*:\s*"',
            "",
            answer
        )

        if not answer:
            st.error("PULLUP returned an empty response. Please try again.")

        else:

            st.markdown("## 🧃 PULLUP says:")

            with st.container(border=True):
                st.markdown(answer)

            st.success("Your plan is ready. Send it to the group chat 🚀")

            # Extract the group message for easy copying
            if "## Group Chat Message" in answer:

                group_message = answer.split(
                    "## Group Chat Message",
                    1
                )[1].strip()

                st.markdown("### 📲 Copy this to your group chat")

                st.code(
                    group_message,
                    language="text"
                )

            st.balloons()


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.markdown(
    """
    <div style="
        text-align: center;
        color: #6b7280;
        padding: 35px 0 10px 0;
        font-size: 13px;
    ">
        Made with 💀, Python and Gemini · PULLUP
    </div>
    """,
    unsafe_allow_html=True
)