import requests

response = requests.post("http://127.0.0.1:8000/process", json={"input": "我脑袋疼，吃什么药呢？"})
print(response.json())
