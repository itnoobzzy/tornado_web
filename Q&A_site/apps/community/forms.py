#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : forms.py
# @Author: itnoobzzy
# @Date  : 2021/2/27
# @Desc  : 小组，评论表单校验

from wtforms_tornado import Form
from wtforms import (
    StringField,
    TextAreaField,
    IntegerField
)
from wtforms.validators import (
    DataRequired,
    AnyOf,
    Length
)

class CommunityGroupForm(Form):
    name = StringField("名称", validators=[DataRequired("请输入小组名称")])
    category = StringField("类别", validators=[AnyOf(values=["教育同盟", "同城交易", "程序设计", "生活兴趣"])])
    desc = TextAreaField("简介", validators=[DataRequired(message="请输入简介")])
    notice = TextAreaField("公告", validators=[DataRequired(message="请输入公告")])
    front_image = StringField("封面图", validators=[DataRequired(message="请输入公告")])

class GroupApplyForm(Form):
    apply_reason = StringField("申请理由", validators=[DataRequired("请输入申请理由")])

class PostForm(Form):
    title = StringField("标题", validators=[DataRequired("请输入标题")])
    content = StringField("内容", validators=[DataRequired("请输入内容")])

class PostCommentForm(Form):
    content = StringField("内容", validators=[DataRequired("请输入评论内容"),
                                            Length(min=3, message="内容不能少于3个字符")])
class CommentReplyForm(Form):
    replyed_user = IntegerField("回复用户", validators=[DataRequired("请输入回复用户")])
    content = StringField("内容", validators=[DataRequired("请输入评论内容"),
                                            Length(min=3, message="内容不能少于3个字符")])