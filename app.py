
#streamlit run app.py

import streamlit as st             # 웹 화면을 만드는 라이브러리
import os                          # 환경변수에서 키 문자열을 꺼낼 때 사용
from dotenv import load_dotenv     # .env 파일을 읽어 오는 함수
from openai import OpenAI          # API를 호출할 클라이언트
from ai import ask                 # ai.py에 만들어 둔 질문 함수

load_dotenv()                      # 같은 폴더의 .env를 읽어 환경변수로 올림
api_key = os.getenv("OPENAI_API_KEY")


#챗봇 디자인 추가(2026.10.14)

# 1) 페이지 기본 설정 (반드시 다른 st 명령보다 먼저 호출)
st.set_page_config(page_title="리빠나 챗봇", page_icon="🤖", layout="centered")

# 2) CSS로 화면 꾸미기
st.markdown("""
<style>
    /* 제목 영역 그라데이션 박스 */
    .chat-header {
        background: linear-gradient(90deg, #6a5acd, #00bfff);
        padding: 18px 24px;
        border-radius: 14px;
        color: white;
        margin-bottom: 16px;
    }
    .chat-header h2 { margin: 0; color: white; }
    .chat-header p  { margin: 4px 0 0 0; opacity: 0.9; }

    /* 말풍선 모양 */
    [data-testid="stChatMessage"] {
        border-radius: 14px;
        padding: 10px 14px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="chat-header">
    <h2>🤖 안녕하세요, 리빠나입니다</h2>
    <p>파이썬만으로 만든 첫 AI 챗봇입니다 ^^</p>
</div>
""", unsafe_allow_html=True)

# 3) 사이드바: 설정 / 대화 초기화
USER_AVATAR = "🧑"
BOT_AVATAR = "🤖"

with st.sidebar:
    st.header("⚙️ 설정")
    max_len = st.slider("최대 입력 글자 수", 50, 1000, 300, step=50)
    if st.button("🗑️ 대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.caption("Made with Streamlit + OpenAI")


#입력 검사 추가 (2026.10.XX)

BANNED_WORDS = ["바보", "멍청이", "욕설"]   # 금지어 목록 (필요에 따라 추가)

def validate_input(text, max_len):
    """입력값을 검사해서 (통과여부, 메시지)를 돌려준다."""
    text = text.strip()                       # 앞뒤 공백 제거

    if not text:                              # 1) 빈 입력
        return False, "내용을 입력해 주세요."
    if len(text) < 2:                         # 2) 너무 짧은 입력
        return False, "2글자 이상 입력해 주세요."
    if len(text) > max_len:                   # 3) 너무 긴 입력
        return False, f"{max_len}자 이하로 입력해 주세요. (현재 {len(text)}자)"
    for word in BANNED_WORDS:                 # 4) 금지어 포함
        if word in text:
            return False, f"'{word}'는(은) 사용할 수 없는 단어입니다."
    if len(set(text)) == 1:                   # 5) 같은 글자만 반복 (예: ㅋㅋㅋㅋ)
        return False, "의미 있는 문장을 입력해 주세요."

    return True, text                         # 통과하면 정리된 문장을 돌려줌


# API 키가 없으면 더 진행하지 않음
if not api_key:
    st.error("OPENAI_API_KEY가 없습니다. .env 파일을 확인해 주세요.")
    st.stop()

client = OpenAI(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

# 첫 화면 안내 문구
if not st.session_state.messages:
    st.info("👋 무엇이든 물어보세요! 아래 입력창에 메시지를 입력하면 됩니다.")

# 지금까지의 대화 출력
for msg in st.session_state.messages:
    avatar = USER_AVATAR if msg["role"] == "user" else BOT_AVATAR
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

# 새 입력 처리
prompt = st.chat_input("메시지를 입력하세요")
if prompt is not None:
    ok, result = validate_input(prompt, max_len)
    if not ok:
        st.warning(f"⚠️ {result}")            # 검사 실패 → 경고만 띄우고 API 호출 안 함
    else:
        st.session_state.messages.append({"role": "user", "content": result})
        with st.chat_message("user", avatar=USER_AVATAR):
            st.write(result)

        with st.chat_message("assistant", avatar=BOT_AVATAR):
            with st.spinner("답변을 생각하는 중..."):
                try:
                    ai_response = ask(client, st.session_state.messages)
                    answer = ai_response["content"]
                except Exception as e:        # 네트워크/키 오류 등
                    answer = None
                    st.error(f"오류가 발생했습니다: {e}")
            if answer:
                st.write(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
