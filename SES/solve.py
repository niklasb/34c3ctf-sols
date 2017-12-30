from sage.all import *
from IPython import embed
from ses import SES, ary
import string
import struct
import hashlib
import sys

F = GF(2)
BF = F['X'];
X, = BF._first_ngens(1)

mod = X**8  + X**4  + X**3  + X + 1
FF = GF(2 ** 8, modulus=mod, names=('A',))
A, = FF._first_ngens(1)

int2ele = FF.fetch_int
ele2int = lambda x: x.integer_representation()

def vec(x):
    return vector(FF, map(int2ele, x))

## SBOX generator
# a, b = 223, 198
# for x in range(0x100):
    # print ele2int(int2ele(x)*int2ele(a) + int2ele(b))

zero = '\0'*16

def one_at(i):
    return '\0'*i + '\1' + '\0'*(16-i-1)

cols = []
for i in range(16):
    v = vec(SES(zero).encrypt_block(zero))
    v += vec(SES(zero).encrypt_block(one_at(i)))
    cols.append(v)

A = matrix(FF, cols).transpose()

print "A="
for i in range(16):
    for j in range(16):
        print ele2int(A[i,j]),
    print
print

# cipher = A*plain + f(k),   f non-linear

plain1 = 'AAAABBBBCCCCDDDD'
plain2 = 'FODDASDIASIDISAD'
key = 'FFFFGGGGHHHHIIII'
plainv1 = vec(map(ord,plain1))
plainv2 = vec(map(ord,plain2))
keyv = vec(map(ord,key))

# sanity check 1: linearity?
c1 = vec(SES(key).encrypt_block(plain1))
c2 = vec(SES(key).encrypt_block(plain2))
assert c1+c2 == A*(plainv1+plainv2)
Ainv = A**(-1)

cipher = open('flag.enc').read()

# sanity check 2: encryption correct?
sz=48
actual_key= [246, 34, 24, 48, 163, 233, 92, 230, 115, 20, 160, 94, 245, 124, 143, 77]
assert SES(actual_key).encrypt_block(struct.pack('>Q', sz)+'34C3_w0w') == ary(cipher[:16])

block1 = Ainv*vec(map(ord, cipher[0:16]))
block2 = Ainv*vec(map(ord, cipher[16:32]))
block3 = Ainv*vec(map(ord, cipher[32:48]))
block4 = Ainv*vec(map(ord, cipher[48:64]))
block5 = Ainv*vec(map(ord, cipher[64:80]))

alph = [int2ele(ord(x)) for x in string.printable[:-5]]
# alph = [int2ele(ord(x)) for x in 'w0']

maxlen= len(cipher)-8-16
print maxlen

count=0
total = 16*len(alph)**3
for sz in range(maxlen-15, maxlen+1):
    plain = struct.pack(">Q", sz) + '34C3_\0\0\0'
    v=vec(map(ord,plain))
    assert len(plain) == 16
    for x in alph:
        sys.stdout.write('\rProgress: %.02f%%        ' % (count*100.0/total))
        sys.stdout.flush()
        v[13] = x
        for y in alph:
            v[14] = y
            for z in alph:
                v[15] = z
                bkey = block1 - v
                plain2 = block2 - bkey
                if all(0x20 <= ele2int(x) < 0x80 for x in plain2):
                    # print "YES"
                    # print ary(map(ele2int,plain2)).tostring()
                    plain3 = block3 - bkey
                    if all(0x20 <= ele2int(x) < 0x80 for x in plain3):
                        plain4 = block4 - bkey
                        plain5 = block5 - bkey

                        plain = ary(map(ele2int,v))
                        plain += ary(map(ele2int,plain2))
                        plain += ary(map(ele2int,plain3))
                        plain += ary(map(ele2int,plain4))
                        digest = ary(map(ele2int,plain5))
                        if ary(hashlib.sha256(plain.tostring()).digest()[:16]) == digest:
                            print 'YES'
                            print `plain[8:8+sz].tostring()`
                            exit()

                if 0 and [x,y,z] == [int2ele(ord(c)) for c in 'w0w'] and sz == 49:
                    key = Binv*(block1 - A*v)
                    plain3 = Ainv*(block3 - bkey)
                    plain4 = Ainv*(block4 - bkey)
                    print
                    print 'yes'
                    print ary(map(ele2int,plain2)).tostring()
                    print ary(map(ele2int,plain3)).tostring()
                    print ary(map(ele2int,plain4)).tostring()
                    assert ary(map(ele2int,key)) == ary(actual_key)
                count += 1
print count
