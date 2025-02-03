import os

from services.llm_service import LLMService

# 스마트 스토어 운영자 관점

TEST_NAME = "chat_demo_2"
REQUEST_MESSAGE_LIST = [
    "나는 판매자인데 접속이 되지 않아요",
    "판매자 정보는 어디서 봐요",
    "쿠폰을 발행하고 싶어요",
    "부자가 되고 싶어요"
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