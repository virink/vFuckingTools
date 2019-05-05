#!/usr/bin/env python
# -*- coding: utf-8 -*-

#__Author__ = virink
#__Blog__   = https://www.virzz.com

import os
import sys
import commands
import re
import time
import base64
import platform

rulelist = [
    '(\$_(GET|POST|REQUEST)\[.{0,15}\]\s{0,10}\(\s{0,10}\$_(GET|POST|REQUEST)\[.{0,15}\]\))',
    '(base64_decode\([\'"][\w\+/=]{200,}[\'"]\))',
    '(eval(\s|\n)*\(base64_decode(\s|\n)*\((.|\n){1,200})',
    '((eval|assert)(\s|\n)*\((\s|\n)*\$_(POST|GET|REQUEST)\[.{0,15}\]\))',
    '(\$[\w_]{0,15}(\s|\n)*\((\s|\n)*\$_(POST|GET|REQUEST)\[.{0,15}\]\))',
    '(call_user_func\(.{0,15}\$_(GET|POST|REQUEST))',
    '(preg_replace(\s|\n)*\(.{1,100}[/@].{0,3}e.{1,6},.{0,10}\$_(GET|POST|REQUEST))',
    '(wscript\.shell)',
    '(cmd\.exe)',
    '(shell\.application)',
    '(documents\s+and\s+settings)',
    '(serv-u)',
    '(phpspy)',
    '(jspspy)',
    '(webshell)',
    '(Program\s+Files)'
]


def ScanShell(path):
    for root, dirs, files in os.walk(path):
        for filespath in files:
            if filespath.find('.php') > 0 or filespath.find('.inc') > 0:
                file = open(os.path.join(root, filespath))
                filestr = file.read()
                file.close()
                for rule in rulelist:
                    result = re.compile(rule).findall(filestr)
                    if result:
                        print os.path.join(root, filespath) + '\r\n'
                        break

##############################################
if __name__ == '__main__':
    print '''
\t\t#########################################
\t\t#   AppName :   Scan Shell              #
\t\t#   Author  :   Virink                  #
\t\t#   Blog    :   https://www.virzz.com   #
\t\t#########################################\r\n'''
    if platform.system() != 'Linux':
        print '\tPlease Run in Linux'
        exit()
    if len(sys.argv) != 2:
        print '\tRun error\r\n\tUsage:python ' + sys.argv[0] + ' website_path\r\n\teg : python ' + sys.argv[0] + ' /root/www\r\n'
        exit()
    webroot = sys.argv[1]
    # Start scan webshell
    print '\tStart scan webshell'
    ScanShell(webroot)
    print '\tFinish scan webshell'
