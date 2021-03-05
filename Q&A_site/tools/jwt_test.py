#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File  : jwt_test.py
# @Author: itnoobzzy
# @Date  : 2021/3/3
# @Desc  :

from datetime import datetime

import jwt
from qa_site.settings import settings

current_time = datetime.utcnow()

data = {
    "name": "bobby",
    "id": 1,
    "exp": current_time
}
encode_data = jwt.encode(data, "abc")

send_data = jwt.decode(encode_data, settings["secret_key"], algorithms='HS256', leeway=1, options={"verify_signature":False})
print(send_data)