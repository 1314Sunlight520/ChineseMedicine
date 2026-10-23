from bs4 import BeautifulSoup

html = """
<html>
    <body>
        <h1>Hello</h1>
        <a href="https://example.com">Link</a>
    </body>
</html>
"""

# 解析 HTML
soup = BeautifulSoup(html, 'html.parser')

print(soup.h1.text)      # 输出：Hello
print(soup.a['href'])    # 输出：https://example.com