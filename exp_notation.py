#!/usr/bin/env python3
from math import log

def sign(x):
    # https://www.quora.com/How-do-I-get-sign-of-integer-in-Python
    return x and (1, -1)[x < 0]

def exp_tuple(x, base = 10):
    s, x = sign(x), abs(x)
    a = int(log(x) / log(base))
    return s * x / base**a, base, a


if __name__ == "__main__":
    x = float(input("Number pls: "))
    b = int(input("Base pls: "))
    t = exp_tuple(x, b)
    print(t)
