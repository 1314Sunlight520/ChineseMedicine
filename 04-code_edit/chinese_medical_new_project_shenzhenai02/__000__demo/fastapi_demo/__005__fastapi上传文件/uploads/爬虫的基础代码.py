import requests
from bs4 import BeautifulSoup

# 目标网站
url = "https://zhongyibaike.com/wiki/%E4%B8%AD%E8%8D%AF%E5%A4%A7%E5%85%A8"

# 自定义请求头，伪装成浏览器
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                   (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
}

try:
    # 发送请求
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # 如果返回非200，会主动抛出异常

    # 指定编码（有些网站需要手动设置）
    response.encoding = "uft-8"
    print("网页编码：", response.encoding)

    # 打印 HTML 部分内容
    print("网页标题：")
    # print(response.text)

    # HTML 解析
    soup = BeautifulSoup(response.text, "html.parser")
    #
    # 示例：提取所有 a 标签的链接
    links = [a["href"] for a in soup.find_all("a", href=True)]
    print("\n所有链接：")
    for link in links:
        print(link)

except requests.exceptions.RequestException as e:
    print("请求出现错误：", e)
