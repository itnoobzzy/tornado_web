#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : urls.py
# @Author: itnoobzzy
# @Date  : 2021/3/9
# @Desc  :
from tornado.web import url

from apps.question.handler import *

urlpattern = (
    url("/questions/", QuestionHandler),
    url("/questions/([0-9]+)/", QuestionDetailHandler),
    #
    # #问题回答
    url("/questions/([0-9]+)/answers/", AnswerHandler),
    url("/answers/([0-9]+)/replys/", AnswerReplyHandler),
)