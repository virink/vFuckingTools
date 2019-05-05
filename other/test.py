# coding:utf-8
#
import requests
import urllib
import hashlib
import bs4

req = requests.get("http://106.75.67.214:2250")
_cookies = req.cookies
text = req.headers['Ciphertext']
print text

content = req.content
bsobj = bs4.BeautifulSoup(content, "html.parser")
part = bsobj.findAll(text=lambda text: isinstance(text, bs4.Comment))[
    2].split("+")[1].split(")")[0]
print part

for i in range(100, 999):
    dest = str(i)+part
    if hashlib.sha1(dest).hexdigest() == text:
        data = {"pass": i}
        req = requests.post(
            "http://106.75.67.214:2250", data=data, cookies=_cookies)
        print req.content

        bsobj = bs4.BeautifulSoup(req.content, "html.parser")
        print bsobj.findAll(text=lambda text: isinstance(text, bs4.Comment))[2]
        part = bsobj.findAll(text=lambda text: isinstance(text, bs4.Comment))[
            2].split(u"\uff1a")[1]

        result = eval(part)

        data = {"pass": result}
        req = requests.post(
            "http://106.75.67.214:2250", data=data, cookies=_cookies)
        print req.content  # flag{f325c62b-9505-4c13-ad4b-010bddb23c68}

        break

    else:
        continue
