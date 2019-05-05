# - coding:utf8
from flask import *
import requests

app = Flask(__name__)

url = "http://172.91.1.12:9090/arace/index"
token = "0ade4d3d8b7ed42f"

server_port = 3001


def submit_token(url, answer, token):
    data = {"token": token, "flag": answer}
    resp = requests.post(url, data=data)
    if (resp.status_code != "404"):
        print "Status code:%d" % (resp.status_code)


def submit_cookie(ip, answer):
    submit_ip = '172.91.1.12:9090'
    urls = 'http://%s/ad/hacker/submit/submitCode' % submit_ip
    post = {'flag': answer}
    '''cmder = ' %s -b "JSESSIONID=C64DD133EFDDB22CE5BE4CA3991AB6DF" -d "flag=%s"'% (urls,answer)
                #print cmd
                os.system('curl ' + cmder)'''

    header = {'Host': '172.91.1.12:9090',
              'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
              'Accept': 'application/json, text/javascript, */*; q=0.01',
              'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
              'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
              'X-Requested-With': 'XMLHttpRequest',
              'Referer': 'http://172.91.1.12:9090/arace/index',
              'Content-Length': '14',
              'Cookie': 'JSESSIONID=77A0AFA7757CE43018889FCF9AAFE59A'}

    req = requests.post(urls, headers=header, data=post)
    print req.content
    if 'errorInfo' not in req.content:
        print ' ' + req.content


last_flag = {}


@app.route('/flag', methods=['POST'])
def receive_flag():
    flag = request.get_data().strip()
    ip = request.remote_addr
    if not last_flag.has_key(ip):
        last_flag[ip] = set()
    ip_flag_list = last_flag.get(ip, set())
    if flag in ip_flag_list:
        print "Receive %s from %s , already submitted." % (flag, ip)
        return ""
    ip_flag_list.add(flag)
    result = ""
    print "\nReceive from : %s\nflag : %s" % (ip, flag)
    submit_cookie(ip, flag)
    return ''


if __name__ == '__main__':
    app.run("0.0.0.0", port=server_port)
