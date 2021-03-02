#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : handler.py
# @Author: itnoobzzy
# @Date  : 2021/2/27
# @Desc  :

import json
from random import choice
from datetime import datetime

from tornado.web import RequestHandler
import jwt

from apps.users.forms import (
    SmsCodeForm,
    RegisterForm,
    LoginFrom
)
from apps.users.models import User
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
            # yun_pian = Yunpian(api_key)
            #
            # ret_json = await yun_pian.send_single_sms(code, mobile)
            # if ret_json["code"] != 0:
            #     # 参数错误
            #     self.set_status(400)
            #     ret_data["mobile"] = ret_json["msg"]
            # else:
            #     # 将验证码写入redis中
            #     self.redis_conn.set("{}_{}".format(mobile, code), 1, 10*60)

            self.redis_conn.set("{}_{}".format(mobile, code), 1, 10*60)
        else:
            self.set_status(400)
            for field in sms_form.errors:
                ret_data[field] = sms_form.errors[field][0]
        await self.finish(ret_data)


class RegisterHandler(RedisHandler):
    """
    注册功能
    """

    async def post(self, *args, **kwargs):
        ret_data = {}

        param = self.request.body.decode("utf-8")
        param = json.loads(param)
        register_form = RegisterForm.from_json(param)
        if register_form.validate():
            # 表单合法
            mobile = register_form.mobile.data
            code = register_form.code.data
            password = register_form.password.data

            # 从redis中获取验证码
            redis_key = "{}_{}".format(mobile, code)
            if not self.redis_conn.get(redis_key):
                self.set_status(400)
                ret_data["code"] = "验证码错误或者失效"
            else:
                try:
                    existed_user = await self.application.objects.get(User, mobile=mobile)
                    self.set_status(400)
                    ret_data["mobile"] = "用户已经存在"
                except User.DoesNotExist as e:
                    user = await self.application.objects.create(User, mobile=mobile, password=password)
                    ret_data["id"] = user.id
        else:
            # 表单不合法
            self.set_status(400)
            for field in register_form.errors:
                ret_data[field] = register_form[field][0]

        await self.finish(ret_data)


class LoginHandler(RedisHandler):
    """
    登录功能
    """
    async def post(self, *args, **kwargs):
        ret_data = {}
        param = self.request.body.decode("utf-8")
        param = json.loads(param)
        form = LoginFrom.from_json(param)

        if form.validate():
            mobile = form.mobile.data
            password = form.password.data

            try:
                user = await self.application.objects.get(User, mobile=mobile)
                if not user.password.check_password(password):
                    self.set_status(400)
                    ret_data["non_fields"] = "用户名或密码错误"
                else:
                    # 登录成功，生成json web token
                    pay_load = {
                        "id": user.id,
                        "nick_name": user.nick_name,
                        "exp": datetime.utcnow()
                    }
                    token = jwt.encode(pay_load, self.settings["secret_key"], algorithm='HS256')
                    ret_data["id"] = user.id
                    # 用户如果设置匿名就返回匿名
                    if user.nick_name is not None:
                        ret_data["nick_name"] = user.nick_name
                    else:
                        ret_data["nick_name"] = user.mobile
                    ret_data["token"] = token
            except User.DoesNotExist as e:
                self.set_status(400)
                ret_data["mobile"] = "用户不存在"

            await self.finish(ret_data)

















