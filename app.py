import streamlit as st
from groq import Groq

st.set_page_config(page_title="VISION", layout="centered", initial_sidebar_state="collapsed")

# WhatsApp jaisa Dark Theme CSS
st.markdown("""
<style>
    /* Background color */
    .stApp {
        background-color: #0b141a; /* WhatsApp dark background */
        color: #e9edef;
    }
    /* Header text style */
    h1 {
        color: #e9edef !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-size: 28px !important;
        text-align: center;
        margin-bottom: 0px;
    }
    .subtitle {
        text-align: center; 
        color: #8696a0; 
        margin-bottom: 30px;
        font-size: 14px;
    }
    /* Input box styling */
    .stChatInputContainer textarea {
        background-color: #2a3942 !important; /* WhatsApp input background */
        color: #e9edef !important;
        border-radius: 25px !important;
        border: none !important;
        padding: 15px !important;
    }
    /* User message bubble */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #005c4b; /* WhatsApp green bubble */
        border-radius: 15px 15px 0px 15px;
        padding: 12px 15px;
        margin-left: auto;
        margin-right: 0;
        width: fit-content;
        max-width: 85%;
    }
    /* Assistant message bubble */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #202c33; /* WhatsApp grey bubble */
        border-radius: 15px 15px 15px 0px;
        padding: 12px 15px;
        margin-right: auto;
        margin-left: 0;
        width: fit-content;
        max-width: 85%;
    }
    /* Hide default avatar icons */
    [data-testid="stChatMessageAvatar"] {
        display: none;
    }
    /* Remove extra padding from chat containers */
    [data-testid="stChatMessage"] {
        border: none;
    }
</style>
""", unsafe_allow_html=True)

VISION_PROMPT = """You are VISION, an advanced personal AI assistant — intelligent, calm, analytical, warm and honest. 
You support English, Hindi and Marathi, including Hinglish. Respond naturally and concisely.
Never claim to have capabilities you do not have. Be honest about being an AI.
Be proactive but not intrusive. Correct mistakes respectfully. Never fabricate facts, sources or legal provisions.
Adapt mode from context: casual, thinking, learning, professional, personal guidance."""

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Header without Emojis
st.markdown("<h1>VISION</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Your personal AI assistant</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": VISION_PROMPT}]

# Chat history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Input and Reply
if prompt := st.chat_input("Message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=st.session_state.messages
            )
            reply = response.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Error: {e}")
