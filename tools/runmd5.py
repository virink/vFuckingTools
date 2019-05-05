#!/bin/env python
# -*- encoding: utf-8 -*-

import md5

def md5x(str):
    m1 = md5.new()
    m1.update(str)
    return m1.hexdigest()


def run(arg):
    code = arg[0]
    start = 10000000
    end = 100000000
    if len(arg) > 2:
        start = arg[1]
    if len(arg) > 3:
        start = arg[2]
    if not code:
        return False
    print 'Runing...'
    while start <= end:
        res = md5x(str(start))[:len(code)]
        if res == code:
            print start
            return start
        start += 1

if __name__ == '__main__':
    run(['1ceac'])