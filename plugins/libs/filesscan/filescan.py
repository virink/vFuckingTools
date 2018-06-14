#!/bin/env python3
# -*- encoding: utf-8 -*-

# from .common import get_basedomain
from .common import *


def start_spider(siteurl):
    # 目标赋值
    if "://" not in siteurl:
        siteurl = 'http://%s' % siteurl.rstrip('/')
    siteurl = siteurl.rstrip('/')
    basedomain = get_basedomain(siteurl)

    # 初始化字典
    #   备份文件压缩包
    fuzz_bak_ext = loadDic(package_ext_dict)
    #   临时文件
    fuzz_tmp_ext = loadDic(tempfile_ext_dict)
    #   目录
    fuzz_webdirs = loadDic(directory_dict)
    #   IDE or 版本管理
    fuzz_ide_vcs = loadDic(ide_vcs_dict)
    #   文件名
    fuzz_filename = loadDic(filename_dict)


if __name__ == '__main__':
    start_spider("https://www.virzz.com")
