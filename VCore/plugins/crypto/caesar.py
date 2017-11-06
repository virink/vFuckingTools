#!/bin/env python3
# -*- encoding: utf-8 -*-

'''
Title : Caesar
Author : Virink
Type : crypto
Detail : 凯撒编码
Param : @s, @offset
'''

TABLE_AZ_U = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
              'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

TABLE_AZ_L = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
              'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def encode(s):
    return caesar(s)


def decode(s):
    return caesar(s)


def caesar(s):
    res = []
    for offset in range(26):
        r = ""
        for ch in s:
            if ch.isupper():
                r += TABLE_AZ_U[((TABLE_AZ_U.index(ch) + offset) % 26)]
            elif ch.islower():
                r += TABLE_AZ_L[((TABLE_AZ_L.index(ch) + offset) % 26)]
            elif ch.isdigit():
                r += ch
            else:
                r += ch
        res.append({'offset': o, 'result': result})
    # return '\n'.join(res)
    return res
