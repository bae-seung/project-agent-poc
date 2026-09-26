from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import AIMessage

class ApprovalState(MessagesState):
    approved: bool | None # 타입 힌트 -> apporved 의 안에는 True,False 또는 None이 들어 올 수있다.

def approval_node(state: ApprovalState):
    decision = interrupt(
        {
            "question" : "이 변경안을 적용 할까요?",
            "options" : ["approve","reject"]
        }
    )
    return{
        "approved": decision == "approve"
    }

def result_node(state: ApprovalState):
    if state["approved"]:
        message = "변경안이 승인되었습니다."
    else:
        message = "변경안이 거절되었습니다."
    
    return {
        "messages":[
            AIMessage(content=message)
        ]
    }

graph_builder = StateGraph(ApprovalState)
graph_builder.add_node("approval",approval_node)
graph_builder.add_node("result",result_node)

graph_builder.add_edge(START,"approval")
graph_builder.add_edge("approval","result")
graph_builder.add_edge("result",END)

checkpointer = InMemorySaver()

graph = graph_builder.compile(
    checkpointer=checkpointer
)

config = {
    "configurable":{
        "thread_id" : "approval-test-1"
    }
}

result = graph.invoke(
    {
        "messages" : [],
        "approved" : None
    },
    config=config
)

print("\n====== 승인 요청 ======")
print(result["__interrupt__"])

user_input = input("\napprove 또는 reject를 입력하세요: ").strip().lower()

while user_input not in ["approve","reject"]:
    user_input = input("approve 또는 reject만 입력하세요: ").strip().lower()

result = graph.invoke(
    Command(resume=user_input),
    config=config
)

print("\n===== 최종 결과 =====")
print(result["messages"][-1].content)