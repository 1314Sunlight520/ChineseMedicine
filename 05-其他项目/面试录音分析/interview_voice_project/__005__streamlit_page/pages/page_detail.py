import json
import requests

import streamlit as st


def get_data_by_id(record_id):
    json_data = {
        "record_id": record_id
    }
    data = {
        "json_data_str": json.dumps(json_data, ensure_ascii=False)
    }
    resp = requests.get(
        "http://127.0.0.1:8001/get_interview_records_by_record_id",
        data=data,
        timeout=60,
    )
    if resp.ok:
        result_dict = resp.json()
        data_dict = result_dict.get("data", {})
        return data_dict
    else:
        st.error(f"提交失败：{resp.status_code} {resp.text}")


def page_detail():
    if st.button("← 返回主界面"):
        st.session_state.update({"page": "page_main"})
        st.rerun()
    st.title("面试评价详情页")

    record_id = st.session_state.get("record_id", "")
    # print(record_id)
    data_dict = get_data_by_id(record_id)
    # print(data_dict)
    st.download_button(
        "下载md文件",
        data=str(data_dict['markdown_text']),
        file_name=f"{data_dict['interview_time'][:10]}_{data_dict['name']}_{data_dict['company_name']}_面试评价.md",
        mime="text/markdown",
    )
    st.markdown(str(data_dict['markdown_text']))
