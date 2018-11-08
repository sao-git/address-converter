#!/usr/bin/env python3
import math
import re

# TODO:
#       Add a lookup table of SI prefixes, and convert from base 10
#       to 1000 for engineering notation.

# Valid values for display_base other than 10
valid_radices = (2, 8, 16)
# Functions for converting an integer to a string in a new base, in order of above
int_convs = (bin, oct, hex)

# Lookup table maps display_base as a key to conversion function as a value
radix_conv_funcs = dict(zip(valid_radices, int_convs))
# Lookup table maps int as a key to int(log(int, 2)) as a value
# Valid for powers of 2 from 0 to 1024
radix_bits = dict((2**n, n) for n in range(0, 11))

def _radix_conv(n, radix):
    conv = radix_conv_funcs[radix]
    if n == 0:
        return '0'
    else:
        return '-' + conv(abs(n))[2:] if n < 0 else conv(n)[2:]


def radix_conv(radix):
    return lambda x: _radix_conv(x, radix)


class RadixError(Exception):
    """Standard error message for a display_base not in valid_radices."""
    def __init__(self):
        radix_error = tuple(str(i) for i in sorted(valid_radices + (10,)))
        radix_error = ", ".join(radix_error[:-1]) + ", or " + radix_error[-1]
        radix_error = "Display base must be " + radix_error + "."
        super(RadixError, self).__init__(radix_error)


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
    Returns -1 or 1 based on the numeric sign of x.
    Any number equivalent to False, including -0.0, will return itself.
    """

    # From https://www.quora.com/How-do-I-get-sign-of-integer-in-Python
    return x and (1, -1)[x < 0]


def sign_str(x):
    return '-' if x < 0 else ''


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
        # occurs naturally for |x| >= 1.
        try:
        # If x is ±inf or NaN return x, x, base
            int(x)
        except (OverflowError, ValueError):
            return x, x, base

        x_log = math.log(abs(x), base)
        # int() always truncates towards zero, so negative exponents are covered.
        n = int(x_log)
        t = x_log - n

    if normalize and t < 0:
        # If 0 <= t < 1, do nothing. If t >= 0, it will be < 1 by definition.
        # If t < 0, subtract 1 from n, which implicitly adds 1 to t and guarantees
        # it to be between 0 and 1. This has the effect of multiplying the original m by b.
        n -= 1

    if n == 0:
        # If 0 < |x| < base, n is zero, so m is just x.
        m = x
    else:
        # Conditional added here to mitigate rounding errors observed during testing.
        m = x / pow(base, n) if n >= 1 else x * pow(base, -n)

    return m, n, base


def hex_manip(f, display_base = 16, normalize = True):
    """
    Converts a float `f` to a tuple of strings `m, (n, d), display_base`, where:

        `m` is the mantissa, normalized or not, in digits of `display_base`
        `n` is the numerator of the exponent on `display_base` that converts `m` back to `f`
        `d` is the denominator of the exponent, including 1
        `display_base` is in `valid_radices`

    If `normalize` == True and `display_base` != 2, there is a chance the exponent will not be an
    integer. In this case, the denominator `d` is equal to the base 2 logarithm of `display_base`.
    """

    if display_base not in valid_radices:
        raise RadixError

    # Get the hex literal for `f`, described at:
    # https://docs.python.org/3/library/stdtypes.html#float.hex
    # https://docs.oracle.com/javase/7/docs/api/java/lang/Double.html#toHexString(double)
    f_hex = f.hex()
    # Capture a negative sign if present
    sign_f = '-' if f_hex[0] != '0' else ''
    # Determine how many places to skip the sign character and '0x'
    skip = 3 if f < 0 else 2
    # `mantissa` is the absolute value, `p` is to base 2
    mantissa, p = f_hex[skip:].split('p')
    p = int(p)
    # `whole` is 1 for normal floats, 0 for subnormal or zero
    # `fraction` is in hex; each digit will be converted to int if display_base != 16
    whole, fraction = mantissa.split('.')

    bits = radix_bit_conv[display_base]
    n = int(p / bits)
    s = abs(p) % bits

    # Determine builtin function for conversion
    int_conv_func = lambda x: int_conv_funcs[display_base](x)[2:]

    # Helper generator for readability
    f_frac = (int(x, 16) for x in iter(fraction))
    # Convert hex digits in the fraction to a big endian binary string
    fraction = "".join(bin(x)[2:].zfill(4) for x in f_frac)

    if n < 0:
        if normalize == True:
            working_set = whole + fraction
            whole_new, fraction_new = working_set[:s+1], working_set[s+1:]
            n = (p+bits-1)/bits
            n_conv = '-' + int_conv_func(abs(int(n*bits - s+1))), str(bits)
        else:
            working_set = whole.zfill(s+1) + fraction
            whole_new, fraction_new = working_set[0], working_set[1:]
            n_conv = n, '1'
    else:
        working_set = whole + fraction
        whole_new, fraction_new = working_set[:s+1], working_set[s+1:]
        n_conv = n, '1'

    print(fraction_new)

    if int(fraction_new) == 0:
        # A '0' in a 1-tuple is sufficient if there is no new fractional part
        frac_groups = '0',
    else:
        # Pad `fraction` with trailing zeroes if the length of `fraction` is not divisible by `bits`
        frac_length = len(fraction_new) % bits
        if frac_length != 0:
            fraction_new += ''.zfill(bits - frac_length)

        # Helpers for frac_groups
        #
        # The expression inside `zip` creates a tuple of length `bits` where each element is a reference
        # to `frac_iter`, with the star operator allowing `zip` to use `frac_iter` to create the groups
        frac_iter = iter(fraction_new)
        frac_group_zip = zip(*( (frac_iter,)*bits ))
        # Get the groups of `fraction_new` of `bits` length as big endian binary strings
        frac_groups = [''.join(t) for t in frac_group_zip]
        # Strip trailing zero groups
        while int(frac_groups[-1]) == 0:
            frac_groups.pop()

    # Final converstion for `fraction`, giving a string of characters in the display base
    fraction_final = ''.join(int_conv_func(int(g,2)) for g in frac_groups)
    # Finally, assemble the whole signed mantissa…
    final = sign_f + int_conv_func(int(whole_new,2)) + '.' + fraction_final
    # …and return the mantissa, exponent (with denominator), and display base
    return final, n_conv, str(display_base)


def radix_base(t, display_base = 16, raw_hex = False):
    """
    Make a new exp_tuple with each element as a string of radix representation, e.g.
    if display_base is 16, convert m to a hex string. This is limited in scope to the
    "common" bases, i.e. 2, 8, 10, 16.
    """

    if raw_hex == True:
        return tuple(float(_t).hex() for _t in t)
    if display_base == 10:
        return tuple(str(f) for f in t)
    else:
        m_t, n_t, b_t = t

    int_conv_func = int_conv_funcs[display_base]
    n = int_conv_func(n_t)

    if type(b_t) == int:
        b = int_conv_func(b_t)
    else:
        None



    #f.hex(), float.fromhex()


    return m, n, b


#if __name__ == "__main__":
#    print(exp_tuple(float("-inf"), 10))

if __name__ == "__main__":
    f = float(input("Number pls: "))
    d = float(input("Number pls: "))
    print(hex_manip(f, d, True))

if __name__ == "__main_":
    a = float(input("Number pls: "))
    print(normalize(a))

if __name__ == "__main_":
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


