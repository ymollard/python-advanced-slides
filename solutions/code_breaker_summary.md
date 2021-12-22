# The code breaker: THe 4 weaknesses of the naive implementation

## Version 1: Avoid I/Os
I/O operations take time. Avoid them as much as possble: 

**What to do:** Replace  `print()` by `#print()`

If this is not possible, use [`asyncio.aprint`](https://aioconsole.readthedocs.io/) to optimize the wait of results from I/Os.

## Version 2: Use appropriate data containers
Here, membership test "elem ∈ L" is better with sets: 

**What to do:** Replace  `found = []` by `found = set()`

Sets are also performant for differences (`s1-s2`) and unions (`s1+s2`).

## Version 3: Use built-in functions
**What to do:** Replace  `[choice(ascii_letters) for _ in range(10)]` by `choices(ascii_letters, k=10)`

Built-in libs are full of micro-optimizations. [Example with choices() implementation](https://github.com/python/cpython/blob/5be98e57b3c3b36d1a1176b49c73b8822c6380e7/Lib/random.py#L460).

## Version 4: Use deterministic approaches
**What to do:** Replace `choices()` by `itertools.product()`

## Version 5: Compare on `bytes` instead of `str`
**What to do:** Convert the hex representation of the input md5 into `bytes` (e.g. using [`unhexlify` from `binascii`](https://docs.python.org/3/library/binascii.html#binascii.unhexlify)) ; and for each generated md5, get its binary `digest()` instead of its `hexdigest()`.

You will save a little overhead due to the conversion of each digest into an hexadecimal string at every loop. 

