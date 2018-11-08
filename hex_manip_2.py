#!/usr/bin/env python3
import exp_notation
import math

f = float(input("Number pls: "))
d = int(input("Display base pls: "))

if d not in exp_notation.valid_radices:
    raise exp_notation.RadixError

f_hex = f.hex()
print(f_hex)
# Capture a negative sign if present
sign_f = f_hex[0] if f_hex[0] != '0' else ''
# Determine how many places to skip the sign character and '0x'
skip = 3 if f < 0 else 2
# Mantissa is the absolute value, p is to base 2
mantissa, p = f_hex[skip:].split('p')
p = int(p)
# Whole part is 1 for normal floats, 0 for subnormal
# Fraction part is in hex; each digit will be converted to int if display_base != 16
whole, fraction = mantissa.split('.')
print("sign + mantissa = {}{}.{}\n".format(sign_f, whole, fraction))

print("p = " + str(p))
bits = exp_notation.radix_bit_conv[d]
n = int(p / bits)
print("n = " + str(n))
s = abs(p) % bits
print("s = " + str(s))

# Determine builtin function for conversion
int_conv_func = lambda x: exp_notation.int_conv_funcs[d](x)[2:]

# Helper generator for readibility
f_frac = (int(x, 16) for x in iter(fraction))
# Convert hex digits in the fraction to a big endian binary string
fraction = "".join(bin(x)[2:].zfill(4) for x in f_frac)

normalize = True
if n < 0:
    if normalize == True:
        working_set = whole + fraction
        whole_new, fraction_new = working_set[:s+1], working_set[s+1:]
        n -= (s+1)/bits
        n_conv = '-' + int_conv_func(abs(int(n*bits - s+1))), str(bits)
        print("normalized n = {}/{}".format(*n_conv))
        print(n)
    else:
        working_set = whole.zfill(s+1) + fraction
        whole_new, fraction_new = working_set[0], working_set[1:]
        n_conv = n, '1'
else:
    working_set = whole + fraction
    whole_new, fraction_new = working_set[:s+1], working_set[s+1:]
    n_conv = n, '1'

print("whole_new, fraction_new = {}, {}".format(whole_new, fraction_new))

# Showing that sign + whole_new + fraction_new is equal (within float rounding error) to input `f`
f_frac_gen = (int(x)/2**i for i,x in enumerate(fraction_new,1))
f_new = exp_notation.sign(f) * (int(whole_new, 2) + sum(f_frac_gen)) * d**n
print(f)
print(f_new)
print()

frac_length = len(fraction_new) % bits
if frac_length != 0:
    fraction_new += ''.zfill(bits - frac_length)

# Helpers for frac_groups
frac_iter = iter(fraction_new)
frac_group_zip = zip(*((frac_iter,)*bits))
# Get the groups of `fraction_new` of `bits` length
frac_groups = tuple(''.join(t) for t in frac_group_zip)
print(frac_groups)
# Strip any trailing zero
if int(frac_groups[-1]) == 0:
    frac_groups = frac_groups[:-1]

fraction_final = ''.join(int_conv_func(int(g,2)) for g in frac_groups)
final = sign_f + int_conv_func(int(whole_new,2)) + '.' + fraction_final
print((final, n_conv, str(d)))
