import streamlit as st
from brain import ask_pullup

st.set_page_config(
    page_title="PULLUP",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 PULLUP")
st.caption("Your group chat, but smarter.")

st.divider()

chat = st.text_area(
    "💬 Paste your group chat",
    height=300,
    placeholder="""Rahul: Guys Goa tomorrow?
Priya: YESSS
Aman: Where are we staying?
Rahul: I'll book the hotel.
Priya: Please get somewhere near a beach.
Aman: What time are we leaving?"""
)

if st.button("🚀 ANALYZE CHAT", use_container_width=True):

    if not chat.strip():
        st.warning("Paste some chat first 👀")

    else:
        with st.spinner("PULLUP is thinking... 🧠"):

            try:
                result = ask_pullup(
                    conversation=chat,
                    user_message="Analyze this entire group chat and give me the summary, plans, decisions, things still needed, and tasks."
                )

                st.success("Chat analyzed!")

                st.markdown("### 🧠 PULLUP'S TAKE")
                st.markdown(result)

            except Exception as e:
                st.error(f"Something went wrong: {e}")

st.divider()

st.caption("PULLUP — turning group-chat chaos into clarity.")