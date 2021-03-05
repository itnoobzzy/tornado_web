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


class GroupMemberHandler(RedisHandler):
    """
    申请加入小组
    """

    @authenticated_async
    async def post(self, group_id, *args, **kwargs):
        ret_data = {}
        param = self.request.body.decode("utf-8")
        param = json.loads(param)
        form = GroupApplyForm.from_json(param)

        if form.validate():
            try:
                # 查询加入的小组是否存在
                group = await self.application.objects.get(CommunityGroup, id=int(group_id))
                # 查询该用户是否已经加入
                existed = await self.application.objects.get(CommunityGroupMember, community=group, user=self.current_user)
            except CommunityGroup.DoesNotExist as e:
                self.set_status(404) # 小组不存在
            except CommunityGroupMember.DoesNotExist as e:
                # 该用户未加入
                community_member = await self.application.objects.create(
                    CommunityGroupMember,
                    community=group,
                    user=self.current_user,
                    apply_reason=form.apply_reason.data
                )
                ret_data["id"] = community_member.id
        else:
            self.set_status(400)
            for field in form.errors:
                ret_data[field] = form.errors[field][0]

        await self.finish(ret_data)


class GroupDetailHandler(RedisHandler):
    """
    小组详情
    """

    @authenticated_async
    async def get(self, group_id, *args, **kwargs):
        # 获取小组基本信息
        ret_data = {}
        try:
            group = await self.application.objects.get(CommunityGroup, id=int(group_id))
            item_dict= {}
            item_dict["name"] = group.name
            item_dict["id"] = group.id
            item_dict["desc"] = group.desc
            item_dict["notice"] = group.notice
            item_dict["member_nums"] = group.member_nums
            item_dict["post_nums"] = group.post_nums
            item_dict["front_images"] = "{}/media/{}".format(self.settings["SITE_URL"], group.front_image)
            ret_data = item_dict

        except CommunityGroup.DoesNotEixst as e:
            self.set_status(404)

        await self.finish(ret_data)


class PostHandler(RedisHandler):
    """
    帖子详情，发表帖子
    """

    @authenticated_async
    async def get(self, *args, **kwargs):
        pass

    @authenticated_async
    async def post(self, group_id, *args, **kwargs):
        """
        发表帖子
        :param group_id: 发帖的小组id
        :param args:
        :param kwargs:
        :return:
        """
        ret_data = {}

        try:
            # 判断小组是否存在，是否为小组内成员
            group = await self.application.objects.get(CommunityGroup, id=int(group_id))

            group_number = await self.application.objects.get(CommunityGroupMember, user=self.current_user, community=group, status="agree")

            param = self.request.body.decode("utf-8")
            param = json.loads(param)
            form = PostForm.from_json(param)
            if form.validate():
                post = await self.application.objects.create(Post, user=self.current_user,title=form.title.data,
                                                             content=form.content.data, group=group)
                ret_data["id"] = post.id
            else:
                self.set_status(400)
                for field in form.errors:
                    ret_data[field] = form.errors[field][0]
        except CommunityGroup.DoesNotExist as e:
            self.set_status(404)
        except CommunityGroupMember.DoesNotExist as e:
            self.set_status(403)
        await self.finish(ret_data)









