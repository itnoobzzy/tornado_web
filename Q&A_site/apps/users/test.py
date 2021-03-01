#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : test.py
# @Author: itnoobzzy
# @Date  : 2021/2/27
# @Desc  : 测试用例

import requests

web_url = "http://139.196.161.70:8000"
def test_sms():
    url = "{}/code/".format(web_url)
    data = {
        "mobile": "17720495379"
    }
    res = requests.post(url, json=data)
    print(res.text)

if __name__ == '__main__':
    test_sms()