#!/bin/env python3
# -*- encoding: utf-8 -*-

'''
Title : Morse
Author : Virink
Type : crypto
Detail : 摩斯电码
Param : @s
func : encode, decode
'''

MORSE_TABLE = {
    'A': '.-',     'B': '-...',   'C': '-.-.',
    'D': '-..',    'E': '.',      'F': '..-.',
    'G': '--.',    'H': '....',   'I': '..',
    'J': '.---',   'K': '-.-',    'L': '.-..',
    'M': '--',     'N': '-.',     'O': '---',
    'P': '.--.',   'Q': '--.-',   'R': '.-.',
    'S': '...',    'T': '-',      'U': '..-',
    'V': '...-',   'W': '.--',    'X': '-..-',
    'Y': '-.--',   'Z': '--..',
    '0': '-----',  '1': '.----',  '2': '..---',
    '3': '...--',  '4': '....-',  '5': '.....',
    '6': '-....',  '7': '--...',  '8': '---..',
    '9': '----.',
    ',': '--..--', '.': '.-.-.-', ':': '---...', ';': '-.-.-.',
    '?': '..--..', '=': '-...-',  "'": '.----.', '/': '-..-.',
    '!': '-.-.--', '-': '-....-', '_': '..--.-', '(': '-.--.',
    ')': '-.--.-', '$': '...-..-', '&': '. . . .', '@': '.--.-.',
    '{': '----.--', '}': '-----.-'
}


def encode(s):
    return ' '.join([str(MORSE_TABLE[i.upper()]) if i.upper() in MORSE_TABLE.keys() else '???' for i in s])


def decode(s):
    msg = ''
    try:
        msg = ''.join([dict(map(lambda t: (t[1], t[0]), MORSE_TABLE.items()))[
                      c] for c in s.split(' ')])
    except:
        UNCODE = dict(map(lambda t: (t[1], t[0]), MORSE_TABLE.items()))
        for code in s.split('/'):
            if code == '':
                msg += ' '
            elif code in UNCODE.keys():
                msg += UNCODE[code]
    return msg

if __name__ == '__main__':
    print decode('--./-.-/-.-./-/..-./----.--/-../../-../../-../../-../../-../../-./-/./.-././.../../-./--./-----.-')
