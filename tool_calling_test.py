from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import json
from langchain_core.messages import HumanMessage, ToolMessage


from tools import (
    get_blocked_tasks,
    get_following_tasks,
    get_available_tasks,
)

load_dotenv()

model = ChatOpenAI(
    model="gpt-4.1-mini"
)

tools = [
    get_blocked_tasks,
    get_following_tasks,
    get_available_tasks,
]

#if - elif - elif 로 하기엔 너무 코드가 별로라 밑에 코드 처럼 매핑.
tool_map = {
    "get_blocked_tasks": get_blocked_tasks,
    "get_following_tasks": get_following_tasks,
    "get_available_tasks": get_available_tasks,
}

model_with_tools = model.bind_tools(tools)


"""
사용자 질문
↓
LLM 판단
↓
get_blocked_tasks를 써야겠다고 결정 ✅
"""

#user_message = "현재 프로젝트에서 BLOCKED된 작업을 찾아줘."


#response = model_with_tools.invoke(user_message)

#print(response.tool_calls)

"""
get_blocked_tasks 실제 실행
↓
mock_data에서 BLOCKED Task 가져오기
"""



"""
tool_call = response.tool_calls[0]
#이 경우는 get_blocked_tast 인 상태 일때만 가져온것.
if tool_call["name"] == "get_blocked_tasks":
    result = get_blocked_tasks.invoke(tool_call["args"])

    print("\nTool 실행 결과:")
    print(result)
"""

#tool_call = response.tool_calls[0] #response.tool_calls = LLM이 요청한 Tool Call들의 리스트

#user_message = "BLOCKED 작업이랑 지금 바로 할 수 있는 작업도 찾아줘"
#response = model_with_tools.invoke(user_message)
user_message = "BLOCKED 작업이랑 지금 바로 할 수 있는 작업도 찾아줘"

messages = [
    HumanMessage(content=user_message)
]

response = model_with_tools.invoke(messages)

messages.append(response)


for tool_call in response.tool_calls:
    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    selected_tool = tool_map[tool_name]

    result = selected_tool.invoke(tool_args)

    print("\nLLM이 선택한 Tool:")
    print(tool_name)

    print("\nTool에 전달한 인자:")
    print(tool_args)

    print("\nTool 실행 결과:")
    print(result)

    messages.append(
        ToolMessage(
            content=json.dumps(result, ensure_ascii=False),
            tool_call_id=tool_call["id"]
        )
    )


final_response = model_with_tools.invoke(messages)

print("\n최종 답변:")
print(final_response.content)