#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : handler.py
# @Author: itnoobzzy
# @Date  : 2021/2/27
# @Desc  :
import os
import uuid
import json

import aiofiles
from playhouse.shortcuts import model_to_dict

from qa_site.handler import RedisHandler
from apps.utils.my_decorators import authenticated_async
from apps.community.forms import *
from apps.community.models import *
from apps.utils.util_func import json_serial

class GroupHandler(RedisHandler):

    async def get(self, *args, **kwargs):
        # 获取小组列表
        ret_data = []
        # 此处只能使用自定义查询集，不能使用select,因为CommunityGroup存在外键，异步驱动会报错
        community_query = CommunityGroup.extend()

        # 根据类别进行过滤
        c = self.get_argument("c", None)
        if c:
            community_query = community_query.filter(CommunityGroup.category==c)

        # 根据参数进行排序
        order = self.get_argument("o", None)
        if order:
            if order == "new":
                community_query = community_query.order_by(CommunityGroup.add_time.desc())
            elif order == "hot":
                community_query = community_query.order_by(CommunityGroup.member_nums.desc())

        limit = self.get_argument("limit", None)
        if limit:
            community_query = community_query.limit(int(limit))

        groups = await self.application.objects.execute(community_query)
        for group in groups:
            group_dict = model_to_dict(group)
            group_dict["front_image"] = "{}/media/{}/".format(self.settings["SITE_URL"], group_dict["front_image"])
            ret_data.append(group_dict)

        await self.finish(json.dumps(ret_data, default=json_serial))



    @authenticated_async
    async def post(self, *args, **kwargs):
        ret_data = {}

        # 不能使用jsonform 要使用wtform自身获取参数
        group_form = CommunityGroupForm(self.request.body_arguments)
        if group_form.validate():
            # 自己完成图片的验证
            # 接收图片名
            files_meta = self.request.files.get("front_image", None)
            if not files_meta:
                self.set_status(400)
                ret_data["front_image"] = "请上传图片"
            else:
                # 完成图片的保存并将值设置给对应的记录，通过aiofiles写文件
                new_filename = ""
                for meta in files_meta:
                    filename = meta["filename"]
                    new_filename = "{uuid}_{filename}".format(uuid=uuid.uuid1(), filename=filename)
                    file_path = os.path.join(self.settings["MEDIA_ROOT"], new_filename)
                    # 异步读写文件
                    async with aiofiles.open(file_path, 'wb') as f:
                        await f.write(meta["body"])
                # 异步保存至数据库
                data = {
                    "creator": 1,
                    "name": group_form.name.data,
                    "category": group_form.category.data,
                    "desc": group_form.desc.data,
                    "notice": group_form.notice.data,
                    "front_image": new_filename
                }
                group = await self.application.objects.create(CommunityGroup, **data)
                ret_data["id"] = group.id
        else:
            # 表单校验不通过
            self.set_status(400)
            for field in group_form.errors:
                ret_data[field] = group_form.errors[field][0]
        await self.finish(ret_data)















