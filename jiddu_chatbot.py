import streamlit as st
from openai import OpenAI
import os

# Page setup
st.set_page_config(page_title="Jiddu Krishnamurti Chatbot", layout="centered")

st.title("🧘 Chat with Krishnamurti")

# Load API key securely from environment or .env file
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat input box
prompt = st.chat_input("Ask Krishnamurti something...")

# Show past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# On user message
if prompt and client:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # System prompt to instruct the model to act as Krishnamurti
    system_prompt = (
        "You are Jiddu Krishnamurti. Respond thoughtfully, spiritually, and succinctly. "
        "Never exceed 100 words. Embrace clarity, non-authority, and insight."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )

        reply = response.choices[0].message.content.strip()
        st.session_state.messages.append({"role": "assistant", "content": reply})

        with st.chat_message("assistant"):
            st.markdown(reply)

    except Exception as e:
        st.error(f"Error: {e}")
elif prompt and not client:
    st.warning("Please set your OPENAI_API_KEY environment variable.")
