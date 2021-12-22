#!/usr/bin/env python
"""
Break a md5 digest of a password made of upper and lower case characters (aka reverse-MD5) using Brute force.
Optimized version of the original naive_code_breaker.py

:warning It assumes only alphabetical characters, not digits!

:Example

./code_breaker.py --digest=d0eedb799584d850fdd802fd3c27ae34 --password-length=3 (must take <100ms on 1 CPU)
./code_breaker.py --digest=9fcce10c03dc2eaada4c361c508c4ebe --password-length=4 (must take <10s on 1 CPU)
./code_breaker.py --digest=8b1a9953c4611296a827abf8c47804d7 --password-length=5 (must take <1000s on 1 CPU)
./code_breaker.py --digest=4d546c773867b86b4a233a7428c46c19 --password-length=6 (must take... more!)
"""

from argparse import ArgumentParser
from string import ascii_letters
from itertools import product
from hashlib import md5
from time import time
from binascii import unhexlify

parser = ArgumentParser(description="Add padding to a password so that it matches a SHA-512 prefix pattern")
parser.add_argument("--digest", help="MD5 digest to be reversed", default="9fcce10c03dc2eaada4c361c508c4ebe")
parser.add_argument("--password-length", type=int, choices=range(1, 20), default=4)
args = parser.parse_args()


def reverse_md5(length: int, digest: str):
    binary_digest = unhexlify(digest)
    for password in product(ascii_letters, repeat=length):
        str_password = "".join(password)
        generated_digest = md5(str_password.encode("utf8")).digest()
        if binary_digest == generated_digest:
            return str_password
    return None


t0 = time()
result = reverse_md5(args.password_length, args.digest)
t1 = time()
print("Found {} result in {} seconds: {}".format(0 if result is None else 1, round(t1-t0, 2), result))
