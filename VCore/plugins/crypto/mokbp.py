#!/bin/env python3
# -*- encoding: utf-8 -*-

'''
Title : MobilePhoneKeyBoardCipher
Author : Virink
Type : crypto
Detail : 手机键盘遍码
Param : @s, @sep
func : encode, decode
'''

TABLE = {
    'A': 21, 'B': 22, 'C': 23, 'D': 31, 'E': 32, 'F': 33,
    'G': 41, 'H': 42, 'I': 43, 'J': 51, 'K': 52, 'L': 53,
    'M': 61, 'N': 62, 'O': 63, 'P': 71, 'Q': 72, 'R': 73, 'S': 74,
    'T': 81, 'U': 82, 'V': 83, 'W': 91, 'X': 92, 'Y': 93, 'Z': 94
}


def decode(s, sep=' '):
    s = s.split(sep)
    return 'Waiting...'


def encode(s, sep=' '):
    s = s.split(sep)
    return 'Waiting...'
