from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import RunnableConfig, interrupt, Command


# 定义状态结构
class State(dict):
    task: str
    approval: str


def create_task(state: State):
    task = "审批预算申请（金额：500万元）"
    print(f"系统创建任务：{task}")
    state["task"] = task
    return state


# 人工操作节点
def human_approval(state: State):
    print("等待人工审批中...")
    # 触发人工中断（这里 LangGraph 会暂停执行，直到被 resume）
    receiver = interrupt({"type": "human_approval", "value": "请领导进行审批！"})
    print(receiver)
    state["approval"] = receiver["value"]
    return state


# 后续步骤：根据人工结果继续
def finalize(state: State):
    if state["approval"] == "批准":
        print(f"✅ 审批通过：{state['task']}")
    else:
        print(f"❌ 审批拒绝：{state['task']}")
    return state


def build_graph():
    grpah_builder = StateGraph(State)
    grpah_builder.add_node("create_task", create_task)
    grpah_builder.add_node("human_approval", human_approval)
    grpah_builder.add_node("finalize", finalize)

    grpah_builder.add_edge(START, "create_task")
    grpah_builder.add_edge("create_task", "human_approval")
    grpah_builder.add_edge("human_approval", "finalize")
    grpah_builder.add_edge("finalize", END)

    memory = InMemorySaver()
    graph = grpah_builder.compile(checkpointer=memory)
    return graph


if __name__ == "__main__":
    graph = build_graph()

    # 第一次运行 —— 执行到人工中断处
    config = RunnableConfig(configurable={"thread_id": "12345"})
    print("=== 第一次运行 ===")
    state = graph.invoke({}, config=config)
    print("第一次运行状态：", state)
    value_dict = {}
    if "__interrupt__" in state and len(state["__interrupt__"]) > 0:
        value_dict = state["__interrupt__"][0].value
    user_decision = input(value_dict["value"])

    # 模拟人工输入并恢复执行
    print("\n=== 第二次运行（人工输入后继续） ===")
    state = graph.invoke(Command(resume={"value": user_decision}), config=config)
    print("第二次运行状态：", state)
