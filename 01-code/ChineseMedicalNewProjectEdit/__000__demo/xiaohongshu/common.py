from langchain_openai import ChatOpenAI

# ============ 配置llm区域 ============
my_llm = ChatOpenAI(
    api_key="YOUR_CREDENTIAL",  # ← 替换为你自己的 API Key
    base_url="https://api.deepseek.com",
    model="deepseek-chat"
)

JIMENG_AK = "YOUR_ACCESS_CREDENTIAL"
JIMENG_SK = "YOUR_ACCESS_CREDENTIAL"