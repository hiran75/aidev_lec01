import streamlit as st             # 챗봇 웹 화면을 만드는 라이브러리

prompt = st.chat_input("메시지를 입력하세요")

if prompt:
    #ai 응답 결과
    ai_response = {
        "id": "msg_123",
        "type": "message",
        "role": "assistant",
        "status": "completed",
        "content": "반가워요! 무엇을 도와드릴가요?"
    }
    answer = ai_response["role"] + " >> " + ai_response["content"]
else:
    answer = ""

st.write(answer)
