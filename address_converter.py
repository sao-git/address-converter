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


def cat(t):
    """
    Concatenates an iterable of strings into a single string.
    """
    return ''.join(t)


def split_by_eights(s):
    """
    Takes a string of even length and splits into strings of two characters each.
    Made to break up a hex string into octets.
    """
    r = iter(s)
    return (a+b for a,b in zip(r,r))
    

def hex_to_int(t):
    """
    Takes an iterable of hex strings and returns an iterable of integers.
    The hex strings may be of any length except 0.

    TODO:
        Output None where empty strings occur.
    """
    return (int(b, 16) for b in t)


def int_to_dd(t):
    """
    Takes an iterable of integers and returns a dot-decimal string.
    """
    return '.'.join((str(x) for x in t))


if __name__ == "__main__":
    token = input("Hex token, e.g. dead:beef : ")
    token_p = (a.zfill(4) for a in token.split(':'))
    token_s = cat(token_p)
    token_r = split_by_eights(token_s)
    token_d = hex_to_int(token_r)
    print(int_to_dd(token_d))
