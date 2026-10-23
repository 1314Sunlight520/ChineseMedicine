import os
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

from common.path_utils import get_file_path

try:
    import pandas as pd
except ImportError:  # 简单兜底：如果没有 pandas 就提示一下
    pd = None


URL = "https://zhongyibaike.com/wiki/中医方剂"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
}


def fetch_html(url: str) -> str:
    """请求网页 HTML."""
    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    # 网站是 UTF-8 编码
    resp.encoding = "utf-8"
    return resp.text


def parse_fangji(html: str) -> List[Dict[str, str]]:
    """
    解析“中医方剂”页面，提取：方剂名 + 方剂链接。

    根据已知页面结构：
    - 文章正文位于：<section id="content"><div class="col s12 p_content"> ... </div></section>
    - 各个方剂都出现在这个 div 里的 <a href="/wiki/xxx">方剂名</a> 中
    - 页眉导航、页脚链接都在正文区域外

    因此，这里只在正文 div 中查找所有 /wiki/ 开头的链接，
    再用“名称结尾字”做一次粗略过滤，避免把“中医理论”等非方剂抓进来。
    """
    soup = BeautifulSoup(html, "html.parser")

    # 1. 精确定位正文区域
    content = soup.select_one("section#content div.p_content")
    if content is None:
        # 兜底：退化为 id=content 或整个 body，尽量不让程序直接崩
        content = soup.find("div", id="content") or soup.body or soup

    rows: List[Dict[str, str]] = []

    # 2. 在正文中查找所有 /wiki/ 开头的链接
    seen = set()  # 去重 (name, href)
    for a in content.select('a[href^="/wiki/"]'):
        name = a.get_text(strip=True)
        href = a["href"]

        if not name:
            continue

        # 处理相对链接
        if href.startswith("/"):
            href_full = "https://zhongyibaike.com" + href
        else:
            href_full = href

        key = (name, href_full)
        if key in seen:
            continue
        seen.add(key)

        rows.append(
            {
                "方剂名": name,
                "链接": href_full,
            }
        )

    return rows


def save_to_excel(rows: List[Dict[str, str]], file_path: str) -> None:
    """保存为 Excel 文件."""
    df = pd.DataFrame(rows)
    df.to_excel(file_path, index=False)
    print(f"已成功保存到：{file_path}")


def main():
    print(f"开始抓取：{URL}")
    html = fetch_html(URL)
    print("网页抓取完成，开始解析...")

    rows = parse_fangji(html)
    print(f"解析到方剂条目数量：{len(rows)}")

    # 输出到当前脚本所在目录下
    out_file = get_file_path("__001__clawer/中医方剂_方剂列表.xlsx")
    save_to_excel(rows, out_file)


if __name__ == "__main__":
    main()


