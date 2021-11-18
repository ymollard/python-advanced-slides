#!/usr/bin/env python3
"""
This is an improved version optimized with multiprocessing 
"""
from decimal import Decimal, getcontext
from multiprocessing import Process, Queue

# Set the precision display to 60 digits and print the estimate of π
getcontext().prec = 60

def get_partial_nilakantha(start_n: int, count: int, queue: Queue) -> float:
    """
    Computes a portion of the Nilakantha fractions:
    pi = 3 + fraction #1 + fraction #2 + ... + fraction #N

    :param start_n: Index of the first Nilakantha fraction (must be odd)
    :param count: Number of total fractions to be generated (must be odd)
    :param queue: the queue to store the result in
    :return: the sum of the Nilakantha fractions between #start_n and #final_n

    ..warning: count and start id must be odd so that all partial sums are coherentlm
    """
    def _nilakantha_generator(start_n: int, count: int):
        for n in range(start_n, start_n+2*count, 2):
            yield Decimal(4) / Decimal(n * (n+1) * (n+2))
    
    nilakantha_sum = Decimal(0)

    sign = True
    for fraction in _nilakantha_generator(start_n, count):
        nilakantha_sum += fraction * (1 if sign else -1)
        sign = not sign
    
    queue.put(nilakantha_sum)


queue = Queue()   # Stores partial  Nilakantha sums from all processes
count = 10000000
process_id = 0
num_processes = 6
processes = []

for process_id in range(num_processes):
    processes.append(Process(target=get_partial_nilakantha, args=(2*process_id*count+2, count, queue)))
    processes[-1].start()

for process in processes:
    process.join()

# Retrieve partial sums and print the estimate of π
partial_sums = [queue.get() for _ in range(num_processes)]
print("Partial sums:", partial_sums)
nilakantha_sum_str = str(sum(partial_sums))
print("Estimation of π =", nilakantha_sum_str)

# Compare the obtained precision with a reference
reference = "0.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
for digit_i, char in enumerate(reference):
    if char != nilakantha_sum_str[digit_i] or digit_i == min(50, len(nilakantha_sum_str)):
        break
print("This is a precision of {} digits".format(digit_i-2))

