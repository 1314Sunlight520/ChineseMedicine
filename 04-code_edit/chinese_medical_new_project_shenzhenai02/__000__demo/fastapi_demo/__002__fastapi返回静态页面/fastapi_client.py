import requests


response = requests.get("http://192.168.40.24:8000/")
print(response.status_code)
print(response.text)