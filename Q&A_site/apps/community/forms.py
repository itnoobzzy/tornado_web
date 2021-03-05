#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : forms.py
# @Author: itnoobzzy
# @Date  : 2021/2/27
# @Desc  : 表单校验

from wtforms_tornado import Form
from wtforms import (
    StringField,
    TextAreaField,
    IntegerField
)
from wtforms.validators import (
    DataRequired,
    Regexp,
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