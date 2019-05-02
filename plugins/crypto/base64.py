#!/bin/env python3
# -*- encoding: utf-8 -*-

'''
Title : Base64编码
Author : Virink
Type : crypto
Detail : Base64/32/16编码/解密
Param : @s, @bit
func : encode, decode
'''

import base64


def encode(s, bit=64):
    if bit == 16:
        return base64.b16encode(s)
    elif bit == 32:
        return base64.b32encode(s)
    else:
        return base64.b64encode(s)


def decode(s, bit=64):
    if bit == 16:
        return base64.b16decode(s)
    elif bit == 32:
        return base64.b32decode(s)
    else:
        return base64.b64decode(s)


if __name__ == '__main__':
    encode('aaa')
