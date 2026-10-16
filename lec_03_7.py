import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask(client, messages):
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=messages,
    )
    msg = response.output[0]
    return {
        "id": msg.id,
        "type": msg.type,
        "role": msg.role,
        "status": msg.status,
        "content": msg.content[0].text,
    }

if "messages" not in st.session_state:
    st.session_state.messages = []

prompt = st.chat_input("메시지를 입력하세요")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    ai_response = ask(client, st.session_state.messages)
    st.session_state.messages.append({
        "role": ai_response["role"],
        "content": ai_response["content"],
    })

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
