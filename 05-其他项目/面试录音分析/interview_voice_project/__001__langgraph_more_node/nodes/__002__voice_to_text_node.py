import time

from funasr.utils.postprocess_utils import rich_transcription_postprocess
from tqdm import tqdm

from __001__langgraph_more_node.agent_state import AgentState
from __003__fastapi.update_mysql import update_mysql
from common.voice_model import my_voice_model


async def void2text(voice_path):
    res = my_voice_model.generate(
        input=voice_path,
        cache={},
        language="auto",  # "zn", "en", "yue", "ja", "ko", "nospeech"
        use_itn=True,
        batch_size_s=60,
        merge_vad=True,  #
        merge_length_s=15,
    )
    text = rich_transcription_postprocess(res[0]["text"])
    return text


async def voice_to_text_node(state: AgentState):
    await update_mysql("开始语音转文本", record_id=state["record_id"])
    split_audio_path_list = state['split_audio_path_list']
    # 获取voice路径
    voice_text_list = []
    for i, split_audio_path in enumerate(tqdm(split_audio_path_list, desc="处理语音")):
        text = await void2text(split_audio_path)
        await update_mysql(f"正在处理第{(i + 1)}/{len(split_audio_path_list)}块。", record_id=state["record_id"])
        print(text)
        voice_text_list.append(text)
    print(voice_text_list)
    state['voice_text_list'] = voice_text_list
    await update_mysql("完成语音转文本", record_id=state["record_id"])
    return state


if __name__ == '__main__':
    voice_to_text_node({"split_audio_path_list": [
        '/Users/duyi/PycharmProjects/interview_voice_project/voice/20250927_201420_罗培鑫面试/20250927_201420_罗培鑫面试_segment_001.wav',
        '/Users/duyi/PycharmProjects/interview_voice_project/voice/20250927_201420_罗培鑫面试/20250927_201420_罗培鑫面试_segment_002.wav',
        '/Users/duyi/PycharmProjects/interview_voice_project/voice/20250927_201420_罗培鑫面试/20250927_201420_罗培鑫面试_segment_003.wav',
        '/Users/duyi/PycharmProjects/interview_voice_project/voice/20250927_201420_罗培鑫面试/20250927_201420_罗培鑫面试_segment_004.wav',
        '/Users/duyi/PycharmProjects/interview_voice_project/voice/20250927_201420_罗培鑫面试/20250927_201420_罗培鑫面试_segment_005.wav',
        '/Users/duyi/PycharmProjects/interview_voice_project/voice/20250927_201420_罗培鑫面试/20250927_201420_罗培鑫面试_segment_006.wav',
        '/Users/duyi/PycharmProjects/interview_voice_project/voice/20250927_201420_罗培鑫面试/20250927_201420_罗培鑫面试_segment_007.wav',
        '/Users/duyi/PycharmProjects/interview_voice_project/voice/20250927_201420_罗培鑫面试/20250927_201420_罗培鑫面试_segment_008.wav',
        '/Users/duyi/PycharmProjects/interview_voice_project/voice/20250927_201420_罗培鑫面试/20250927_201420_罗培鑫面试_segment_009.wav',
        '/Users/duyi/PycharmProjects/interview_voice_project/voice/20250927_201420_罗培鑫面试/20250927_201420_罗培鑫面试_segment_010.wav',
        '/Users/duyi/PycharmProjects/interview_voice_project/voice/20250927_201420_罗培鑫面试/20250927_201420_罗培鑫面试_segment_011.wav',
        '/Users/duyi/PycharmProjects/interview_voice_project/voice/20250927_201420_罗培鑫面试/20250927_201420_罗培鑫面试_segment_012.wav',
        '/Users/duyi/PycharmProjects/interview_voice_project/voice/20250927_201420_罗培鑫面试/20250927_201420_罗培鑫面试_segment_013.wav',
        '/Users/duyi/PycharmProjects/interview_voice_project/voice/20250927_201420_罗培鑫面试/20250927_201420_罗培鑫面试_segment_014.wav',
        '/Users/duyi/PycharmProjects/interview_voice_project/voice/20250927_201420_罗培鑫面试/20250927_201420_罗培鑫面试_segment_015.wav',
        '/Users/duyi/PycharmProjects/interview_voice_project/voice/20250927_201420_罗培鑫面试/20250927_201420_罗培鑫面试_segment_016.wav',
        '/Users/duyi/PycharmProjects/interview_voice_project/voice/20250927_201420_罗培鑫面试/20250927_201420_罗培鑫面试_segment_017.wav',
        '/Users/duyi/PycharmProjects/interview_voice_project/voice/20250927_201420_罗培鑫面试/20250927_201420_罗培鑫面试_segment_018.wav',
        '/Users/duyi/PycharmProjects/interview_voice_project/voice/20250927_201420_罗培鑫面试/20250927_201420_罗培鑫面试_segment_019.wav',
        '/Users/duyi/PycharmProjects/interview_voice_project/voice/20250927_201420_罗培鑫面试/20250927_201420_罗培鑫面试_segment_020.wav',
        '/Users/duyi/PycharmProjects/interview_voice_project/voice/20250927_201420_罗培鑫面试/20250927_201420_罗培鑫面试_segment_021.wav',
        '/Users/duyi/PycharmProjects/interview_voice_project/voice/20250927_201420_罗培鑫面试/20250927_201420_罗培鑫面试_segment_022.wav',
        '/Users/duyi/PycharmProjects/interview_voice_project/voice/20250927_201420_罗培鑫面试/20250927_201420_罗培鑫面试_segment_023.wav',
        '/Users/duyi/PycharmProjects/interview_voice_project/voice/20250927_201420_罗培鑫面试/20250927_201420_罗培鑫面试_segment_024.wav',
        '/Users/duyi/PycharmProjects/interview_voice_project/voice/20250927_201420_罗培鑫面试/20250927_201420_罗培鑫面试_segment_025.wav']})
