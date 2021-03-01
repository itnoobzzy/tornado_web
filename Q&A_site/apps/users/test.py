#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : test.py
# @Author: itnoobzzy
# @Date  : 2021/2/27
# @Desc  : 测试用例

import requests
import json

web_url = "http://139.196.161.70:8000"
def test_sms():
    """
    测试发送短信
    :return:
    """
    url = "{}/code/".format(web_url)
    data = {
        "mobile": "17720495379"
    }
    res = requests.post(url, json=data)
    print(res.text)

def test_register():
    """
    测试注册
    :return:
    """
    url = "{}/register/".format(web_url)
    data = {
        "mobile": "17720495379",
        "code": "5849",
        "password": "admin123"
    }
    res = requests.post(url, json=data)
    print(json.loads(res.text))

if __name__ == '__main__':
    # test_sms()
    test_register()