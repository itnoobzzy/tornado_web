#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : YunPian.py
# @Author: itnoobzzy
# @Date  : 2021/2/27
# @Desc  : 发送短信验证码
import requests


class Yunpian:

    def __init__(self, api_key):
        self.api_key = api_key

    def send_single_sms(self, code, mobile):
        """
        发送单条短信
        :param code: 短信验证码
        :param mobile: 手机号
        :return:
        """
        url = "https://sms.yunpian.com/v2/sms/single_send.json"
        text = "【学有涯而知无涯】您的验证码是{}。如非本人操作，请忽略本短信".format(code)
        res = requests.post(url, data={
            "apikey": self.api_key,
            "mobile": mobile,
            "text": text
        })

        return res



if __name__ == '__main__':
    api_key = '53821f80740ec9258f3460f5c57a804a'
    yun_pian = Yunpian(api_key)
    res = yun_pian.send_single_sms('1234', '17720495379')
    print(res.text)