#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: itnoobzzy
# @Date  : 2021/2/27
# @Desc  : users url配置

from tornado.web import url

from apps.community.handler import (
    GroupHandler,
    GroupMemberHandler,
    GroupDetailHandler,
    PostHandler,
    PostDetailHandler,
    PostCommentHandler,
    CommentReplyHandler,
    CommentsLikeHanlder
)

urlpattern = (
    url("/groups/", GroupHandler),
    url("/groups/([0-9]+)/", GroupDetailHandler),
    url("/groups/([0-9]+)/members/", GroupMemberHandler),
    # 发表帖子
    url("/groups/([0-9]+)/posts/", PostHandler),

    # 帖子详情
    url("/posts/([0-9]+)/", PostDetailHandler),

    # 评论
    url("/posts/([0-9]+)/comments/", PostCommentHandler),
    url("/comments/([0-9]+)/replys/", CommentReplyHandler),
    url("/comments/([0-9]+)/likes/", CommentsLikeHanlder),
)