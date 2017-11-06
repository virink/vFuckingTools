#!/bin/env python3
# -*- encoding: utf-8 -*-

'''
Title : Peigen
Author : Virink
Type : crypto
Detail : 培根密码编码/解码
Param : @s
'''

TABLE_PAIGEN = {
    'aabbb': 'H', 'aabba': 'G', 'baaab': 'R', 'baaaa': 'Q',
    'bbaab': 'Z', 'bbaaa': 'Y', 'abbab': 'N', 'abbaa': 'M',
    'babaa': 'U', 'babab': 'V', 'abaaa': 'I', 'abaab': 'J',
    'aabab': 'F', 'aabaa': 'E', 'aaaaa': 'A', 'aaaab': 'B',
    'baabb': 'T', 'baaba': 'S', 'aaaba': 'C', 'aaabb': 'D',
    'abbbb': 'P', 'abbba': 'O', 'ababa': 'K', 'ababb': 'L',
    'babba': 'W', 'babbb': 'X'}


def encode(s):
    res = ''
    for i in range(0, len(s)):
        res = res + TABLE_PAIGEN[s[i].upper()]
    return res


def decode(s):
    sums = len(s)
    j = 5  # 每5个为一组
    res = ''
    for i in range(sums / j):
        result = s[j * i:j * (i + 1)].lower()
        res = res + TABLE_PAIGEN[result]
    return res

if __name__ == '__main__':
    print decode("babbababaababbababaaababaaaaaaabaaa")
