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

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Models ki list (Agar ek busy ho toh dusra try karega)
MODELS = ["gemini-3.8-flash", "gemini-2.5-flash", "gemini-1.5-flash"]

st.title("VISION")
st.caption("Your personal AI assistant")

st.session_state.clear()

if "chat" not in st.session_state:
    # Pehla model try karega
    st.session_state.chat = client.chats.create(
        model=MODELS[0],
        config=types.GenerateContentConfig(system_instruction=VISION_PROMPT)
    )
    st.session_state.current_model_index = 0

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
                model=MODELS[0], # Voice ke liye pehla model
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

# --- SMART TEXT INPUT ---
if prompt := st.chat_input("Ya yahan type karein..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        success = False
        # Fallback Loop: Busy hone par dusre model par switch karega
        for i in range(st.session_state.current_model_index, len(MODELS)):
            try:
                response = st.session_state.chat.send_message(prompt)
                st.markdown(response.text)
                success = True
                break # Agar jawab mil gaya toh loop se bahar
            except Exception as e:
                if "503" in str(e) or "UNAVAILABLE" in str(e):
                    # Agar model busy hai toh naya model try karo
                    st.session_state.current_model_index = i + 1
                    if st.session_state.current_model_index < len(MODELS):
                        st.session_state.chat = client.chats.create(
                            model=MODELS[st.session_state.current_model_index],
                            config=types.GenerateContentConfig(system_instruction=VISION_PROMPT)
                        )
                        continue # Naya model try karo
                st.error(f"Error: {e}") # Agar aur koi error ho toh dikhao
                success = True
                break
        
        if not success:
            st.error("Sorry, abhi sabhi AI models busy hain. Thodi der baad try karein.")
