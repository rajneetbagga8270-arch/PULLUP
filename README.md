# 🫵 PULLUP

### Your group chat, but actually useful.

PULLUP is a GenAI group-planning assistant. Instead of spending 200 messages deciding what to do, users tell PULLUP their city, people, budget, time and vibe — and it turns the chaos into a realistic plan.

## MVP

- GenAI-powered planning
- Group size / people
- Budget-aware suggestions
- Vibe selection
- Time window
- Backup plan
- Copy-paste group-chat message
- Gen-Z friendly interface

## Tech

Python • Streamlit • Gemini • LangChain

## Run

```bash
conda create -n pullup python=3.11 -y
conda activate pullup
pip install -r requirements.txt
```

Create `.env` from `.env.example` and add your Gemini API key.

Then:

```bash
streamlit run app.py
```

## Product vision

PULLUP can later connect to live maps, weather, events, restaurants, transport and calendars. An agent layer could then build and adapt plans in real time.

## Resume bullet

**PULLUP — GenAI Group Planning Assistant:** Built a GenAI application using Python, Streamlit, Gemini and LangChain that converts group preferences, budget, location and time constraints into personalized activity plans, including fallback options and shareable group-chat messages.

## Future roadmap

V2: live places/events APIs  
V3: shared squad profiles and preferences  
V4: group voting  
V5: calendar integration  
V6: agentic booking workflow  
V7: personalized memory for each squad
