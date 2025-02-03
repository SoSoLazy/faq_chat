import os

from services.llm_service import LLMService

# 스마트 스토어 사용자 관점 관점

TEST_NAME = "chat_demo_1"
REQUEST_MESSAGE_LIST = [
    "회원가입 어떻게 함?",
    "회원가입은 했는데 개인정보를 바꾸고싶어",
    "구매한 상품을 취소하고 싶어요",
    "판매자 정보는 어디서 봐요",
]

def test_chat_demo_1():
    ret = ""
    session_id = None

    for chat_num, request_message in enumerate(REQUEST_MESSAGE_LIST):
        response = LLMService.get_instance().chat_session(
            request_message, session_id
        )
    
        session_id = response.session_id

        ret += f"--------------[CHAT COUNT : {chat_num + 1}]--------------"
        ret += f"\nREQUEST:\n{request_message}"
        ret += f"\n\nRESPONSE:\n{response.message}"
        ret += f"\n\nADDITINONAL_QUESTIONS:\n{response.additional_questions}"
        ret += "\n\n"
        
    with open(os.path.join("test", f"{TEST_NAME}.text"), "w") as f:
        f.write(ret)