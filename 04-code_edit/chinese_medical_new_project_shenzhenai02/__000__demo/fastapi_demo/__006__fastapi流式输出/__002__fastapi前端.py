import requests


def stream_client():
    url = "http://localhost:8000/stream"
    response = requests.post(url, stream=True)
    for chunk in response.iter_content(chunk_size=None):
        print(chunk.decode("utf-8"), end="", flush=True)


if __name__ == "__main__":
    stream_client()
