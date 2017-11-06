#!/bin/env python3
# -*- encoding: utf-8 -*-

'''
Title : AtbashCipher
Author : Virink
Type : crypto
Detail : 埃特巴什码解码
Param : @s
func :  decode
'''

TABLE = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
         'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def decode(s):
    s = s.lower().replace(' ', 'vvvzzzvvv')
    res = [TABLE[25 - j]
           for i in s for j in range(len(TABLE)) if i == TABLE[j]]
    return ''.join(res).replace('eeeaaaeee', ' ')
