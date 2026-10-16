
import streamlit as st             # 챗봇 웹 화면을 만드는 라이브러리

import os                          # 환경변수에서 키 문자열을 꺼낼 때 사용
from dotenv import load_dotenv     # .env 파일을 읽어 오는 함수

from openai import OpenAI          # API를 호출할 클라이언트

load_dotenv()                      # 같은 폴더의 .env를 읽어 환경변수로 올림
api_key = os.getenv("OPENAI_API_KEY")  # .env에 적어 둔 키를 변수로 꺼냄

print("API 키:", api_key)  # 확인용으로 출력

client = OpenAI(api_key=api_key)  # 그 키를 넣어 API 접속 창구를 만듦

#--------------------------------------------------------------------
def ask(client, messages):
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=messages,
    )
    msg = response.output[0]
    ai_response = {
        "id": msg.id,
        "type": msg.type,
        "role": msg.role,
        "status": msg.status,
        "content": msg.content[0].text,
    }
    return ai_response
#-----------------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []
    
    
prompt = st.chat_input("메시지를 입력하세요")

if prompt:
    #사용자 입력값을 messages에 담기
    user_msg = {"role": "user", "content": prompt}
    st.session_state.messages.append(user_msg)
    
    #AI 호출하기
    ai_response = ask(client, st.session_state.messages)
    
    #AI 응답 결과를 messages에 담기
    st.session_state.messages.append(
    {
        "role": ai_response["role"],
        "content": ai_response["content"],
    }
    )
    
           
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])        