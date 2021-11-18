#!/usr/bin/env python3
"""
This is an improved version optimized with a generator and using mathematically-correct decimals 
"""
from decimal import Decimal, getcontext

N = 100000000    # Number of iterations

def _nilakantha_generator(N: int):
    """
    Generator of N nilakantha fractions
    """
    for n in range(2, 2*N+1, 2):
        yield Decimal(4) / Decimal(n * (n+1) * (n+2))

nilakantha_sum = Decimal(0)
sign = True
for fraction in _nilakantha_generator(N):
    nilakantha_sum += fraction * (1 if sign else -1)
    sign = not sign

# Set the precision display to 50 digits and print the estimate of π
getcontext().prec = 50
nilakantha_sum_str = str(nilakantha_sum)
print("Estimation of π =", nilakantha_sum_str)

# Compare the obtained precision with a reference
reference = "0.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
for digit_i, char in enumerate(reference):
    if char != nilakantha_sum_str[digit_i] or digit_i == min(50, len(nilakantha_sum_str)):
        break
print("This is a precision of {} digits".format(digit_i-2))

