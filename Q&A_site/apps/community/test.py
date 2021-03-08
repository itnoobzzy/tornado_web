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
    """
    测试创建小组
    :return:
    """
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

def apply_group(group_id, apply_reason):
    """
    测试加入小组
    :param group_id: 小组id
    :param apply_reason: 加入理由
    :return:
    """
    data = {
        "apply_reason": apply_reason,
    }
    res = requests.post("{}/groups/{}/members/".format(web_url, group_id), headers=headers, json=data)
    print(res.status_code)
    print(json.loads(res.text))

def get_group(group_id):
    """
    小组详情
    :param group_id:
    :return:
    """
    res = requests.get("{}/groups/{}/".format(web_url, group_id), headers=headers)
    print(res.status_code)
    print(json.loads(res.text))

def add_post(group_id):
    #发帖
    data = {
        "title":"tornado从入门到实战",
        "content":"tornado从入门到实战"
    }
    res = requests.post("{}/groups/{}/posts/".format(web_url, group_id), headers=headers, json=data)
    print(res.status_code)
    print(json.loads(res.text))

def get_posts(group_id):
    res = requests.get("{}/groups/{}/posts/".format(web_url, group_id), headers=headers)
    print(res.status_code)
    print(json.loads(res.text))

def get_detail_post(post_id):
    res = requests.get("{}/posts/{}/".format(web_url, post_id), headers=headers)
    print(res.status_code)
    print(json.loads(res.text))

def add_comments(post_id):
    data = {
        "content": "tornado从入门到实战"
    }
    res = requests.post("{}/posts/{}/comments/".format(web_url, post_id), headers=headers, json=data)
    print(res.status_code)
    print(json.loads(res.text))

def get_comments(post_id):
    res = requests.get("{}/posts/{}/comments/".format(web_url, post_id), headers=headers)
    print(res.status_code)
    print(json.loads(res.text))

def add_reply(comment_id):
    data = {
        "replyed_user": 1,
        "content": "tornado从入门到实战2"
    }
    res = requests.post("{}/comments/{}/replys/".format(web_url, comment_id), headers=headers, json=data)
    print(res.status_code)
    print(json.loads(res.text))

def get_replys(comment_id):
    res = requests.get("{}/comments/{}/replys/".format(web_url, comment_id), headers=headers)
    print(res.status_code)
    print(json.loads(res.text))

def add_like(comment_id):
    res = requests.post("{}/comments/{}/likes/".format(web_url, comment_id), headers=headers, json={})
    print(res.status_code)
    print(json.loads(res.text))

if __name__ == '__main__':
    # new_group()
    # apply_group(2, '理由')
    # get_group(2)
    # add_post(2)
    # get_posts(2)
    # get_detail_post(1)
    # add_comments(1)
    # get_comments(1)
    # add_reply(1)
    add_like(1)