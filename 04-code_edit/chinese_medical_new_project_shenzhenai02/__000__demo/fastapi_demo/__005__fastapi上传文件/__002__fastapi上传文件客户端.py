# 创建请求客户端
import requests

# 单文件上传
file_path = "查理芒格语录.jpg"
# 发送单文件上传请求
url = "http://localhost:8000/uploadfile/"
with open(file_path, "rb") as f:
    files = {"file": (file_path, f)}
    response = requests.post(url, files=files)

print("单文件上传响应:")
print(f"状态码: {response.status_code}")
print(f"响应内容: {response.json()}")