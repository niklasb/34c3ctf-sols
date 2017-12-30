import struct, os, sys
from sage.all import matrix, vector
from subprocess import Popen, PIPE

os.system('clang++ -std=c++11 stream.cpp -o stream')

def babai(A, w):
    ''' http://sage-support.narkive.com/HLuYldXC/closest-vector-from-a-lattice '''
    C = max(max(row) for row in A.rows())
    B = matrix([list(row) + [0] for row in A.rows()] + [list(w) + [C]])
    B = B.LLL(delta=0.9)
    return w - vector(B.rows()[-1][:-1])

def rng(n):
    p = Popen('./stream', stdin=PIPE, stdout=PIPE, stderr=PIPE)
    res = []
    for _ in range(n):
        res.append(int(p.stdout.readline().strip()))
    p.kill()
    p.wait()
    return res

m = 64

with open(sys.argv[1]) as f:
    dat = f.read()

    n, = struct.unpack("<Q", dat[:8])
    dat = dat[8:]

    c = vector([0]*m)
    for i in range(m):
        c[i], = struct.unpack("<Q", dat[:8])
        dat = dat[8:]

A = matrix(m, n)
values = rng(m*n)
for i in range(m):
    for j in range(n):
        A[i,j] = values[i*n + j]

mod = 2**64

X = matrix([[0]*(n+m) for _ in range(n+m)])
for i in range(n):
    X[i,i]=-1
for i in range(n,n+m):
    X[i,i]=mod

for i in range(m):
    for j in range(n):
        X[j,n+i] = A[i,j]

t = vector([0]*n + list(c))
res = t-babai(X, t)
print repr(''.join(map(chr,list(res)[:n])))
