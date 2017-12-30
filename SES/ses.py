#!/usr/bin/env python2
import array
import struct
import random
import hashlib

def ary(*x):
    return array.array('B', *x)

def add(a, b):
    a, b = map(ary, (a,b))
    return ary([x^y for x, y in zip(ary(a), b)])

def mul(a, b):
    p = 0
    while b:
        if b & 1:
            p ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x1b
        b >>= 1
    return p & 0xff

ses_sbox = ary(
    'c61963bc974832ed64bbc11e35ea904f99463ce3c8176db23be49e416ab5cf10'
    '78a7dd0229f68c53da057fa08b542ef127f8825d76a9d30c855a20ffd40b71ae'
    'a17e04dbf02f558a03dca679528df728fe215b84af700ad55c83f9260dd2a877'
    '1fc0ba654e91eb34bd6218c7ec334996409fe53a11ceb46be23d4798b36c16c9'
    '08d7ad725986fc23aa750fd0fb245e815788f22d06d9a37cf52a508fa47b01de'
    'b66913cce738429d14cbb16e459ae03fe9364c93b8671dc24b94ee311ac5bf60'
    '6fb0ca153ee19b44cd1268b79c4339e630ef954a61bec41b924d37e8c31c66b9'
    'd10e74ab805f25fa73acd60922fd87588e512bf4df007aa52cf389567da2d807'.decode('hex')
)

ses_inv_sbox = ary([0]*len(ses_sbox))
for i in range(len(ses_sbox)):
    ses_inv_sbox[ses_sbox[i]] = i

def sub_bytes(block, sbox=ses_sbox):
    block = ary(block)
    for i in xrange(len(block)):
        block[i] = sbox[block[i]]
    return block

def shift_rows(b):
    b = ary(b)
    b[1], b[5], b[9],  b[13] = b[5],  b[9],  b[13], b[1]
    b[2], b[6], b[10], b[14] = b[10], b[14], b[2],  b[6]
    b[3], b[7], b[11], b[15] = b[15], b[3],  b[7],  b[11]
    return b

def shift_rows_inv(b):
    b = ary(b)
    b[5],  b[9],  b[13], b[1]  = b[1], b[5], b[9],  b[13]
    b[10], b[14], b[2],  b[6]  = b[2], b[6], b[10], b[14]
    b[15], b[3],  b[7],  b[11] = b[3], b[7], b[11], b[15]
    return b

def mix_columns(block):
    block = ary(block)
    for col in xrange(0, 16, 4):
        v0, v1, v2, v3 = block[col:col + 4]
        block[col]     = mul(v0, 2) ^ v3 ^ v2 ^ mul(v1, 3)
        block[col + 1] = mul(v1, 2) ^ v0 ^ v3 ^ mul(v2, 3)
        block[col + 2] = mul(v2, 2) ^ v1 ^ v0 ^ mul(v3, 3)
        block[col + 3] = mul(v3, 2) ^ v2 ^ v1 ^ mul(v0, 3)
    return block

def mix_columns_inv(block):
    block = ary(block)
    for col in xrange(0, 16, 4):
        v0, v1, v2, v3 = block[col:col + 4]
        block[col]     = mul(v0, 14) ^ mul(v3, 9) ^ mul(v2, 13) ^ mul(v1, 11)
        block[col + 1] = mul(v1, 14) ^ mul(v0, 9) ^ mul(v3, 13) ^ mul(v2, 11)
        block[col + 2] = mul(v2, 14) ^ mul(v1, 9) ^ mul(v0, 13) ^ mul(v3, 11)
        block[col + 3] = mul(v3, 14) ^ mul(v2, 9) ^ mul(v1, 13) ^ mul(v0, 11)
    return block

def hashfunc(st):
    return ary(hashlib.sha256(ary(st).tostring()).digest()[:16])

def pad(st):
    st = ary(struct.pack('>Q', len(st))) + ary(st)
    while len(st) % 16:
        st.append(random.randrange(0x100))
    st.extend(hashfunc(st))
    return st

def unpad(st):
    sz, = struct.unpack('>Q', st[:8].tostring())
    assert st[-16:] == hashfunc(st[:-16])
    return st[8:8+sz]

class SES(object):
    ''' A simple authenticated block cipher for the masses '''
    def __init__(self, key):
        self.setkey(key)

    def setkey(self, key):
        self.key = ary(key)
        self.key_size = len(key)
        assert self.key_size == 16
        # better safe than sorry
        self.rounds = 31337
        self.expand_key()

    def expand_key(self):
        exkey = ary(self.key)
        word = exkey[-4:]
        rcon = 0x8d
        for i in xrange(1, self.rounds + 1):
            word = word[1:4] + word[0:1]
            for j in xrange(4):
                word[j] = ses_sbox[word[j]]
            word[0] ^= rcon
            rcon = mul(rcon, 2)
            for z in xrange(4):
                for j in xrange(4):
                    word[j] ^= exkey[-self.key_size + j]
                exkey.extend(word)
            if len(exkey) >= (self.rounds + 1) * 16:
                break
        self.exkey = exkey

    def get_round_key(self, round):
        return ary([self.exkey[round*16 + i] for i in range(16)])

    def encrypt_block(self, block):
        block = add(block, self.get_round_key(0))

        for round in xrange(1, self.rounds):
            block = sub_bytes(block, ses_sbox)
            block = shift_rows(block)
            block = mix_columns(block)
            block = add(block, self.get_round_key(round))

        block = sub_bytes(block, ses_sbox)
        block = shift_rows(block)
        block = add(block, self.get_round_key(self.rounds))
        return block

    def decrypt_block(self, block):
        block = add(block, self.get_round_key(self.rounds))

        for round in xrange(self.rounds - 1, 0, -1):
            block = shift_rows_inv(block)
            block = sub_bytes(block, ses_inv_sbox)
            block = add(block, self.get_round_key(round))
            block = mix_columns_inv(block)

        block = shift_rows_inv(block)
        block = sub_bytes(block, ses_inv_sbox)
        block = add(block, self.get_round_key(0))
        return block

    def encrypt(self, plain):
        plain = pad(plain)
        res = ary()
        for i in range(0, len(plain), 16):
            res.extend(self.encrypt_block(plain[i:i+16]))
        return res

    def decrypt(self, cipher):
        assert len(cipher) % 16 == 0
        res = ary()
        for i in range(0, len(cipher), 16):
            res.extend(self.decrypt_block(cipher[i:i+16]))
        return unpad(res)


if __name__ == '__main__':
    key = ary('AAAABBBBCCCCDDDD')
    plain = ary('FFFFGGGGHHHHIIII')
    cipher = SES(key)
    assert cipher.decrypt_block(cipher.encrypt_block(plain)) == plain
    for i in [0,1,15,16,17,31,32]:
        assert cipher.decrypt(cipher.encrypt('A'*i)) == ary('A'*i)

    key = open('/dev/urandom').read(16)
    flag = '34C3_....'
    cipher = SES(key).encrypt(flag)
    with open('flag.enc', 'wb') as f:
        f.write(cipher.tostring())
