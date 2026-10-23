import asyncio


class MsgQueueManager:
    def __init__(self):
        self.msg_queue_dict = {}

    def get_msg_queue_by_user_id(self, user_id):
        if user_id not in self.msg_queue_dict:
            self.msg_queue_dict[user_id] = asyncio.Queue()
        return self.msg_queue_dict[user_id]

    def delete_msg_queue_by_user_id(self, user_id):
        if user_id in self.msg_queue_dict:
            del self.msg_queue_dict[user_id]


msg_queue_manager = MsgQueueManager()


async def put_think_text_to_msg(user_id, text):
    msg_queue = msg_queue_manager.get_msg_queue_by_user_id(user_id)
    await msg_queue.put({"type": "think", "msg": f"{text}  \n"})
    await asyncio.sleep(0.1)


async def put_stream_text_to_msg(user_id, text):
    msg_queue = msg_queue_manager.get_msg_queue_by_user_id(user_id)
    await msg_queue.put({"type": "stream", "msg": f"{text}"})
    await asyncio.sleep(0.1)


async def put_think_text_stream_to_msg(user_id, text):
    msg_queue = msg_queue_manager.get_msg_queue_by_user_id(user_id)
    await msg_queue.put({"type": "think", "msg": f"{text}"})
    await asyncio.sleep(0.1)


async def put_think_huiche_text_to_msg(user_id):
    msg_queue = msg_queue_manager.get_msg_queue_by_user_id(user_id)
    await msg_queue.put({"type": "think", "msg": f"  \n"})
    await asyncio.sleep(0.1)


async def put_done_to_msg(user_id):
    msg_queue = msg_queue_manager.get_msg_queue_by_user_id(user_id)
    await msg_queue.put({"type": "done"})
