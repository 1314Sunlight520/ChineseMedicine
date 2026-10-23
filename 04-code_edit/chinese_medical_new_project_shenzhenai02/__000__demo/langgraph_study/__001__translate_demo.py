from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END, START
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph.state import CompiledStateGraph

# ========== 1) 创建 LLM ==========
llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com",
    api_key="YOUR_CREDENTIAL"
)


# ========== 2) 定义状态 ==========，这就是一个字典
class AgentState(dict):
    # 输入
    input: str
    # 是否是翻译
    is_translate_or_not: bool
    # 要翻译的句子
    translate_sentence: str
    # 翻译结果
    translate_result: str
    # QA结果
    qa_result: str
    # 输出
    output: str


def identify_intent_node(state: AgentState) -> AgentState:
    """判断用户输入是翻译文章还是普通回答"""
    input = state['input']
    messages = [
        SystemMessage(content=(
            "你是一个意图分类助手，用来判断用户输入是'翻译任务'还是'普通回答任务'。\n"
            "翻译任务的特征：用户明确要求翻译文章、句子、单词，或要求将中文翻译成英文/英文翻译成中文。\n"
            "普通回答任务的特征：用户是直接提问、咨询信息、讨论话题，而不是要求翻译。\n"
            "请你只回答：翻译 或 普通回答，不要补充其他内容。"
        )),
        HumanMessage(content=input)
    ]

    response = llm.invoke(messages).content.strip()

    if "翻译" in response:
        state['is_translate_or_not'] = True
    else:
        state['is_translate_or_not'] = False

    return state


def extract_translate_sentence_node(state: AgentState) -> AgentState:
    """提取翻译句子"""
    input = state['input']
    prompot = (
        "你是翻译助手。请先自动识别语言，然后提取待翻译的句子。"
        "请将待翻译的句子提取出来，并输出。"
        "请不要输出其他内容。\n"
        f"待翻译内容：{input}"
    )
    result = llm.invoke([HumanMessage(content=prompot)]).content
    state['translate_sentence'] = result
    return state


def translate_node(state: AgentState) -> AgentState:
    """翻译节点"""
    translate_sentence = state["translate_sentence"]
    prompt = (
        "你是翻译助手。请先自动识别语言，然后在中文与英文之间互译。"
        "只输出译文本身，不要额外解释。\n"
        f"待翻译内容：{translate_sentence}"
    )
    result = llm.invoke([HumanMessage(content=prompt)]).content
    state['translate_result'] = result
    state['output'] = result
    # 按你的状态定义回写
    return state


def qa_node(state: AgentState) -> AgentState:
    """QA节点"""
    qa_sentence = state["input"]
    prompt = (
        "你是一个问答助手，请回答问题。"
        "请使用中文回答。\n"
        f"问题：{qa_sentence}"
    )
    result = llm.invoke([HumanMessage(content=prompt)]).content
    state['qa_result'] = result
    state['output'] = result
    # 按你的状态定义回写
    return state


def build_langgraph():
    graph_builder = StateGraph(AgentState)
    graph_builder.add_node("意图识别节点", identify_intent_node)
    graph_builder.add_node("抽取信息节点", extract_translate_sentence_node)
    graph_builder.add_node("翻译节点", translate_node)
    graph_builder.add_node("问答节点", qa_node)

    graph_builder.add_edge(START, "意图识别节点")

    def identify_intent_node_condition(state: AgentState):
        if state['is_translate_or_not']:
            return "抽取信息节点"
        else:
            return "问答节点"

    graph_builder.add_conditional_edges("意图识别节点", identify_intent_node_condition, path_map={
        "抽取信息节点": "抽取信息节点",
        "问答节点": "问答节点"
    })
    graph_builder.add_edge("抽取信息节点", "翻译节点")
    graph_builder.add_edge("问答节点", END)
    graph_builder.add_edge("翻译节点", END)
    graph = graph_builder.compile()
    return graph


if __name__ == '__main__':
    graph = build_langgraph()
    input = "请将这句话翻译成英文：我叫小王，我爱找工作，找工作使我快乐，我感觉找工作就像开盲盒一样，每次面试完都要等消息，好刺激啊。"
    result = graph.invoke({"input": input})
    print(result["output"])

    # input = "请解释一下找工作的快乐。"
    # result = graph.invoke({"input": input})
    # print(result["output"])
