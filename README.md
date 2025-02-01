# FAQ chatbot project
FAQ 응대 챗봇 만들기

## 주요 기능 정리
### RAG를 활용한 답변
제공된 데이터와 chroma DB를 활용하여 RAG를 구축하였습니다.

### 세션 기능
모든 대화 기록은 sqlite DB에 저장되며
session_id를 활용하여 과거 채팅을 이어서 할 수 있습니다.
이 때 챗봇은 과거 채팅 기록에서 맥락을 기반한 답변을 합니다.

### 스마트 스토어와 무관한 질문 회피
RAG와 임계값을 활용하여, 스마트 스토어와 무관한 질문이 온 경우, 답변을 하지 않도록 하였습니다.

# Architecure

# Environment

# Build & Run & Test

## Build & Run
pyenv local 3.12
python install poetry
poetry install
poetry run python main.py

## Test: 모든 API는 postman을 통해 실험하도록 세팅하였습니다.

# Api-Spec

## /llm

## /admin