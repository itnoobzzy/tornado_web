#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : AsyncYunpian.py
# @Author: itnoobzzy
# @Date  : 2021/2/27
# @Desc  : 异步发送短信

import json
from urllib.parse import urlencode

from tornado import (
    httpclient,
    ioloop
)
from tornado.httpclient import HTTPRequest


class Yunpian:

    def __init__(self, api_key):
        self.api_key = api_key

    async def send_single_sms(self, code, mobile):
        """
        异步发送单条短信
        :param code: 短信验证码
        :param mobile: 手机号
        :return:
        """
        http_client = httpclient.AsyncHTTPClient()
        url = "https://sms.yunpian.com/v2/sms/single_send.json"
        text = "【学有涯而知无涯】您的验证码是{}。如非本人操作，请忽略本短信".format(code)
        post_request = HTTPRequest(url, method="Post", body=urlencode({
            "apikey": self.api_key,
            "mobile": mobile,
            "text": text
        }))
        res = await http_client.fetch(post_request)
        return json.loads(res.body.decode("utf-8"))


if __name__ == '__main__':
    api_key = '53821f80740ec9258f3460f5c57a804a'
    yun_pian = Yunpian(api_key)
    from functools import partial
    new_func = partial(yun_pian.send_single_sms, "1234", "17720495379")
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(new_func)
