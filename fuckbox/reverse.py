from aes_py import aes128_reverse_keyschedule

res = [
[63, None, None, None, None, None, None, 9, None, None, 222, None, None, 213, None, None],
[None, None, None, 87, None, None, 20, None, None, 225, None, None, 211, None, None, None],
[None, None, 179, None, None, 200, None, None, 203, None, None, None, None, None, None, 231],
[None, 96, None, None, 213, None, None, None, None, None, None, 161, None, None, 225, None]
]

key = [None]*16
for x in res:
    for i, y in enumerate(x):
        if y is not None:
            key[i] = y

print 'Key: '+''.join(map(chr,aes128_reverse_keyschedule(key, 10)))
