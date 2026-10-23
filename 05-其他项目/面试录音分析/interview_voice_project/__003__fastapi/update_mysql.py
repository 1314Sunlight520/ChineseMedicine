import asyncio
import time
from enum import Enum
from common.config import Config
from __002__db_helper_parse.db_helper import my_db_helper

conf = Config()


async def update_mysql(msg: str, record_id=None):
    my_db_helper.update_interview_record(record_id, {"processing_tips": msg})
