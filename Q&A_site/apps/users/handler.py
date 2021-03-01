#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : handler.py
# @Author: itnoobzzy
# @Date  : 2021/2/27
# @Desc  :

import json
from random import choice
from tornado.web import RequestHandler

from apps.users.forms import SmsCodeForm
from apps.utils.AsyncYunpian import Yunpian
from qa_site.handler import RedisHandler

class SmsHandler(RedisHandler):

    def generate_code(self):
        """
        生成随机4位的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)

    async def get(self, *args, **kwargs):
        self.write('hello')

    async def post(self, *args, **kwargs):
        ret_data = {}

        param = self.request.body.decode("utf-8")
        param = json.loads(param)
        # 接收的param是json数据需要使用wtforms_json的猴子补丁将json集成到Form中
        sms_form = SmsCodeForm.from_json(param)

        if sms_form.validate():
            code = self.generate_code()
            mobile = sms_form.mobile.data
            api_key = '53821f80740ec9258f3460f5c57a804a'
            yun_pian = Yunpian(api_key)

            ret_json = await yun_pian.send_single_sms(code, mobile)
            if ret_json["code"] != 0:
                # 参数错误
                self.set_status(400)
                ret_data["mobile"] = ret_json["msg"]
            else:
                # 将验证码写入redis中
                self.redis_conn.set("{}_{}".format(mobile, code), 1, 10*60)
        else:
            self.set_status(400)
            for field in sms_form.errors:
                ret_data[field] = sms_form.errors[field][0]
        await self.finish(ret_data)