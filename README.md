# Project Management Agent PoC

LangChain과 LangGraph를 학습하면서  
AI Agent의 Tool Calling과 Agent Loop를 직접 구현해보는 학습용 PoC입니다.

프로젝트 관리 상황을 예시로 사용하지만,  
실제 서비스 구현보다는 AI Agent의 동작 원리를 이해하는 것이 목적입니다.

---

## Learning Goals

- LLM Tool Calling 이해
- LangChain Tool 사용
- 여러 Tool Call 처리
- Tool 결과를 LLM에 다시 전달
- Agent Loop 이해 및 구현
- LangGraph의 State / Node / Edge 이해
- Conditional Edge를 이용한 분기
- Human-in-the-loop 학습

---

## Current Implementation

현재 구현한 기능입니다.

- Python 가상환경 구성
- LangChain + OpenAI API 연동
- Mock Task 데이터 구성
- LangChain Tool 정의
- LLM의 Tool 선택
- Multiple Tool Calls 처리
- Tool 실행
- Tool 결과를 `ToolMessage`로 LLM에 전달
- Tool 결과를 기반으로 자연어 응답 생성
- Agent Loop를 이용한 반복적인 Tool Calling 구현
- LangGraph를 이용한 Agent Loop 구현
- State, Node, Edge, Conditional Edge를 이용한 Tool Calling 흐름 구현
- LangGraph `interrupt()`를 이용한 Human-in-the-loop 구현
- Checkpointer와 `Command(resume=...)`를 이용한 승인/거절 후 그래프 재개 구현

현재 사용 중인 Tool:

### `get_blocked_tasks`

`BLOCKED` 상태인 Task를 조회합니다.

### `get_following_tasks`

특정 Task에 직접 의존하는 후속 Task를 조회합니다.

### `get_available_tasks`

현재 바로 시작할 수 있는 `TODO` Task를 조회합니다.

---

## Example

사용자 입력:

```text
BLOCKED 작업이랑 지금 바로 할 수 있는 작업도 찾아줘
```

LLM이 선택한 Tool:

```text
get_blocked_tasks
get_available_tasks
```

최종 응답 예시:

```text
현재 BLOCKED 상태인 작업은 "예약 API 구현"입니다.
지금 바로 할 수 있는 TODO 상태의 작업은 "관리자 화면"입니다.
```

---

## Current Flow

```text
User Message
↓
LLM
↓
Tool Selection
↓
Tool Execution
↓
Tool Result
↓
ToolMessage
↓
LLM
↓
Final Response
```

---

## Project Structure

```text
project-agent-poc/
├── app.py
├── mock_data.py
├── tools.py
├── tool_calling_test.py
├── .gitignore
├── README.md
├── agent_loop_test.py
├── langgraph_agent_test.py
└── human_in_the_loop_test.py
```

---

## Tech Stack

- Python
- LangChain
- OpenAI API
- LangGraph

학습 예정:

- BLOCKED 복구 시나리오 구현



---

## Roadmap

- [x] Mock Task 데이터 구성
- [x] LangChain Tool 작성
- [x] LLM Tool Calling
- [x] Multiple Tool Calls 처리
- [x] Tool 결과를 LLM에 다시 전달
- [x] 자연어 최종 응답 생성
- [x] Agent Loop 구현
- [x] LangGraph 적용
- [x] State / Node / Edge 실습
- [x] Conditional Edge 실습
- [x] Human-in-the-loop 실습
- [ ] BLOCKED 복구 시나리오 구현

---

## Security

OpenAI API Key는 `.env`에서 관리하며 Git에 포함하지 않습니다.

```text
.env
.venv/
__pycache__/
```
