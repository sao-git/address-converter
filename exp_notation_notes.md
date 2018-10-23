A real number `x` may be represented in exponential notation by the equation:

    x = m * b^n

The base `b` can be any positive real number but is usually restricted to 2, 8, 16--or most commonly 10, known as *scientific notation*. Other bases of note are 12 and 60 (for historical purposes) and 64 (for *base64* binary-to-ASCII conversions).

The textbook way to convert a number to /normalized/ scientific notation is to count the number of places one must move the decimal point in order to leave a single digit in the integral part of `m`. The exponent `n` is that count; `n` is positive if the point moved right, negative if it moved left, zero if it didn't move. This operation is covered algorithmically by a separate function `normalize(x)`, using strings to replicate the exactness of human readable representation in base 10.

Here, however, we wish to make a more general mathematical conversion, without normalization. This is particularly useful for *engineering notation* for which the base is 1000 (10^3), lining the representation up with the majority of SI prefixes. How then do we find `m` and `n` in the general case?

Note: Since the equation involves exponentiation, its solution will involve a logarithm. Real logarithms cannot have a negative argument, so we use `|x|`, the absolute value of `x`, for the solution.

The first step makes a substitution to take advantage of an important property of both exponentiation and logarithms:

    (1) m = b^t -> |x| = |b^t * b^n| = |b^(t + n)|
    (2) log_b(|x|) = t + n

Note that `t + n` itself does not have to be positive, only `|b^(t + n)|`. This fact allows us to easily deal with negative values for both `t` and `n`.

What are `t` and `n`? Recall that any real number can be separated into an integral part and a fractional part, i.e. the number "to the left of" the decimal point added "what's left":

    (Ex.) -2018.1234 = -2018 + 0.1234

For a logarithm, the integral part always represents `n`, the integer exponent that shifts the decimal point to the correct place. This can be computed using the trunc() function:

    (Def.) trunc(x) := {floor(x) if x >= 0, ceiling(x) if x < 0}

    (3) n = trunc(log_b(|x|))

We then determine `t` by simple algebra:

    (4) t = log_b(|x|) - n

Note that this simplifies the calculation of `m`, as:

    (5) m = b^t = b^(log_b(|x|) - n) = x / b^n

In a more rigorous context, the |x| must be kept because it was inside the logarithm and x is not assumed to be positive. The solution is to multiply `sign(x)` (1 for positive or zero, -1 for negative) with |x|, which is just equal to x.

Also note:

    (6) x = x / b^n * b^n

is algebraically correct. Therefore, our solution is:

    (7) m = x / b^n,  n = trunc(log_b(|x|))

