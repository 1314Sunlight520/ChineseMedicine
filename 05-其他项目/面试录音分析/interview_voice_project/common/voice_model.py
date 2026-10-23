from funasr import AutoModel

from common.config import Config

conf = Config()

my_voice_model = AutoModel(
    model=conf.VOICE_MODEL_PATH,
    trust_remote_code=True,
    vad_model=conf.VOICE_VAD_MODEL_PATH,
    vad_kwargs={"max_single_segment_time": 30000},
    device="cpu",
    disable_update=True
)
