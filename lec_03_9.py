

import streamlit as st             # 챗봇 웹 화면을 만드는 라이브러리
import os                          # 환경변수에서 키 문자열을 꺼낼 때 사용
from dotenv import load_dotenv     # .env 파일을 읽어 오는 함수
from openai import OpenAI          # API를 호출할 클라이언트
load_dotenv()                      # 같은 폴더의 .env를 읽어 환경변수로 올림
api_key = os.getenv("OPENAI_API_KEY")  # .env에 적어 둔 키를 변수로 꺼냄



class ChatBot:
    def __init__(self):
        self.client = OpenAI(api_key=api_key)
        if "messages" not in st.session_state:
            st.session_state.messages = []
        self.messages = st.session_state.messages

    def ask(self, prompt):
        self.messages.append({"role": "user", "content": prompt})
        response = self.client.responses.create(
            model="gpt-5.4-mini",
            input=self.messages,
        )
        msg = response.output[0]
        self.messages.append({
            "role": msg.role,
            "content": msg.content[0].text,
        })

    def run(self):
        prompt = st.chat_input("메시지를 입력하세요")
        if prompt:
            self.ask(prompt)
        for msg in self.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

bot = ChatBot()
bot.run()