import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import mic_recorder

st.set_page_config(page_title="VISION", page_icon="🤖", layout="centered")

VISION_PROMPT = """You are VISION, an advanced personal AI assistant — intelligent, calm, analytical, warm and honest. 
You support English, Hindi and Marathi, including Hinglish. Respond naturally and concisely.
Never claim to have capabilities you do not have. Be honest about being an AI.
Be proactive but not intrusive. Correct mistakes respectfully. Never fabricate facts, sources or legal provisions.
Adapt mode from context: casual, thinking, learning, professional, personal guidance."""

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    system_instruction=VISION_PROMPT
)

st.title("VISION")
st.caption("Your personal AI assistant")

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Chat history dikhane ke liye
for msg in st.session_state.chat.history:
    role = "user" if msg.role == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(msg.parts[0].text)

# --- VOICE INPUT KA NAYA HISA ---
st.write("---")
st.write("🎤 **Bolkar poochhein (Mic dabayein):**")
audio = mic_recorder(start_prompt="Start Recording", stop_prompt="Stop & Send", just_once=True, key='recorder')

if audio:
    with st.spinner("Aawaz sun raha hoon..."):
        try:
            audio_bytes = audio['bytes']
            response = model.generate_content([
                "Transcribe this audio exactly in the language spoken. Do not answer, just transcribe.",
                {"mime_type": "audio/wav", "data": audio_bytes}
            ])
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
# --- VOICE INPUT KHATAM ---

# Type karke bhejne ka option
if prompt := st.chat_input("Ya yahan type karein..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        response = st.session_state.chat.send_message(prompt)
        st.markdown(response.text)
