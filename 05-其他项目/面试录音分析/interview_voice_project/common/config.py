import os
from dotenv import load_dotenv

from common.path_utils import get_file_path

load_dotenv()
load_dotenv(get_file_path(".env"))


class Config:
    def __init__(self):
        # 大模型相关
        self.MODEL_API_KEY = os.getenv("MODEL_API_KEY")
        self.MODEL_BASE_URL = os.getenv("MODEL_BASE_URL")
        self.MODEL_NAME = os.getenv("MODEL_NAME")

        # 语音路径
        self.VOICE_MODEL_PATH = os.getenv("VOICE_MODEL_PATH")
        self.VOICE_VAD_MODEL_PATH = os.getenv("VOICE_VAD_MODEL_PATH")

        # mysql数据 库
        self.MYSQL_HOST = os.getenv("MYSQL_HOST")
        self.MYSQL_USER = os.getenv("MYSQL_USER")
        self.MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
        self.MYSQL_DATABASE_NAME = os.getenv("MYSQL_DATABASE_NAME")


if __name__ == "__main__":
    conf = Config()
