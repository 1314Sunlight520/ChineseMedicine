import asyncio
import json
import shutil

from fastapi import FastAPI, UploadFile, File, Form
import os

from common.markdown_utils import generate_markdown
from common.path_utils import get_file_path, get_file_extension
from common.time_utils import get_current_time, get_datetime_from_str
from __002__db_helper_parse.db_helper import my_db_helper

app = FastAPI()

UPLOAD_DIR = get_file_path("uploaded_files")  # Directory to store the uploaded files
print(UPLOAD_DIR)
# Make sure the upload directory exists
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@app.get("/interview_records")
async def get_interview_records():
    try:
        records = my_db_helper.get_all_interview_records(exclude_fields=["markdown_text"])
        return {"data": records}
    except Exception as e:
        return {"error": str(e)}


@app.get("/get_interview_records_by_record_id")
async def get_interview_records_by_record_id(json_data_str: str = Form(...)):
    try:
        data_dict = json.loads(json_data_str)
        print(data_dict)
        id = data_dict.get("record_id", "")
        records = my_db_helper.get_all_interview_records({"id": id})
        data_dict = records[0]
        # detail_list = my_db_helper.get_analysis_details_by_record_id(interview_record_analysis_id=id)
        # markdown_text = generate_markdown(records, detail_list)
        # print(markdown_text)
        # if len(records) > 0:
        #     records[0]["markdown_text"] = markdown_text
        return {"data": data_dict}
    except Exception as e:
        return {"error": str(e)}


@app.post("/add_interview_record")
async def add_interview_record(
        json_data_str: str = Form(...),  # 获取 JSON 字符串数据
        file: UploadFile = File(...),  # 获取上传的文件
):
    try:
        # 解析 JSON 数据
        data_dict = json.loads(json_data_str)
        print(data_dict)

        name = data_dict.get("name", "")
        company = data_dict.get("company", "")
        subject = data_dict.get("subject", "")
        interview_date_str = data_dict.get("interview_date_str", "")
        print("面试日期：")
        print(interview_date_str)
        extension = get_file_extension(file.filename)
        save_file_name = f"{get_current_time()}_{name}_{company}{extension}"
        # 保存上传的文件到服务器
        relative_path = os.path.join("uploaded_files", save_file_name)
        file_location = os.path.join(UPLOAD_DIR, save_file_name)
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)

        my_db_helper.add_interview_record(name=name, company_name=company, subject=subject,
                                          interview_time=get_datetime_from_str(interview_date_str),
                                          recording_url=relative_path)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
