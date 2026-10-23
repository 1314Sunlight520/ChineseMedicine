from typing import Optional

from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from pydantic import BaseModel

app = FastAPI()


# 表单数据
@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    print(f"用户名为:{username}")
    print(f"密码为:{password}")
    return {"username": username}


@app.post("/receive_raw_json/")
async def receive_raw_json(data: dict):
    print(f"接收到的数据为:{data}")
    data["friend"] = data.get("username", "") + "朋友"
    return data


class Item(BaseModel):
    name: str
    description: str
    price: Optional[float] = None


# 接收JSON数据的POST接口
@app.post("/items/")
async def create_item(item: Item):
    # 可以直接使用item对象，FastAPI会自动解析JSON
    print(item.model_dump())
    print(type(item.model_dump()))
    print(item.model_dump_json())
    print(type(item.model_dump_json()))
    return {"item": item.model_dump(), "message": "Item created successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
