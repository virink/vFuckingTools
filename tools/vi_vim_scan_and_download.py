# -*- coding: utf-8 -*-
# __Author__: Byblue
# __Change__: Virink

import time
import urllib
import urllib2


interval = 1

websites = {
    "http://web.l-ctf.com:55533": "php"
}
script = {
    "general": {
        "/robots.txt", "/install.txt", "/password.txt", "/readme.txt", "/sql.txt", "/Password.txt", "/ReadMe.txt",
        "/www.rar", "/wwwroot.rar", "/webroot.rar", "/backup.rar",
        "/www.zip", "/wwwroot.zip", "/webroot.zip", "/backup.zip",
        "/DS_Store", "/.DS_Store", "/.svn/entries", "/.htaccess", "/.git/config"
    },
    "php": {
        "index.php",
        "config.php"
    },
    "jsp": {
        "index.jsp",
        "config.jsp"
    },
    "asp": {
        "index.asp",
        "config.asp"
    },
    "aspx": {
        "index.aspx",
        "config.aspx"
    },
    "discuz": {
        "config/config_global.php",  # discuz
        "config/config_ucenter.php",  # discuz
        "uc_server/data/config.inc.php"  # discuz
    },
    "dede": {
        "data/common.inc.php",  # dede old version
        "include/config_base.php"  # dede new version
    },
    "qibo": {
        "data/mysql_config.php"  # qibo
    },
    "thinkphp": {
        "Common/Conf/config.php"  # thinkphp
    }
}


def getScriptConfig(sc):
    if script.has_key(sc):
        return script[sc]
    else:
        return script['php']


def downLoad(fileUrl, path="./downloads/"):
    try:
        u = urllib2.urlopen(fileUrl)
        #data = u.read()
        splitPath = fileUrl.split('/')
        fName = splitPath.pop()
        print "Downloading: %s " % (fName)
        start = fileUrl.find('://')+3
        end = fileUrl.find('/', start)
        urllib.urlretrieve(fileUrl, path+fileUrl[start:end]+"_"+fName)
    except Exception, e:
        print "[+]%s----%s" % (fileUrl, e)


def usage():
    print "no usage."


def main():
    generalBackup = getScriptConfig('general')

    while (True):
        for backup in generalBackup:
            for website in websites.keys():
                script = websites[website]
                downLoad(website+backup)
                time.sleep(interval)

        for backup in vimBackup:
            for website in websites.keys():
                script = websites[website]
                if isinstance(getScriptConfig(script), set):
                    vimBackup = getScriptConfig(script)
                path = website+backup
                idx = path.rfind('/')
                downLoad(path[0:idx]+"/" + path[idx+1:]+".bak")
                time.sleep(interval)

        for backup in vimBackup:
            for website in websites.keys():
                script = websites[website]
                if isinstance(getScriptConfig(script), set):
                    vimBackup = getScriptConfig(script)
                path = website+backup
                idx = path.rfind('/')
                downLoad(path[0:idx]+"/" + path[idx+1:]+"~")
                time.sleep(interval)

        for backup in vimBackup:
            for website in websites.keys():
                script = websites[website]
                if isinstance(getScriptConfig(script), set):
                    vimBackup = getScriptConfig(script)
                path = website+backup
                idx = path.rfind('/')
                downLoad(path[0:idx]+"/."+path[idx+1:]+".swp")
                time.sleep(interval)
        break
if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
