#!/bin/env python3
# -*- encoding: utf-8 -*-

'''
Title : ASCII
Author : Virink
Type : crypto
Detail : 美国信息交换标准代码编码/解码
Param : @s
func : encode, decode
'''


def encode(s):
    return ' '.join([str(ord(i)) for i in s])


def decode(s):
    return ''.join([chr(int(i)) for i in s.split(' ')])
