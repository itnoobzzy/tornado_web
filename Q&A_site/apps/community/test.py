#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : test.py
# @Author: itnoobzzy
# @Date  : 2021/2/27
# @Desc  : 测试用例

import requests
import json
from datetime import datetime

import jwt

from qa_site.settings import settings

current_time = datetime.utcnow()


web_url = "http://139.196.161.70:8000"

data = jwt.encode({
    "name": "zzy",
    "id": 1,
    "exp": current_time
}, settings["secret_key"])

headers = {
    "tsessionid": data
}

def new_group():
    files = {
        "front_image": open("/home/tornado_site/1.jpg", "rb")
    }
    data = {
        "name": "学前教育交流角",
        "desc": "这里是学前教育的交流中心，大家有什么问题可以一起来交流讨论！欢迎大家的加入！",
        "notice": "这里是学前教育的交流中心，大家有什么问题可以一起来交流讨论！欢迎大家的加入！",
        "category": "教育同盟"
    }
    res = requests.post("{}/groups/".format(web_url), headers=headers, data=data, files=files)
    print(res.status_code)
    print(json.loads(res.text))


if __name__ == '__main__':
    new_group()