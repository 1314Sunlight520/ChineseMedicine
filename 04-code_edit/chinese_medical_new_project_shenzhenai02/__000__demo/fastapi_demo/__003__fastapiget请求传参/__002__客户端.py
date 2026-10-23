import requests


response = requests.get("http://localhost:8000/items/12345")
print(response.json())


response = requests.get("http://localhost:8000/dogs?type=田园犬&age=5")
print(response.json())

response = requests.get("http://localhost:8000/dogs", params={"type": "柯基", "age": 2000})
print(response.json())

response = requests.get("http://localhost:8000/cats", params={"age": 5})
print(response.json())