#!/usr/bin/env python3
import math
import re

# TODO:
#       Add a lookup table of SI prefixes, and convert from base 10
#       to 1000 for engineering notation.


class exponential:
    si_prefixes = {
            # SI powers of 10, or
            # 1000^(1/3)
            "0": ("", ""),
            "1": ("deca", "da"),
            "2": ("hecto", "h"),
            "3": ("kilo", "k"),
            "6": ("mega", "M"),
            "9": ("giga", "G"),
            "12": ("tera", "T"),
            "15": ("peta", "P"),
            "18": ("exa", "E"),
            "21": ("zetta", "Z"),
            "24": ("yotta", "Y"),
            "-1": ("deci", "d"),
            "-2": ("centi", "c"),
            "-3": ("milli", "m"),
            "-6": ("micro", "µ"),
            "-9": ("nano", "n"),
            "-12": ("pico", "p"),
            "-15": ("femto", "f"),
            "-18": ("atto", "a"),
            "-21": ("zepto", "z"),
            "-24": ("yocto", "y")
            }

    bi_prefixes = {
            # IEC powers of 1024, or
            # 2^10
            # 8^(10/3)
            # 16^(5/2)
            "0": ("", ""),
            "1": ("kibi", "Ki"),
            "2": ("mebi", "Mi"),
            "3": ("gibi", "Gi"),
            "4": ("tebi", "Ti"),
            "5": ("pebi", "Pi"),
            "6": ("exbi", "Ei"),
            "7": ("zebi", "Zi"),
            "8": ("yobi", "Yi")
            }

    def __init__(self):
        return


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

    Returns a pair (x_n, shift, base) where x_n is the normalized number
    and shift is the base 10 exponent to return to the original x.

    If x is ±inf it will return (x, x, base) rather than throw an exception.
    """

    # Implementation detail:
    #
    # This is the algorithm for perfect normalization which relies on
    # string conversion to eliminate rounding error, but is very, very slightly
    # slower than using normalize = True with exp_tuple() (~5.5 µs on a
    # Pentium N3700 @ 1.60GHz) and currently only works for base 10.

    x_abs = abs(x)

    # Nothing further needed if the whole part of |x| is in [1, 10).
    # Zero added to this case because it returned an exponent of -2
    # when caught by the |x| < 1 case.
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
        # If x is ±inf or NaN return x, x, base
        except (OverflowError, ValueError):
            return x, x, base
        #post_dec = str(x_abs).split('.')[1]
        return x / 10**(shift), shift, base
        #return sign(x) * float(post_dec[shift - 1] + "." + post_dec[shift:]), -1 * shift


def exp_tuple(x, base = 10, normalize = False):
    """
    For a number x and base b, return (m, n, b) where m = x / b^n, n = int(log_b(|x|)).
    If normalize is True, the output will be tuned to ensure 1 <= |m| < b.

    (0, 0, base) will be the output for x = 0, since 0 * base^0 = 0 * 1 = 0.

    If x is ±inf or NaN it will return (x, x, base) rather than raise an exception.
    However, if b <= 1, a ValueError will be raised.
    """

    if base <= 1:
        raise ValueError("Base must be greater than 1.")
    elif x == 0:
        return 0, 0, base
    else:
        # log_b |x| is equal to n + t, where n is the integer part and t the fractional part.
        # |x| is then equal to b^(n+t) which is also b^t*b^n, known as the exponentional
        # form of |x|. Let b^t be called |m|, which is also |x|/b^n. Then x = x/b^n * b^n.
        #
        # This form is called "normalized" if 1 <= |m| < b, which means 0 <= t < 1, and
        # occurs naturally for |x| >= 1. When 0 < |x| < b, 1 must be subtracted from the
        # exponent n to make m fit this condition.
        try:
            int(x)
        # If x is ±inf or NaN return x, x, base
        except (OverflowError, ValueError):
            return x, x, base

        x_log = math.log(abs(x), base)
        # int() always truncates towards zero, so negative exponents are covered.
        n = int(x_log)
        t = x_log - n

    # Conditional added here to mitigate rounding errors from exponentiation
    # observed during testing.
    m_calc = lambda x,n: x / pow(base, n) if n >= 1 else x * pow(base, -1 * n)

    if normalize and t < 0:
        # If 0 <= t < 1, do nothing. If t >= 0, it will be < 1 by definition.
        # If t < 0, subtract 1 from n, which implicitly adds 1 to t and guarantees
        # it to be between 0 and 1. Subtracting 1 from n multiples m by b.
        n -= 1

    if n == 0:
        # If 0 < |x| < base, n is zero, so m is just x.
        m = x
    else:
        m = m_calc(x, n)

    return m, n, base


def radix_base(t):
    """
    Make a new exp_tuple with each element as a string of base representation, e.g.
    if the base is 16, convert m to a hex string. This is limited in scope to the "common"
    bases, i.e. 2, 8, 10, 16, and 64.
    """
    m, n, b = t

    #float.hex(), float.fromhex()

    m_i = int(m)
    m_f = str(abs(m))[2:]
    r = r"(0[xbo])"
    m_i_r = re.search(r, m_i)
    m_f_r = re.search(r, m_f)

    return

#if __name__ == "__main__":
#    print(exp_tuple(float("-inf"), 10))

if __name__ == "__main_":
    a = float(input("Number pls: "))
    print(normalize(a))

if __name__ == "__main__":
    x = float(input("Number pls: "))
    b_str = input("Base pls: ")
    #d = int(input("Display base pls: "))
    if b_str == "e":
        b = math.e
    elif b_str == "pi":
        b = math.pi
    else:
        b = int(b_str)
    print("\nUsing input: x = {}, b = {}".format(x, b))

    t = exp_tuple(x, b, normalize = True)
    print("\nexp_tuple(x, base = {}, normalize = True):\n        {}".format(b, t))
    x_normal = normalize(x)
    print("normalize(x): \n        " + str(x_normal))
    x_recons = t[0] * t[2]**t[1]

    print("\nReconstructed from exp_tuple: " + str(x_recons))
    x_recons_n = x_normal[0] * 10**x_normal[1]
    print("Reconstructed from normalize: " + str(x_recons_n))
    print("Equal?: " + str(x_recons == x_recons_n))
    x_comp = abs(x_recons - x_recons_n)
    tolerance = 1e-7
    print("Within {:.0e} of each other?: {}".format(tolerance, x_comp < tolerance))


#    print("\n\n")
#    print(si_prefix.si_prefixes)
#    print(si_prefix.bi_prefixes)
