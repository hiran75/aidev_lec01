import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from ai import ask

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

prompt = st.chat_input("메시지를 입력하세요")
if prompt:
    user_msg = {"role": "user", "content": prompt}
    st.session_state.messages.append(user_msg)
    ai_response = ask(client, st.session_state.messages)
    st.session_state.messages.append({
        "role": ai_response["role"],
        "content": ai_response["content"],
    })

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])