import streamlit as st             # 챗봇 웹 화면을 만드는 라이브러리

messages = []
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

    #list에 담기
    user_msg = {"role": "user", "content": prompt}   
    messages.append(user_msg)
    messages.append(ai_response)
    
else:
    answer = ""
    
if prompt:
    for msg in messages:
        st.write(msg["role"] + " >> " + msg["content"]) 
     
# if prompt:    #같은 효과
#     st.write(messages[0]["role"]+ " >> " + messages[0]["content"])
#     st.write(messages[1]["role"] + " >> " + messages[1]["content"])

