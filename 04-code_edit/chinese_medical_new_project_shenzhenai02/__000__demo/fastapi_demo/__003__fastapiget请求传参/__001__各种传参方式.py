from typing import Optional

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse

app = FastAPI()


# 路径参数示例
@app.get("/items/{good_id}")
async def read_item(good_id: int):
    print(good_id)
    return {"good_id": good_id}


@app.get("/dogs/")
async def read_dog(type: str, age: int):
    print(type)
    print(age)
    age += 1000
    return {"type": type, "age": age}


# 可选参数和默认值
@app.get("/cats/")
async def read_cat(name: Optional[str] = None, age: int = 5):
    age = age + 10000
    return {"name": name, "age": age}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
