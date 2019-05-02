#!/bin/env python3
# -*- encoding: utf-8 -*-

'''
Title : Caesar
Author : Virink
Type : crypto
Detail : 凯撒编码
Param : @s, @offset
func : encode, decode
'''

TABLE_NUM = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

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
    for offset in range(len(TABLE_AZ_L)):
        result = ""
        for ch in s:
            if ch.isupper():
                result += TABLE_AZ_U[((TABLE_AZ_U.index(ch) + offset) % 26)]
            elif ch.islower():
                result += TABLE_AZ_L[((TABLE_AZ_L.index(ch) + offset) % 26)]
            elif ch.isdigit():
                result += ch
            else:
                result += ch
        res.append({'offset': offset, 'result': result})
    return res


def caesar2(s):
    TABLE = TABLE_NUM + TABLE_AZ_L
    res = []
    for offset in range(len(TABLE)):
        result = ""
        for ch in s:
            if ch.isupper():
                result += TABLE_AZ_U[((TABLE_AZ_U.index(ch) + offset) % 26)]
            elif ch.islower():
                result += TABLE_AZ_L[((TABLE_AZ_L.index(ch) + offset) % 26)]
            elif ch.isdigit():
                result += TABLE_NUM[((TABLE_NUM.index(ch) + offset) % 10)]
                # result += ch
            else:
                result += ch
        if 'lwz' in result:
            res.append({'offset': offset, 'result': result})
    # return '\n'.join(res)
    return res


if __name__ == '__main__':
    print(caesar("the tragedy of caesar"))
    # a = "lzw ljsywvq gx uswksj"
    # b = "lwk ynyzwqy gu ofaqtj"
    # # print(ord('w') - ord('a'))
    # # the tragedy of caesar
    # # lzw ljsywvq gx uswksj
    # # lwk ynyzwqy gu ofaqtj
    # for i in range(len(a)):
    #     print(ord(a[i]) - ord(b[i]))
