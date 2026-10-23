from volcengine.visual.VisualService import VisualService
from common.config import Config

conf = Config()


def generate_image():
    visual_service = VisualService()
    visual_service.set_ak(conf.JIMENG_AK)  # 替换为你自己的 AK
    visual_service.set_sk(conf.JIMENG_SK)  # 替换为你自己的 SK

    form = {
        "req_key": "jimeng_high_aes_general_v21_L",
        "prompt": "生成一张小猫图片",
        "return_url": True
    }

    resp = visual_service.cv_process(form)
    image_urls = resp.get('data', {}).get('image_urls', [])
    print(image_urls)


generate_image()
