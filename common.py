#!/bin/env python3
# -*- encoding: utf-8 -*-

import random


def random_str():
    res = ""
    s = "qwertyuiopasdfghjklzxcvbnm,.1234567890-=!@#$%^&*()_ZXCVBNM<>?ASDFGHJKL:WERTYIOP"
    for i in range(0, 128):
        res = res + random.choice(s)
    return res
