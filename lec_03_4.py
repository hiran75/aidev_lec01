#user 입력값
user_msg = {"role": "user", "content": "안녕하세요"}


#ai 응답 결과
ai_response = {
    "id": "msg_123",
    "type": "message",
    "role": "assistant",
    "status": "completed",
    "content": "반가워요! 무엇을 도와드릴가요?"
}


#list에 담기
messages = []
messages.append(user_msg)
messages.append(ai_response)

#usr 입력값 출력
print(messages[0]["role"])
print(messages[0]["content"])

# AI응답 결과 출력
print(messages[1]["role"])
print(messages[1]["content"])


print(messages[0]["role"] + " > " + messages[0]["content"])
print(messages[1]["role"] + " > " + messages[1]["content"])