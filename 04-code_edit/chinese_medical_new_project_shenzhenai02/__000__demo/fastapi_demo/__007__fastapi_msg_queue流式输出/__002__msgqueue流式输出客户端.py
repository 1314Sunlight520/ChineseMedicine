import requests
import json


def stream_client():
    url = "http://localhost:8000/stream"
    response = requests.post(url, stream=True)
    for chunk in response.iter_content(chunk_size=None):
        chunk_str = chunk.decode("utf-8")
        chunk_dict = json.loads(chunk_str)
        type = chunk_dict.get("type", "done")
        msg = chunk_dict.get("msg", "")
        if type == "msg":
            print(msg, end="", flush=True)
        else:
            break



if __name__ == "__main__":
    stream_client()
