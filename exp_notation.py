#!/usr/bin/env python3
from math import log

"""
"""

def split_float(x):
    """
    If x is a float in e notation, return the provided significand and exponent.
    If not, or if x is an integer, return the original number with an exponent of 0.
    """

    x_str = str(x)
    if x_str.count("e"):
        #print("Case: e notation")
        x_s = x_str.split("e")
        return float(x_s[0]), int(x_s[1])
    else:
        #print("Case: no e notation")
        return x, 0


def normalize(x):
    """
    Converts a number to “normalized” or “standard” form, i.e. where
    there is exactly one decimal digit before the decimal point. This is the
    expected default of scientific notation output.

    Returns a pair (x_n, shift) where x_n is the normalized number
    and shift is the base 10 exponent to return to the original x.

    """
    # Implementation detail:
    # Most cases use temporary strings, as this is more a problem of
    # human readable representation rather than the underlying number.
    # This choice makes the contents of the pair exact. However, reversing the
    # process and comparing to the original, e.g.
    #
    #    t = normalize(f)
    #    x_2 = t[0] * 10**[1]
    #    x_2 == x
    #
    # may fail due to the introduction of rounding errors in evaluating x_2.


    # Nothing further needed if the whole part is 1 through 9.
    x_abs = abs(x)
    if 1 <= x_abs < 10:
        #print("Case: [1,10)")
        return x, 0

    elif x_abs < 1:
        # Dealing exclusively with floats in this block.
        #print("Case: <1")

        # Check if x is in e notation. Since |x| < 1 is true, if
        # the output of split_float() has an exponent, nothing more is needed.
        x_split = split_float(x)
        if x_split[1] != 0:
            return x_split

        # Last case here is to split a temp string around the decimal point,
        # count the number of zeroes to the right, and shift the decimal point
        # to the right by that count plus one.
        else:
            post_dec = str(x).split('.')[1]
            shift = len(tuple(True for x in post_dec if x == '0')) + 1
            return x * 10**(shift), -1 * shift


    # Final case is for x > 10. Count the length of the whole part of |x|,
    # subtract one, and shift the decimal point to the left.
    else:
        #print("Case: >=10")
        try:
            shift = len(str(int(x_abs))) - 1
        # If x is ±inf return x, x
        except OverflowError:
            return x, x
        return x / 10**(shift), shift


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
    a = float(input("Number pls: "))
    print(normalize(a))

if __name__ == "__mai__":
    x = float(input("Number pls: "))
    b = int(input("Base pls: "))
    t = exp_tuple(x, b)
    print(t)
