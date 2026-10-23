import os
import re
from typing import Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup, Comment
from tqdm import tqdm

from common.path_utils import get_file_path

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
}

REQUEST_TIMEOUT = 10


def fetch_html(url: str) -> str:
    """Fetch raw HTML for a given url."""
    resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    return resp.text


def extract_main_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    content = soup.select_one("section#content div.p_content")

    if content is None:
        content = soup.find("div", id="content") or soup.body

    if content is None:
        return ""

    # 删除 script/style/ins
    for tag in content(["script", "style", "ins"]):
        tag.decompose()

    # 删除 HTML 注释
    for c in content(text=lambda x: isinstance(x, Comment)):
        c.extract()

    # 手动按块级元素拆段
    parts = []
    block_tags = {"p", "div", "h2", "h3", "h4", "li"}

    for elem in content.descendants:
        # 遇到块级元素 → 插入换行
        if elem.name in block_tags:
            parts.append("\n")
        # 文本节点
        elif isinstance(elem, str):
            parts.append(elem)

    text = "".join(parts)

    # 清除全角空格
    text = text.replace("　", "")

    # 合并多余空行
    text = re.sub(r"\n+", "\n", text).strip()

    return text


def sanitize_filename(name: str) -> str:
    """Replace filesystem-illegal characters with underscores."""
    return re.sub(r'[\\/:*?"<>|]', "_", name)


def save_txt(name: str, text: str, out_dir: str) -> Optional[str]:
    """Persist the extracted text into a UTF-8 txt file."""
    if not text:
        return None

    os.makedirs(out_dir, exist_ok=True)
    filename = sanitize_filename(name) + ".txt"
    path = os.path.join(out_dir, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

    return path


def main():
    excel_path = get_file_path("__001__clawer/中医方剂_方剂列表.xlsx")
    output_dir = get_file_path("__001__clawer/中药")

    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"未找到 Excel 文件：{excel_path}")

    df = pd.read_excel(excel_path)
    if df.empty:
        print("Excel 中没有数据，程序结束。")
        return

    # ==== 断点续爬：加载已存在的 txt 文件 ====
    os.makedirs(output_dir, exist_ok=True)
    # set格式
    existed_txt = {os.path.splitext(f)[0] for f in os.listdir(output_dir) if f.endswith(".txt")}
    print(f"已存在文件数量: {len(existed_txt)}")

    # tqdm 包装 iterrows
    for _, row in tqdm(df.iterrows(), total=len(df), desc="Processing"):
        name = str(row.get("方剂名", "")).strip()
        url = str(row.get("链接", "")).strip()

        if not name or not url:
            continue

        # ==== 如果已经爬过并保存，跳过 ====
        if name in existed_txt:
            tqdm.write(f"[SKIP] {name} 已存在，跳过")
            continue

        try:
            # 抓取页面
            html = fetch_html(url)
            # 抽取主内容
            text = extract_main_text(html)
            # 保存
            saved_path = save_txt(name, text, output_dir)

            if saved_path:
                tqdm.write(f"[OK] {name} -> {saved_path}")
            else:
                tqdm.write(f"[WARN] {name} 页面内容为空，未生成文件。")
        except Exception as exc:
            tqdm.write(f"[ERROR] {name} ({url}) 抓取失败：{exc}")


if __name__ == "__main__":
    main()
