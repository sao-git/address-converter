#!/usr/bin/env python3
from math import log

"""
TODO:
    Define an exp_tuple type as output of said function with named indices?
"""

def _normalize(x):
    return

def exp_tuple(x, base = 10, normalize = True):
    # Real logarithms can't have negative arguments.
    xa = abs(x)
    # We only need the integer part of the logarithm.
    # int() always truncates towards zero, so negative exponents are covered.
    a = int(log(xa) / log(base))
    return x / base**a, base, a

def radix_base(t, base):
    """
    Convert exp_tuple to strings of `base` representation.
    """
    return

if __name__ == "__main__":
    x = float(input("Number pls: "))
    b = int(input("Base pls: "))
    t = exp_tuple(x, b)
    print(t)
