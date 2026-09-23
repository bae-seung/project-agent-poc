"""
agent_loop_test                 LangGraph

messages 리스트        →        MessagesState

while True             →        Graph의 반복 Edge

LLM 호출 부분          →        Agent Node

for tool_call ...      →        ToolNode

if tool_calls 있음?    →        Conditional Edge

break                  →        END
"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from langgraph.graph import StateGraph, START , MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

from tools import(
     get_blocked_tasks,
    get_following_tasks,
    get_available_tasks,
)

load_dotenv()

tools = [
    get_blocked_tasks,
    get_following_tasks,
    get_available_tasks,
]

model = ChatOpenAI(
    model ="gpt-4.1-mini"
)

model_with_tools = model.bind_tools(tools)

class AgentState(MessagesState): # Q. AgentState 클래스는 안에 아무것도 없는거 아니야?
    pass


def agent_node(state : AgentState): 
    # Q. state : AgentState 이 부분이 이해가 안가는데 AgentState 객체를 인자로 받겠다는 소리인가? -> A. state : 매겨변수 이름 AgentState : 타입인자 힌트
    response = model_with_tools.invoke(state["messages"]) # Q. state 라는 리스트는 안보이는데 어디서 나온거지? -> A. LangGraph가 넣어줌
   
    """
    state = {
    "messages": [
        HumanMessage(...),
        AIMessage(...),
        ToolMessage(...),
                ]
            }
    """

    return {
        "messages" : [response]
    }

tool_node = ToolNode(tools)
#get_blocked_tasks, get_following_tasks, get_available_tasks를 실행할 수 있는 Tool 전용 Node를 만들어라

graph_builder = StateGraph(AgentState)
#AgentState를 상태 구조로 사용하는 그래프를 하나 만들겠다. -> 이 그래프가 작업하면서 어떤 정보를 들고 다닐지를 정하는 틀

graph_builder.add_node("agent",agent_node)
graph_builder.add_node("tools",tool_node)
"""
[agent]

[tools]

-> 아직은 연결이 안된 상태
"""

graph_builder.add_edge(START, "agent")
#그래프가 시작되면 제일 먼저 "agent" 노드를 실행해라.

graph_builder.add_conditional_edges(
    "agent",
    tools_condition # "agent" 실행 후 다음에 어디로 갈지
)
#agent 노드가 실행된 뒤에, tools_condition으로 다음 경로를 판단해라.

graph_builder.add_edge(
    "tools",
    "agent"
)

graph = graph_builder.compile()

result = graph.invoke({
    "messages": [
        {
            "role": "user",
            "content": "현재 BLOCKED 된 작업을 찾고, 그 작업의 직접 후속 작업도 알려줘"
        }
    ]
})

"""
graph.invoke(...)
↓
START
↓
agent
↓
tools_condition
↓
필요하면 tools
↓
다시 agent
↓
필요 없으면 END
"""

print(result["messages"][-1].content)

print("\n===== 최종 State의 messages =====")

for index, message in enumerate(result["messages"]):
    print(f"\n[{index}] {type(message).__name__}")
    print("content:", message.content)

    if hasattr(message, "tool_calls") and message.tool_calls:
        print("tool_calls:", message.tool_calls)