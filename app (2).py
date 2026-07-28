
import streamlit as st

import google.generativeai as genai

gemini_api_key = "<>"

genai.configure(api_key=gemini_api_key)


model = genai.GenerativeModel("gemini-3.5-flash")

SYSTEM_PROMPT = """
You are a helpful AI assistant.
Remember details shared in the conversation and answer accordingly.
"""

st.set_page_config(page_title="Memory Chatbot")

st.title("🧠 Parth's Memory Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Ask something...")

if user_input:

    st.session_state.chat_history.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    conversation_text = ""

    for message in st.session_state.chat_history:

        if message["role"] == "user":
            conversation_text += f"User: {message['content']}\n"

        else:
            conversation_text += f"Assistant: {message['content']}\n"

    full_prompt = f"""
{SYSTEM_PROMPT}

{conversation_text}

Assistant:
"""

    try:
        response = model.generate_content(full_prompt)
        assistant_reply = response.text

    except Exception as e:
        assistant_reply = f"Error: {str(e)}"

    st.session_state.chat_history.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )

    st.rerun()

if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()
