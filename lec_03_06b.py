import streamlit as st             # 챗봇 웹 화면을 만드는 라이브러리

#messages = []  ->   st.session_state.messages 로 변경
if "messages" not in st.session_state:
    st.session_state.messages = []

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
    
    # messages.append(user_msg)
    # messages.append(ai_response)
    
    st.session_state.messages.append(user_msg)
    st.session_state.messages.append(ai_response)
    
else:
    answer = ""
    
if prompt:
    # for msg in messages:
    #     st.write(msg["role"] + " >> " + msg["content"]) 
    
    for msg in st.session_state.messages:
        st.write(msg["role"] + " >> " + msg["content"])
        


