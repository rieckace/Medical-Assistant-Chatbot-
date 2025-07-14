import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

import os

# Retrieve the Groq API Key from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Check if API key is found
if not GROQ_API_KEY:
    st.error("🚨 GROQ_API_KEY not found in environment variables.")
    st.stop()

# Initialize the Groq OpenAI-compatible client
client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# Streamlit Page Configuration
st.set_page_config(
    page_title="Goal-based Medical Assistant",
    layout="centered"
)

st.title("📱 Goal-based Medical Assistant")
st.markdown("""
Describe your health condition or symptoms in detail.  
The assistant will:
- 🟥 Recommend **Emergency Visit** for severe symptoms  
- 🟨 Suggest a **Doctor Appointment** for moderate symptoms  
- 🟩 Advise **Rest & Home Care** for mild issues  
""")

# Text input from the user
user_input = st.text_area("📝 How are you feeling? Describe your symptoms below:")

# Session state to store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Handle user input
if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.spinner("🔍 Analyzing your condition..."):
        try:
            # Message history with system instruction
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a goal-based medical assistant. Your task is to analyze the user's health condition "
                        "and provide appropriate advice based on their symptoms:\n"
                        "1️⃣ If symptoms are **severe** (e.g., chest pain, difficulty breathing, high fever), recommend an **emergency visit**.\n"
                        "2️⃣ If symptoms are **moderate** (e.g., persistent pain, mild fever, rash), suggest a **doctor's appointment**.\n"
                        "3️⃣ If symptoms are **mild** (e.g., fatigue, slight cold), advise **rest and home care**.\n"
                        "Always provide self-care tips if possible."
                    )
                }
            ] + st.session_state.chat_history

            # Groq model call
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                temperature=0.6,
                messages=messages,
                max_tokens=800
            )

            ai_reply = response.choices[0].message.content.strip()
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": ai_reply
            })

            st.success("✅ Recommendations")
            st.markdown(ai_reply)

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")

# Display the full chat history
with st.expander("🧾 Chat History", expanded=False):
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"**👤 You:** {message['content']}")
        elif message["role"] == "assistant":
            st.markdown(f"**🤖 AI:** {message['content']}")
