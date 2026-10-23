import time
from operator import add
from typing import TypedDict, List, Annotated

from langgraph.graph import StateGraph, START, END


def my_merge(left, right):
    print(f"left:{left}")
    print(f"right:{right}")
    print(f"left+right:{left + right}")
    return left + right


def my_merge2(data1, data2):
    return data2


# 定义状态结构
class MyState(TypedDict):
    menu: Annotated[List[str], lambda a1, a2: a2]
    all_ready: bool


# --- 节点定义 ---
def start_cooking(state: MyState):
    print("👨‍🍳 厨房准备开始！")
    # 初始化共享菜单列表
    state["menu"] = []
    return state


# b = [] + ["番茄炒蛋", "宫保鸡丁", "鱼香肉丝"] + ["番茄炒蛋", "宫保鸡丁", "鱼香肉丝"] + ["番茄炒蛋", "宫保鸡丁",
#                                                                                         "鱼香肉丝"] + ["番茄炒蛋",
#                                                                                                        "宫保鸡丁",
#                                                                                                        "鱼香肉丝"] + [
#         "番茄炒蛋", "宫保鸡丁", "鱼香肉丝"] + ["番茄炒蛋", "宫保鸡丁", "鱼香肉丝"]
# print(b)


def chef_a(state: MyState):
    print("👩‍🍳 A 厨师在做：番茄炒蛋...")
    time.sleep(2)
    # 向共享 list 添加菜品
    state["menu"].append("番茄炒蛋")
    print("chef_a", state["menu"])
    return state


def chef_b(state: MyState):
    print("👨‍🍳 B 厨师在做：宫保鸡丁...")
    time.sleep(3)
    state["menu"].append("宫保鸡丁")
    print("chef_b", state["menu"])
    return state


def chef_c(state: MyState):
    print("👩‍🍳 C 厨师在做：鱼香肉丝...")
    time.sleep(5)
    state["menu"].append("鱼香肉丝")
    print("chef_c", state["menu"])
    return state


def chef_d(state: MyState):
    print("👩‍🍳 d 厨师在做：京酱肉丝...")
    time.sleep(2)
    state["menu"].append("京酱肉丝")
    print("chef_d", state["menu"])
    return state


def serve_dish(state: MyState):
    print("serve_dish", state["menu"])
    print("\n🍽️ 所有菜都准备好了！菜单如下：")
    for dish in state["menu"]:
        print(" -", dish)
    state["all_ready"] = True

    return state


# --- 构建 LangGraph ---
def build_graph():
    graph_builder = StateGraph(MyState)
    graph_builder.add_node("start", start_cooking)
    graph_builder.add_node("chef_a", chef_a)
    graph_builder.add_node("chef_b", chef_b)
    graph_builder.add_node("chef_c", chef_c)
    graph_builder.add_node("chef_d", chef_d)
    graph_builder.add_node("serve", serve_dish)

    # 启动 → 并行三个厨师
    graph_builder.add_edge(START, "start")
    graph_builder.add_edge("start", "chef_a")
    graph_builder.add_edge("start", "chef_b")
    graph_builder.add_edge("start", "chef_c")
    graph_builder.add_edge("start", "chef_d")

    # 三个厨师汇总到 serve
    graph_builder.add_edge(["chef_a", "chef_b", "chef_c", "chef_d"], "serve")

    graph_builder.add_edge("serve", END)

    return graph_builder.compile()


# --- 运行 ---
if __name__ == "__main__":
    graph = build_graph()
    result = graph.invoke({})
    print("\n最终结果:", result)
