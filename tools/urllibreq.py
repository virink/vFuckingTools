#!/bin/env python
#-*- encoding: utf-8 -*-

import time
import urllib
import urllib2
import json


def post(url, values):
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    req.add_header(
        'user-agent', 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0')
    req.add_header('cache-control', 'no-cache')
    req.add_header('accept', '*/*')
    req.add_header('connection', 'keep-alive')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urllib2.urlopen(req)
    code = response.getcode()
    body = response.read()
    return code, body


if __name__ == '__main__':
    url = 'http://'
    values = {'tel': 'xxx', 'type': "xxx"}
    code, body = post(url, values)
