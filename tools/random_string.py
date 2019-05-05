#!/bin/env python
#-*- encoding: utf-8 -*-

import string
import random
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


def randstr(num=10):
    return string.join(random.sample(['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e', 'd', 'c', 'b', 'a'], num)).replace(' ', '')

if __name__ == '__main__':
    print randstr()
