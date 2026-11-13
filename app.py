import streamlit as st
from groq import Groq

st.set_page_config(page_title="VISION", page_icon="🤖", layout="centered")

VISION_PROMPT = """You are VISION, an advanced personal AI assistant — intelligent, calm, analytical, warm and honest. 
You support English, Hindi and Marathi, including Hinglish. Respond naturally and concisely.
Never claim to have capabilities you do not have. Be honest about being an AI.
Be proactive but not intrusive. Correct mistakes respectfully. Never fabricate facts, sources or legal provisions.
Adapt mode from context: casual, thinking, learning, professional, personal guidance."""

# Groq Client Setup
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("VISION")
st.caption("Your personal AI assistant")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": VISION_PROMPT}]

# Purani chat dikhane ke liye
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Naya message aane par
if prompt := st.chat_input("Kuch bhi poochhein..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Groq ka fast model
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Error: {e}")
