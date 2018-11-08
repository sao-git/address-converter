#!/usr/bin/env python3
import exp_notation
import math
import re
import sys

f = float(input("Number pls: "))
d = int(input("Display base pls: "))

if d not in exp_notation.valid_radices:
    raise exp_notation.RadixError

f_hex = f.hex()
print(f_hex)
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
print("sign + mantissa = {}{}.{}\n".format(sign_f, whole, fraction))

print("p = " + str(p))
bits = exp_notation.radix_bits[d]
print("bits = " + str(bits))

# Determine builtin function for final conversion
conv = exp_notation.radix_conv(d)

# Helper generator for readibility. Convert each hex digit in `fraction` to a sequence of integers…
f_frac = (int(x, 16) for x in iter(fraction))
# …and combine the sequence into an MSB-first bitstring, four bits per, removing trailing zeroes
fraction = re.sub('0*$', '', ''.join(bin(x)[2:].zfill(4) for x in f_frac))

normalize = True

if normalize == True:
    working_set = whole + fraction
    print("working_set = " + str(working_set))
    s = working_set.find('1')
    print("s = " + str(s))
    whole_new, fraction_new = working_set[s:s+bits], working_set[s+bits:]
    n_new = p - s - bits + 1
    n_new, denom = (n_new // bits, 1) if n_new % bits == 0 else (n_new, bits)
    print("n_new = " + str(n_new))

    n_conv = '-' + conv(abs(n_new)), str(denom)
    print("normalized n = {}/{}".format(*n_conv))
    n = n_new/denom
    print(n)
else:
    s = abs(p) % bits
    n = int(p / bits)
    print("s = " + str(s))
    print("n = " + str(n))
    n_conv = conv(abs(n)), '1'
    if n < 0:
        working_set = whole.zfill(s+1) + fraction
        whole_new, fraction_new = working_set[0], working_set[1:]
    else:
        working_set = whole + fraction
        whole_new, fraction_new = working_set[:s+1], working_set[s+1:]

print("whole_new, fraction_new = {}, {}".format(whole_new, fraction_new))

# Showing that sign + whole_new + fraction_new is equal (within float rounding error) to input `f`
f_frac_gen = (int(x)/2**i for i,x in enumerate(fraction_new,1))
f_new = exp_notation.sign(f) * (int(whole_new, 2) + sum(f_frac_gen)) * d**n
print("\nf = " + str(f))
print("f_new = " + str(f_new))
print("Percent difference = {:%}\n" .format(f_new / f - 1))

# If `display_base` is 2, nothing further is needed.
if d == 2:
    final = sign_f + whole_new + '.' + fraction_new
    print((final, n_conv, conv(d)))
    sys.exit(0)

if int(fraction_new) == 0:
    # A '0' in a 1-tuple is sufficient when there is zero fractional part
    frac_groups = '0',
else:
    # Pad `fraction` with trailing zeroes if the length of `fraction` is not divisible by `bits`
    frac_length = len(fraction_new) % bits
    if frac_length != 0:
        fraction_new += ''.zfill(bits - frac_length)
    # Helpers for frac_groups
    #
    # The expression inside the zip creates a tuple of length `bits` where each element is a reference
    # to `frac_iter`, with the star operator allowing zip to use `frac_iter` to create the groups
    frac_iter = iter(fraction_new)
    frac_group_zip = zip(*( (frac_iter,)*bits ))
    # Get the groups of `fraction_new` of `bits` length as big endian binary strings
    frac_groups = [''.join(t) for t in frac_group_zip]
    ## Strip any trailing zero groups
    #while int(frac_groups[-1]) == 0:
    #    frac_groups.pop()
    print(frac_groups)


# Final converstion for `fraction`, giving a string of characters in the display base
fraction_final = ''.join(conv(int(g,2)) for g in frac_groups)
# Finally, assemble the whole signed mantissa...
final = sign_f + conv(int(whole_new,2)) + '.' + fraction_final
# ...and return the mantissa, exponent (with denominator, even if denom is 1), and display base
print((final, n_conv, conv(d)))
