#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-08-10 13:04:42
# @Author  : Virink (virink@outlook.com)
# @Link    : https://www.virzz.com
# @Version : $Id$

import os
import requests as req

URL = ""


def submit(flag):
    data = {
        "flag": flag
    }
    res = req.post(URL, data)
    if res.status_code == 200:
        return True
    else:
        return False

if __name__ == '__main__':
    flag = "flag{test]"
    res = submit(flag)
    print(res)
