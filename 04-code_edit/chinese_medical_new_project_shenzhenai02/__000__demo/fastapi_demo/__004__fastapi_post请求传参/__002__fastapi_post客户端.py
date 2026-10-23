import requests

response = requests.post("http://localhost:8000/login", data={"username": "小张", "password": "123456"})
print(response.json())
print("*" * 100)

response = requests.post("http://localhost:8000/receive_raw_json", json={"username": "小张", "password": "123456"})
print(response.json())
print("*" * 100)

response = requests.post("http://localhost:8000/items",
                         json={"name": "小张", "description": "是个大帅哥"})
print(response.json())
