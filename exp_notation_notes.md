A real number `x` may be represented in exponential notation by the equation:

    x = m * b^n

The base `b` can be any positive real number but is usually restricted to 2, 8, 16, or most often 10, the last commonly known as **scientific notation**. Other bases of note are 12 and 60 (for historical purposes) and 64 (for *base64* binary-to-ASCII conversions).

The textbook way to convert a number to *normalized* scientific notation is to count the number of places one must move the decimal point in order to leave a single digit in the integral part of `m`. The exponent `n` is that count; `n` is positive if the point moved right, negative if it moved left, zero if it didn't move. This operation is covered algorithmically by a separate function `normalize(x)`, using strings to replicate the exactness of human readable representation in base 10 thereby eliminating floating point rounding errors.

Here, however, we wish to make a more general mathematical conversion, without normalization. This is particularly useful for **engineering notation** for which the base is 1000 (10^3), lining the representation up with the majority of SI prefixes. How then do we find `m` and `n` in the general case?

Note: Since the problem involves exponentiation, its solution will involve a logarithm. Real logarithms cannot have a negative argument, so we use `|x|`, the absolute value of `x`, for the solution.

The first step makes a substitution to take advantage of an important property of both exponentiation and logarithms:

    (1) m = b^t -> |x| = |b^t * b^n| = |b^(t + n)|
    (2) log_b(|x|) = t + n

Note that `t + n` itself does not have to be positive, only `|b^(t + n)|`. This fact allows us to easily deal with negative values for both `t` and `n`.

What are `t` and `n`? Recall that any real number can be separated into an integral part and a fractional part, i.e. the number “to the left of” the decimal point added “what’s left”:

    (Ex.) -2018.1234 = -2018 + 0.1234

For a logarithm, the integral part represents `n`, the integer exponent that shifts the decimal point according to the base `b`.

    (Ex.) b = 10 -> log_10(|-2018.1234|) ~= 3.30494771805 -> n = 3

    (Ex.) b = e -> ln(0.00065458) ~= -7.33151674937 -> n = -7

This can be computed using the truncate (`trunc()`) function:

    (Def.) trunc(x) := {floor(x) if x >= 0, ceiling(x) if x < 0}

    (3) n = trunc(log_b(|x|))

We then determine `t` by simple algebra:

    (4) t = log_b(|x|) - n

Note that this simplifies the calculation of `m`, as:

    (5) m = b^t = b^(log_b(|x|) - n) = x / b^n

In a more rigorous context, the `|x|` must be kept because it was inside the logarithm and `x` is not assumed to be positive. The solution is to multiply `sign(x)` (1 for positive or zero, -1 for negative) with `|x|`, which is just equal to `x`.

Also:

    (6) x = x / b^n * b^n

is algebraically correct. Therefore, our solution is:

    (7) m = x / b^n,  n = trunc(log_b(|x|))

It is important to note that this does not necessarily put `m` in normalized form.

An `x` with `1 <= |x| <= b` has an `n` that gives `0 < |m| <= 1`, which is normalized:

An `x` with `b < |x|` has an `n` that gives `1/b <= |m| <= 1`:

An `x` with `0 < |x| < 1` has an `n` that gives `1/b <= |m| <= 1`:


    b = 10 -> 1 / 10 = 0.1

    (Ex.) x = 0.001234 -> log_10(x) ~= -2.9086848403 -> n = -2, m = 0.1234
    (Ex.) x = -0.000008452 -> log_10(|x|) ~= -5.07304051162 -> n = -5, m = -0.8452
    (Ex.) x = 1 / b^2 = b^-2 = 0.01 -> log_10(x) ~= -2 -> n = -2, m = 1

    b = e -> 1 / e = 0.36787944117

    (Ex.) x = 0.001234 -> ln(x) ~= -6.6974943535 -> n = -6, m ~= 0.49783113117
    (Ex.) x = -0.000008452 -> ln(|x|) ~= -11.6811074582 -> n = -11, m = -0.50605624578
    (Ex.) x = -0.000008452 -> ln(|x|) ~= -11.6811074582 -> n = -11, m = -0.50605624578
    (Ex.) x = 1 / b^2 = b^-2 = 0.01 -> log_10(x) ~= -2 -> n = -2, m = 1

The special case to be handled is when `x = 0`. Logarithms of zero for all bases are undefined, since the limit of `log_b(x)` as `x -> 0` goes to `-∞`. This limit means that for smaller and smaller `|x|`, `n` grows in the negative direction without bound, with the line `x = 0` as an asymptote. For our purposes however, any value of `n` may be combined with `m = 0` to give an exponentional form of zero. In this case the simplest solution is:

    (Ex.) m = 0, n = 0

as `0 * b^0` will always equal zero since `b` is restricted to `0 < b`.
