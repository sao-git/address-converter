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
        x_s, x_p = x_str.split("e")
        return float(x_s), int(x_p)
    else:
        return x, 0


def normalize(x, base = 10):
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
    # This is the algorithm for perfect normalization which relies on
    # string conversion to eliminate rounding error, but is very slightly
    # slower than using normalize = True with exp_tuple() (~5.5 µs on a
    # Pentium N3700 @ 1.60GHz) and currently only works for base
    # and display_base of 10.


    # Nothing further needed if the whole part of |x| is in [1, 10).
    # Zero added to this case because it returned an exponent of -2
    # when caught by the |x| < 1 case.
    x_abs = abs(x)
    if 1 <= x_abs < 10 or x == 0:
        return x, 0, base

    elif x_abs < 1:
        # Dealing exclusively with floats in this case.

        # Check if x is in e notation. Since |x| < 1 is true, if the
        # output of split_float() has an exponent, nothing more is needed.
        x_m, x_n = split_float(x)
        if x_n != 0:
            return x_m, x_n, base


        # Last case here is to make a temp string after the decimal point,
        # count the number of zeroes until the first non-zero, and shift
        #the decimal point to the right by that count plus one.
        else:
            post_dec = str(x_abs)[2:]
            shift = re.search("0*", post_dec).end() + 1
            return sign(x) * float(post_dec[shift - 1] + "." + post_dec[shift:]), -1 * shift, base


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
            return x, x, base
        #post_dec = str(x_abs).split('.')[1]
        return x / 10**(shift), shift, base
        #return sign(x) * float(post_dec[shift - 1] + "." + post_dec[shift:]), -1 * shift


def exp_tuple(x, base = 10, normalize = False, display_base = 10):
    """
    For a number x and base b, return (m, n, b) where m = x / b^n, n = int(log_b(|x|))
    If normalize is True, the output will be tuned to ensure 1 <= |m| display_base

    """

    # (0, 0, base) will be the output for x = 0
    if x == 0:
        return 0, 0, base
    else:
        x_log = math.log(abs(x), base)
        # int() always truncates towards zero, so negative exponents are covered.
        n = int(x_log)

    # Conditional added here to mitigate rounding errors from exponentiation
    # observed during testing.
    m_calc = lambda x,n: x / pow(base, n) if n >= 1 else x * pow(base, -1 * n) 

    if normalize == False:
        if n == 0:
            return x, 0, base
        else:
            return m_calc(x,n), n, base
    else:
        t = x_log - n
        log_b_B = math.log(display_base, base)

    if 0 <= t < log_b_B:
        return m_calc(x,n), n, base
    else:
        n = math.ceil(x_log - log_b_B)
        return m_calc(x,n), n, base


def radix_base(t):
    """
    Make a new exp_tuple with m as a string of `base` representation, e.g.
    if the base is 16, convert m to a hex string. This only works for conversions provided
    by Python.
    """
    m, n, b = t

    #float.hex(), float.fromhex()
    
    m_i = int(m)
    m_f = str(abs(m))[2:]
    r = r"(0[xbo])"
    m_i_r = re.search(r, m_i)
    m_f_r = re.search(r, m_f)

    return

if __name__ == "__main_":
    a = float(input("Number pls: "))
    print(normalize(a))

if __name__ == "__main__":
    x = float(input("Number pls: "))
    b_str = input("Base pls: ")
    d = int(input("Display base pls: "))
    if b_str == "e":
        b = math.e
    elif b_str == "pi":
        b = math.pi
    else:
        b = int(b_str)
    print("\nUsing input: x = {}, b = {}, B = {}".format(x, b, d))
    t = exp_tuple(x, b, normalize = True, display_base = d)
    print("\nexp_tuple(x, base = {}, normalize = True, display_base = {:d}):\n        {}".format(b, d, t))
    x_normal = normalize(x)
    print("normalize(x): \n        " + str(x_normal))
    x_recons = t[0] * t[2]**t[1]
    print("\nReconstructed from exp_tuple: " + str(x_recons))
    x_recons_n = x_normal[0] * 10**x_normal[1]
    print("Reconstructed from normalize: " + str(x_recons_n))
    print("Equal?: " + str(x_recons == x_recons_n))
    x_comp = abs(x_recons - x_recons_n)
    tolerance = 1e-20
    print("Within {:.0e} of each other?: {}".format(tolerance, x_comp < tolerance))
