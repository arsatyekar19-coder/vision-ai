import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="VISION", page_icon="🤖", layout="centered")

VISION_PROMPT = """You are VISION, an advanced personal AI assistant — intelligent, calm, analytical, warm and honest. 
You support English, Hindi and Marathi, including Hinglish. Respond naturally and concisely.
Never claim to have capabilities you do not have. Be honest about being an AI.
Be proactive but not intrusive. Correct mistakes respectfully. Never fabricate facts, sources or legal provisions.
Adapt mode from context: casual, thinking, learning, professional, personal guidance."""

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=VISION_PROMPT
)

st.title("VISION")
st.caption("Your personal AI assistant")

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

for msg in st.session_state.chat.history:
    role = "user" if msg.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(msg.parts[0].text)

if prompt := st.chat_input("Kuch bhi poochhein..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        response = st.session_state.chat.send_message(prompt)
        st.markdown(response.text)
