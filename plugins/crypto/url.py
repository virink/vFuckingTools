#!/bin/env python3
# -*- encoding: utf-8 -*-

'''
Title : URL
Author : Virink
Type : crypto
Detail : URL编码
Param : @s, @plus, @charset=utf-8
func : encode, decode
'''

from urllib.parse import quote, unquote, quote_plus, unquote_plus


def encode(s, plus=False, charset='utf-8'):
    s = s.encode(charset)
    if plus:
        return quote_plus(s)
    return quote(s)


def decode(s, plus=False, charset='utf-8'):
    s = s.encode(charset)
    if plus:
        return unquote_plus(s)
    return unquote(s)

if __name__ == '__main__':
    URL = 'https://www.virzz.com?你好'
    print(encode(URL))
    print(encode(URL, 1))
