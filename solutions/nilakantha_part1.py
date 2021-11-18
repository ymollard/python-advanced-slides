#!/usr/bin/env python3
"""
This is a naive implementation of estimation of Pi with Nilakantha fractions 
"""
N = 90000    # Number of iterations

denominators = [(n, n+1, n+2) for n in range(2, 2*N+1, 2)]
nilakantha_list = list(map(lambda x: 4/(x[0] * x[1] * x[2]), denominators))
nilakantha_sum = 0

sign = True
for i in range(N):
    nilakantha_sum += nilakantha_list[i] * (1 if sign else -1)
    print(nilakantha_sum)
    sign = not sign

# Set the precision display to 50 digits and print the estimate of π
nilakantha_sum_str = "{:.50f}".format(nilakantha_sum)
print("Estimation of π =", nilakantha_sum_str)

# Compare the obtained precision with a reference
reference = "0.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
for digit_i, char in enumerate(reference):
    if char != nilakantha_sum_str[digit_i] or digit_i == min(50, len(nilakantha_sum_str)):
        break
print("This is a precision of {} digits".format(digit_i-2))
