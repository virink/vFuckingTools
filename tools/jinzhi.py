#!/bin/env python
#-*- encoding: utf-8 -*-

import binascii

__info__ = {
    "desc": "A script for running firesun's verify code",
    "version": "1.0",
    "usage": "",
    "Error": "This script has some error"
}


def str_to_bin_num(s):
    xx = ''
    for i in s:
        x = bin(ord(i)).replace('0b', '')
        if len(x) < 8:
            x = '0' + x
        xx += x
    return xx


def str_to_bin_num_2(s):
    xx = ''
    for i in s:
        xx += bin(ord(i)).replace('0b', '')
        xx += ','
    return xx[:-1]


def bin_num_to_str(b):
    x = ''
    i = 8
    while i <= len(b):
        o = int('0b' + b[i - 8:i], base=2)
        x += chr(o)
        i += 8
    return x


def bin_num_to_hex(b):
    x = ''
    i = 8
    while i <= len(b):
        x += str(hex(int('0b' + b[i - 8:i], base=2))).replace('0x', '\\x')
        i += 8
    return x


def bin_num_to_hex2(b):
    x = ''
    i = 8
    while i <= len(b):
        x += str(hex(int('0b' + b[i - 8:i], base=2))).replace('0x', '')
        i += 8
    return '0x' + x


def fuck2(a, b):
    x = ''
    for i in xrange(len(a)):
        x += str(int(a[i]) ^ int(b[i]))
    return x

if __name__ == '__main__':
    a = str_to_bin_num('javascript:alert(/xss/);')
    c = bin_num_to_hex(a)
    print c
