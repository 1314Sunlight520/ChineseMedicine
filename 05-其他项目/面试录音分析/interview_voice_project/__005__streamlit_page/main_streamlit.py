import streamlit as st

from __005__streamlit_page.pages.page_add import page_add
from __005__streamlit_page.pages.page_detail import page_detail
from __005__streamlit_page.pages.page_main import page_main
from __005__streamlit_page.pages.page_test import page_test

hide_sidebar = """
<style>
    section[data-testid="stSidebar"] {
        display: none;
    }
</style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)


# 获取当前页面的查询参数
def main():
    # 获取当前 URL 中的页面参数
    page = st.session_state.get("page", "page_main")

    # 根据页面选择显示不同的内容
    if page == "page_main":
        page_main()
    elif page == "page_detail":
        page_detail()
    elif page == "page_add":
        page_add()
    else:
        page_test()


if __name__ == "__main__":
    main()
