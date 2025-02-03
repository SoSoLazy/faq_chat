# FAQ chatbot
FAQ 응대 챗봇

## 주요 기능 정리
### RAG를 활용한 답변
Chroma DB를 기반으로 RAG(Retrieval-Augmented Generation) 시스템을 구축하여, 보다 정확하고 맥락에 맞는 답변을 제공합니다.

### 세션 기능
모든 대화 기록은 SQLite DB에 저장되며, session_id를 활용하여 사용자가 이전 대화를 이어갈 수 있습니다.
챗봇은 과거 채팅 기록을 참고하여 맥락을 반영한 답변을 제공합니다.

### 스마트 스토어와 무관한 질문 필터링
RAG와 임계값을 활용하여 스마트 스토어와 관련 없는 질문이 들어올 경우, 응답하지 않도록 설정하였습니다.

### 추가 예상 질문 생성
채팅 기록과 메타데이터를 활용하여, 사용자가 다음에 할 가능성이 높은 질문을 예측하고 추천하도록 구현하였습니다.

# Architecure
```bash
.
├── data  # RAG(검색 증강 생성, Retrieval-Augmented Generation)에 사용될 데이터 저장
│   └── final_result.pkl
├── README.md
├── clients  # 외부 API 및 데이터베이스 클라이언트 모듈
│   ├── chroma.py
│   ├── open_ai.py
│   └── sqlite.py
├── config.py
├── databases  # 데이터베이스 관련 파일
│   ├── chroma_db
│   └── sqlite.db
├── main.py
├── models  # ORM 모델 정의 (데이터베이스 테이블 구조)
│   └── chat_history.py
├── poetry.lock
├── pyproject.toml
├── routers  # FastAPI의 엔드포인트 (API 라우터) 모음
│   ├── admin.py # 테스트용
│   ├── health.py # 테스트용
│   └── llm.py
├── schemas  # 데이터 모델과 API 요청/응답 형식을 정의하는 Pydantic 스키마
│   ├── chat_history.py
│   └── llm_model.py
├── services  # 비즈니스 로직을 처리하는 서비스 계층
│   ├── llm_service.py
│   ├── rag_service.py
│   └── session_service.py
└── vscode
    └── setting.json
```

# Environment
```bash
# pyenv 환경 설정
pyenv install 3.12
pyenv local 3.12

# poetry & python package 환경설정
python -m install poetry
poetry install --no-root

# openai key 환경변수 추가
export=OPENAI_API_KEY={YOUR_OPENAI_AIP_KEY}
```

# Build & Run
```bash
poetry run python main.py
```

# Api-Spec
```bash
http://localhost:8000/docs
```


