import streamlit as st
from google import genai
from google.genai import types
from streamlit_mic_recorder import mic_recorder

st.set_page_config(page_title="VISION", page_icon="🤖", layout="centered")

VISION_PROMPT = """You are VISION, an advanced personal AI assistant — intelligent, calm, analytical, warm and honest. 
You support English, Hindi and Marathi, including Hinglish. Respond naturally and concisely.
Never claim to have capabilities you do not have. Be honest about being an AI.
Be proactive but not intrusive. Correct mistakes respectfully. Never fabricate facts, sources or legal provisions.
Adapt mode from context: casual, thinking, learning, professional, personal guidance."""

# Naya Google GenAI Client
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.title("VISION")
st.caption("Your personal AI assistant")

st.session_state.clear()
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=VISION_PROMPT)
    )

# Chat history (Naye library ke hisaab se)
for msg in st.session_state.chat.get_history():
    with st.chat_message(msg.role):
        st.markdown(msg.parts[0].text)

# --- VOICE INPUT ---
st.write("---")
st.write("🎤 **Bolkar poochhein (Mic dabayein):**")
audio = mic_recorder(start_prompt="Start Recording", stop_prompt="Stop & Send", just_once=True, key='recorder')

if audio:
    with st.spinner("Aawaz sun raha hoon..."):
        try:
            audio_bytes = audio['bytes']
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav"),
                    "Transcribe this audio exactly in the language spoken. Do not answer, just transcribe."
                ]
            )
            user_text = response.text.strip()
            
            st.success(f"Aapne kaha: {user_text}")
            
            with st.chat_message("user"):
                st.markdown(user_text)
            with st.chat_message("assistant"):
                ai_response = st.session_state.chat.send_message(user_text)
                st.markdown(ai_response.text)
                
        except Exception as e:
            st.error(f"Error: {e}")
st.write("---")

# Type karke bhejne ka option
if prompt := st.chat_input("Ya yahan type karein..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
