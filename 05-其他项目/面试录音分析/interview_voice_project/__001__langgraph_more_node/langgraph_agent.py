from langgraph.constants import START, END
from langgraph.graph import StateGraph

from __001__langgraph_more_node.agent_state import AgentState
from __001__langgraph_more_node.nodes.__001__split_voice_node import split_voice_node
from __001__langgraph_more_node.nodes.__002__voice_to_text_node import voice_to_text_node
from __001__langgraph_more_node.nodes.__003__voice_text_arrange_node import voice_text_arrange_node
from __001__langgraph_more_node.nodes.__004__extract_interview_topic_node import extract_interview_topic_node
from __001__langgraph_more_node.nodes.__005__offer_sample_answer_node import offer_sample_answer_node
from __001__langgraph_more_node.nodes.__006__offer_interview_advice_node import offer_interview_advice_node
from __001__langgraph_more_node.nodes.__007__generate_markdown_node import generate_markdown_node
from common.ouput_graph_utils import output_pic_graph
from common.path_utils import get_file_path


def build_graph():
    # 定义状态图
    graph_builder = StateGraph(AgentState)
    graph_builder.add_node(split_voice_node.__name__, split_voice_node)
    graph_builder.add_node(voice_to_text_node.__name__, voice_to_text_node)
    graph_builder.add_node(voice_text_arrange_node.__name__, voice_text_arrange_node)
    graph_builder.add_node(extract_interview_topic_node.__name__, extract_interview_topic_node)
    graph_builder.add_node(offer_sample_answer_node.__name__, offer_sample_answer_node)
    graph_builder.add_node(offer_interview_advice_node.__name__, offer_interview_advice_node)
    graph_builder.add_node(generate_markdown_node.__name__, generate_markdown_node)

    # 添加边
    graph_builder.add_edge(START, split_voice_node.__name__)
    graph_builder.add_edge(split_voice_node.__name__, voice_to_text_node.__name__)
    graph_builder.add_edge(voice_to_text_node.__name__, voice_text_arrange_node.__name__)
    graph_builder.add_edge(voice_text_arrange_node.__name__, extract_interview_topic_node.__name__)
    graph_builder.add_edge(extract_interview_topic_node.__name__, offer_sample_answer_node.__name__)
    graph_builder.add_edge(offer_sample_answer_node.__name__, offer_interview_advice_node.__name__)
    graph_builder.add_edge(offer_interview_advice_node.__name__, generate_markdown_node.__name__)
    graph_builder.add_edge(generate_markdown_node.__name__, END)

    # 编译状态图
    graph = graph_builder.compile()
    return graph


graph = build_graph()
# 输出表的状态图
output_pic_graph(graph, get_file_path("__001__langgraph_more_node/graph.jpg"))


async def interview_voice_analyse(file_location, record_id, interview_info_dict):
    result = await graph.ainvoke(
        {"input_audio_path": file_location, "record_id": record_id, "interview_info_dict": interview_info_dict})
    return result.get("interview_markdown_text", "")


if __name__ == '__main__':
    result = interview_voice_analyse(get_file_path("__001__data/新录音20.m4a"), "",
                                     {"name": "张三", "company": "传智播客", "subject": "python大模型人工智能",
                                      "interview_date_str": "2023-05-05"})
    print(result)
    ...
