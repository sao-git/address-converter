#!/usr/bin/env python

"""
ip token list/get returns a token in dot-decimal form.
This script will convert a standard hex token to dot-decimal
for comparison to the ip output.

TODO:
Replace input() with argparse
Add conversion from dot-decimal to colon-hex
Add exception handling for bad input strings
"""


def recombine(t):
    s = ''
    for a in t:
        s += a
    return s


def split_by_eights(s):
    r = iter(s)
    return (a+b for a,b in zip(r,r))
    

def hex_to_int(t):
    return (int(b, 16) for b in t)


def int_to_dd(t):
    return '.'.join((str(x) for x in t))


if __name__ == "__main__":
    token = input("Hex token, e.g. dead:beef : ")
    token_p = (a.zfill(4) for a in token.split(':'))
    token_s = recombine(token_p)
    token_r = split_by_eights(token_s)
    token_d = hex_to_int(token_r)
    print(int_to_dd(token_d))
