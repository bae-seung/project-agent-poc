"""
목표
LLM -> Tool 필요? -> Yes -> tool 실행 -> 결과 저장 -> LLM 으로 다시
                 -> No -> 종료
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage,ToolMessage
import json

from tools import (
    get_blocked_tasks,
    get_following_tasks,
    get_available_tasks,
) # tools.py에 있는 Tool 객체들을 현재 파일로 가져오는 것이야. -> U. 아 @tool 이라고 함수 위에 붙이면 Tool 객체가 되는구나.

load_dotenv() # Q.이 부분이 뭘 하는거였지? -> A.프로젝트의 .env 파일을 읽어서 그 안의 값을 환경변수로 등록해주는 함수

tools = [
    get_blocked_tasks,
    get_following_tasks,
    get_available_tasks,
] # Q.이미 from tools 해 줬는데 왜 또 해주지? -> A.가져온 Tool들을 하나의 목록으로 묶기

tool_map = {
    "get_blocked_tasks":get_blocked_tasks,
    "get_following_tasks": get_following_tasks,
    "get_available_tasks":get_available_tasks
}

model = ChatOpenAI(
    model="gpt-4.1-mini"
)

model_with_tools = model.bind_tools(tools)

user_message = "현재 BLOCKED 된 작업을 찾고, 그 작업의 직접 후속 작업도 알려줘"
# Q.왜 이 질문이 좋을까? -? A. 처음에 LLM 이 BLOCKED 된 작업의 id 를 모름 

"""
workFlow)
get_blocked_tasks() -> Task 1이 BLOCKED 라는 사실 확인 -> get_following_tasks(tast_id=1) -> 최종 답변
"""

messages = [
    HumanMessage(content=user_message)
]
# Q. 이 부분이 뭐하는 코드였지?
# A. 사용자 질문을 HumanMessage 형태로 만들어 messages 리스트에 넣는 것.
#    이후 LLM 응답과 Tool 결과도 messages에 계속 추가해서
#    지금까지의 대화/작업 기록을 LLM에게 다시 전달하기 위해 사용한다.
# LangGraph 배우기 전 우리가 직접 관리하는 간단한 State/대화 기록 같은 역할


while True:
    response = model_with_tools.invoke(messages)
    """
    messages 에 담긴것
    사용자 질문
    +이전 LLM 판단
    +이전 Tool 결과
    """
    messages.append(response)

    if not response.tool_calls:
        break
    
    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]

        selected_tool = tool_map[tool_name]
        result = selected_tool.invoke(tool_args)

        print("\nLLM이 선택한 Tool:")
        print(tool_name)

        print("Tool 인자:")
        print(tool_args)

        print("Tool 결과:")
        print(result)

        messages.append(
            ToolMessage( content=json.dumps(result,ensure_ascii=False),
            tool_call_id = tool_call["id"])
        )
        # Q. 이 부분은 뭐였지?
        # A. 실제 Tool 실행 결과를 ToolMessage로 만들어 messages에 저장하는 코드.
        #    다음 LLM 호출에서 "아까 네가 요청한 Tool의 실행 결과가 이것이다"라고 알려준다.


print("\n\n실제로 message 에 무엇이 담기는지 보기위한 코드입니다.")
print("\n===== 최종 messages =====")

for index, message in enumerate(messages):
    print(f"\n[{index}] {type(message).__name__}")
    print("content:", message.content)

    if hasattr(message, "tool_calls") and message.tool_calls:
        print("tool_calls:", message.tool_calls)
