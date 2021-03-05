#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : my_decorators.py
# @Author: itnoobzzy
# @Date  : 2021/3/3
# @Desc  : 自定义装饰器

import functools

import jwt

from apps.users.models import User

def authenticated_async(method):
    """
    异步token登录验证装饰器
    :param method:
    :return:
    """
    @functools.wraps(method)
    async def wrapper(self, *args, **kwargs):
        # 从headers中获取sessionid(token)
        tsessionid = self.request.headers.get("tsessionid", None)
        if tsessionid:
            try:
                # 使用jwt解码获取数据，异常为过期
                send_data = jwt.decode(tsessionid, self.settings["secret_key"], algorithms='HS256', leeway=self.settings["jwt_expire"], options={"verify_signature":True})
                user_id = send_data["id"]
                # 从异步数据库对象Objects中获取到user, 并设置给_current_user
                try:
                    user = await self.application.objects.get(User, id=user_id)
                    self._current_user = user
                    # 使用装饰器的时候会先运行装饰器，和被装饰的方法，因为装饰的是异步方法，不适用await就无法执行该方法
                    await method(self, *args, **kwargs)
                except User.DoesNotExist as e:
                    self.set_status(401)
            except jwt.ExpiredSignatureError as e:
                self.set_status(401)
        else:
            self.set_status(401)
        await self.finish({})
    return wrapper