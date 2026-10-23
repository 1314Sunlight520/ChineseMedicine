from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio
import uvicorn

app = FastAPI()


async def generate_data():
    res_list = ["我", "特别", "喜欢", "玩儿", "大模型"]
    for res in res_list:
        await asyncio.sleep(0.5)
        yield res


@app.post("/stream")
async def stream_data():
    return StreamingResponse(generate_data(), media_type="text/plain")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
