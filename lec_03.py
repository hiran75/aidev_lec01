
import streamlit as st             # 챗봇 웹 화면을 만드는 라이브러리

import os                          # 환경변수에서 키 문자열을 꺼낼 때 사용
from dotenv import load_dotenv     # .env 파일을 읽어 오는 함수

from openai import OpenAI          # API를 호출할 클라이언트

load_dotenv()                      # 같은 폴더의 .env를 읽어 환경변수로 올림
api_key = os.getenv("OPENAI_API_KEY")  # .env에 적어 둔 키를 변수로 꺼냄

client = OpenAI(api_key=api_key)  # 그 키를 넣어 API 접속 창구를 만듦

# 대화 목록이 없으면 빈 리스트로 시작. 새로고침 전까지 이 목록이 유지됨
if "messages" not in st.session_state:
    st.session_state.messages = []

# 지금까지 쌓인 대화를 화면에 말풍선으로 다시 그림
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):  # user 또는 assistant
        st.write(msg["content"])        # 그 말의 내용

# 화면 아래 입력창. 엔터 전이면 prompt는 비어 있음
prompt = st.chat_input("메시지를 입력하세요")

if prompt:  # 사용자가 글을 보냈을 때만 아래를 실행
    # 1) 사용자 말을 대화 목록에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    # 2) 대화 전체를 API로 보내 답을 요청
    response = client.responses.create(
        model="gpt-5.4-mini",                 # 사용할 모델
        input=st.session_state.messages,  # 지금까지의 대화
    )
    # 3) 응답 객체에서 답 문장만 꺼냄
    answer = response.output_text
    # 4) AI 답도 목록에 저장해 다음 화면에서 다시 보이게 함
    st.session_state.messages.append({"role": "assistant", "content": answer})
    # 5) 방금 받은 답을 챗봇 화면에 바로 출력
    with st.chat_message("assistant"):
        st.write(answer)