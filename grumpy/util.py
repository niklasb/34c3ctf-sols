import functools
import itertools

def memoize(f):
    memo = {}
    @functools.wraps(f)
    def helper(*args):
        if args not in memo:
            memo[args] = f(*args)
        return memo[args]
    return helper

def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)

def unpack_le(byte_values):
    return sum(x * pow(0x100, i) for i, x in enumerate(byte_values))

def pack_le(value):
    res = []
    while value:
        res.append(value & 0xff)
        value >>= 8
    return value
