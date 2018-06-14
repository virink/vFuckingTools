#!/bin/env python3
# -*- encoding: utf-8 -*-

import urlparse


tempfile_ext_dict = '../dict/tmpfile_ext.lst'

directory_dict = '../dict/directory.lst'
filename_dict = '../dict/filename.lst'
ide_vcs_dict = '../dict/idevcs.lst'
common_dict = '../dict/commons.lst'


def loadDic(dicfile):
    return [line for line in FileUtils.getLines(
        dicfile) if not line.startswith("#")]


def package_dict_list():
    package_exts = ['.rar', '.zip', '.gz', '.tar', '.tgz',
                    '.tar.gz', '.7z', '.z', '.bz2', '.tar.bz2', '.iso', '.cab']
    package_ext_dict = ['www', '201', 'admin', 'web', 'bak']
    package_ext_dict += [j + str(i)
                         for j in package_ext_dict for i in range(0, 10)]
    return [j + i for i in package_exts for j in package_ext_dict]


def get_basedomain(url):
    try:
        return urlparse.urlparse(url).netloc
    except Exception, e:
        pass

if __name__ == '__main__':
    # res = get_basedomain("https://www.virzz.com/links/index.html")
    res = package_dict_list()
    print(res)
