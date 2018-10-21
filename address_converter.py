#!/usr/bin/env python3

"""
ip token list/get returns a token in dot-decimal form.
This script will convert a standard hex token to dot-decimal
for comparison to the ip output.

TODO:
Replace input() with argparse
Add conversion from dot-decimal to colon-hex
Add exception handling for bad input strings
"""

def split_and_fill(s, fill = 4, delim = ':'):
    return (a.zfill(fill) for a in s.split(delim))


def split_in_pairs(s, padding = "0"):
    """
    Takes a string and splits into an iterable of strings of two characters each.

    Made to break up a hex string into octets, so default is to pad an odd length
    string with a 0 in front. An alternative character may be specified as the
    second argument.
    """
    if not isinstance(padding, str) or len(padding) != 1:
        raise TypeError("Padding must be a single character.")

    s = padding + s if len(s) % 2 else s
    v = iter(s)
    return (a+b for a,b in zip(v,v))


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
    token_p = split_and_fill(token)
    token_s = "".join(token_p)
    #print(token_s)
    token_r = split_in_pairs(token_s)
    token_d = hex_to_int(token_r)
    try:
        print(int_to_dd(token_d))
    except ValueError:
        raise ValueError("Ooops") from ValueError
