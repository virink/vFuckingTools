#!/bin/env python3
# -*- encoding: utf-8 -*-

'''
Title : Vigenere
Author : Virink
Type : crypto
Detail : 维吉利亚密码编码/解码
Param : @s, @key
'''


def vigenere(s, key, de=0):
    s = s.replace(" ", "").upper()
    key = key.replace(" ", "").upper()
    _ascii = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    keylen = len(key)
    ctlen = len(s)
    res = ''
    i = 0
    while i < ctlen:
        j = i % keylen
        k = _ascii.index(key[j])
        m = _ascii.index(s[i])
        if de:
            # decode
            if m < k:
                m += 26
            res += _ascii[m - k]
        else:
            # encode
            res += _ascii[(m + k) % 26]
        i += 1
    return res


def encode(s, key):
    return vigenere(s, key)


def decode(s, key):
    return vigenere(s, key, 1)

if __name__ == '__main__':
    print decode(encode("testtest", 'orz'), 'orz')
