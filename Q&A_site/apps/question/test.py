#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : test.py
# @Author: itnoobzzy
# @Date  : 2021/3/9
# @Desc  :

import json
from datetime import datetime
import requests
import jwt

current_time = datetime.utcnow()

from qa_site.settings import settings

web_site_url = "http://139.196.161.70:8000"
data = jwt.encode({
    "name": "zzy",
    "id": 1,
    "exp": current_time
}, settings["secret_key"])

headers = {
    "tsessionid": data
}

def new_question():
    files = {
        "image": open("/home/tornado_site/1.jpg", 'rb')
    }
    data = {
        "title": "tornado问题",
        "content": "这里是学前教育的交流中心，大家有什么问题可以一起来交流讨论！欢迎大家的加入！",
        "category": "技术问答"
    }
    res = requests.post("{}/questions/".format(web_site_url), headers=headers, data=data, files=files)
    print(res.status_code)
    print(json.loads(res.text))

def get_questions():
    res = requests.get("{}/questions/".format(web_site_url), headers=headers)
    print(res.status_code)
    print(json.loads(res.text))

def get_questions_details(id):
    res = requests.get("{}/questions/{}/".format(web_site_url, id), headers=headers)
    print(res.status_code)
    print(json.loads(res.text))

if __name__ == '__main__':
    # new_question()
    # get_questions()
    get_questions_details(1)
