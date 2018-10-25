#!/usr/bin/env python3
import math
import re

"""
TODO:
    Add a lookup table of SI prefixes, and convert from base 10 to 1000 for engineering notation.
"""

def sign(x):
    """
    Taken from https://www.quora.com/How-do-I-get-sign-of-integer-in-Python
    """
    return x and (1, -1)[x < 0]

def split_float(x):
    """
    If x is a float in e notation, return the provided significand and exponent.
    If not, or if x is an integer, return the original number with an exponent of 0.
    """

    x_str = str(x)

    if x_str.count("e"):
        x_s = x_str.split("e")
        return float(x_s[0]), int(x_s[1])
    else:
        return x, 0


def normalize(x):
    """
    Converts a number to “normalized” or “standard” form, i.e. where
    there is exactly one decimal digit before the decimal point. This is the
    expected default of scientific notation output.

    Returns a pair (x_n, shift) where x_n is the normalized number
    and shift is the base 10 exponent to return to the original x.

    If x is ±inf it will return (x, x) rather than throw an exception.
    """

    # Implementation detail:
    #
    # Most cases use temporary strings, as this is more a problem of
    # human readable representation rather than the underlying number.
    # This choice makes the contents of the pair exact.


    # Nothing further needed if the whole part of |x| is in [1, 10).
    # Zero added to this case because it returned an exponent of -2
    # when caught by the |x| < 1 case.
    x_abs = abs(x)
    if 1 <= x_abs < 10 or x == 0:
        return x, 0

    elif x_abs < 1:
        # Dealing exclusively with floats in this case.

        # Check if x is in e notation. Since |x| < 1 is true, if the
        # output of split_float() has an exponent, nothing more is needed.
        x_split = split_float(x)
        if x_split[1] != 0:
            return x_split


        # Last case here is to make a temp string after the decimal point,
        # count the number of zeroes until the first non-zero, and shift the decimal point
        # to the right by that count plus one.
        else:
            post_dec = str(x_abs)[2:]
            shift = re.search("0*", post_dec).end() + 1
            return sign(x) * float(post_dec[shift - 1] + "." + post_dec[shift:]), -1 * shift


    # Final case is for x > 10. Count the length of the whole part of |x|,
    # subtract one, and shift the decimal point to the left.
    # TODO:
    #       Check for split_float and adjust accordingly.
    #       Rewrite to use temp string construction for exactness.
    else:
        print("Case: x > 10")
        try:
            shift = len(str(int(x_abs))) - 1
        # If x is ±inf return x, x
        except OverflowError:
            return x, x
        #post_dec = str(x_abs).split('.')[1]
        return x / 10**(shift), shift
        #return sign(x) * float(post_dec[shift - 1] + "." + post_dec[shift:]), -1 * shift


def exp_tuple(x, base = 10, normalize = False):
    """
    For a number x and base b, return (m, b, n) where m = x / b^n, n = int(log_b(|x|))

    """
    # (0, 0) will be the output for x = 0
    if x == 0:
        return 0, base, 0

    # We only need the integral part of the logarithm.
    # int() always truncates towards zero, so negative exponents are covered.
    else:
        n = int(math.log(abs(x), base))
        if n == 0:
            return x, base, 0
        # Conditional added here to mitigate rounding errors from exponentiation
        # observed during testing.
        elif n >= 1:
            return x / pow(base, n), base, n
        else:
            # Case n < 1
            return x * pow(base, -1 * n), base, n


def radix_base(t, base):
    """
    Convert exp_tuple to strings of `base` representation.
    """
    return

if __name__ == "__main_":
    a = float(input("Number pls: "))
    print(normalize(a))

if __name__ == "__main__":
    x = float(input("Number pls: "))
    b_str = input("Base pls: ")
    if b_str == "e":
        b = math.e
    elif b_str == "pi":
        b = math.pi
    else:
        b = int(b_str)
    t = exp_tuple(x, b)
    print(t)
