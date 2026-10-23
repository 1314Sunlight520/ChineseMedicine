from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import json

from __004__langgraph_more_nodes.langgraph_more_nodes import zhongyi_response
from __005__fastapi.__003__msg_queue import put_done_to_msg, msg_queue_manager

app = FastAPI()


async def my_zhongyi_project(input: str, user_id: str):
    await zhongyi_response(input, user_id)
    print("执行完了， 添加入done方法")
    await put_done_to_msg(user_id)


async def generate_data(input: str, user_id: str):
    # 异步执行任务
    asyncio.create_task(my_zhongyi_project(input, user_id))

    while True:
        msg_queue = msg_queue_manager.get_msg_queue_by_user_id(user_id)
        msg = await msg_queue.get()
        # 推送 SSE
        yield json.dumps(msg, ensure_ascii=False)
        if msg.get("type") == "done":
            # 删除消息队列
            msg_queue_manager.delete_msg_queue_by_user_id(user_id)
            break


@app.post("/process")
async def process(data: dict):
    input = data.get("input", "")
    user_id = data.get("user_id", "")

    return StreamingResponse(generate_data(input, user_id), media_type="text/plain")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
