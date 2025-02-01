
LLM_SESSION_LIMIT_FOR_CHAT = 8 # 응답에 활용하기 위한 과거 채팅 수
LLM_THRESHOLD_FOR_VALID_REQUEST = 1
LLM_NONE_FAQ_REQUEST_MESSAGE = "저는 스마트 스토어 FAQ를 위한 챗봇입니다. 스마트 스토어에 대한 질문을 부탁드립니다."

RAG_DB_PATH = "databases/chroma_db"
RAG_COLLECTION_NAME = "faq_rag"
RAG_DATA_FILE_PATH="data/final_result.csv"

SESSION_DB_PATH = "databases/sqlite.db"
SESSION_TABLE_NAME = "chat_history"
SESSION_CONFLICT_COLUMNS = "session_id"
SESSION_COLUMNS = """
session_id STRING PRIMARY KEY,
chat_history_list STRING
"""