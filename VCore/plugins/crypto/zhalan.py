#!/bin/env python3
# -*- encoding: utf-8 -*-

'''
Title : Zhalan
Author : Virink
Type : crypto
Detail : 栅栏密码
Param : @s
'''


def decode(s):
    res = []
    s = s.decode('utf-8')
    elen = len(s)
    field = [i for i in range(2, elen) if elen % i == 0]
    for f in field:
        b = elen / f
        result = {x: '' for x in range(b)}
        for i in range(elen):
            a = i % b
            result.update({a: result[a] + s[i]})
        d = ''
        for i in range(b):
            d = d + result[i]
        res.append({'offset': f, 'result': d})
    return res

if __name__ == '__main__':
    print decode("ytt{hlniaabatiicfzaammhoina}")
