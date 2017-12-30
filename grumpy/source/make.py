import random
import json

memo = {}

W = 50
H = 50

def mex(s):
    for i in range(1000):
        if i not in s:
            return i
    assert False

def f(w, h):
    if w==0 or h==0:
        return 0
    if (w,h) in memo:
        return memo[w,h]

    s = set()
    for x in [1,2,3]:
        if ((w-x)%2)^(w==42):
            for l in range(0, w-x+1):
                s.add(f(l,h)^f(w-l-x,h))
    for x in [1,2,3]:
        if ((h-x)%2)^(h==42):
            for l in range(0, h-x+1):
                s.add(f(w,l)^f(w,h-l-x))
    memo[w,h] = mex(s)
    return memo[w,h]

for i in range(W):
    for j in range(H):
        f(i,j)

flag = "34C3_G-machines+Grundy_G1ve_Grumpy_G4mbl3rs_Gr3at_Gr1ef:("

def subsetxor(n, xor_range, W, H):
    dp=[]
    N = 500
    dp.append([True]+[None]*N)
    ws = range(*W)
    hs = range(*H)
    for i in range(n):
        dp.append([None]*N)
        for xor in range(N):
            if dp[-2][xor] is None:
                continue
            random.shuffle(ws)
            random.shuffle(hs)
            for w in ws:
                for h in hs:
                    x = f(w,h)
                    if (xor^x) >= N:
                        continue
                    dp[-1][xor^x] = (w, h, xor)

    xor_range = list(xor_range)
    random.shuffle(xor_range)
    for x in xor_range:
        if dp[-1][x] is None:
            continue
        i = len(dp)-1
        res = []
        while i > 0:
            w,h,x = dp[i][x]
            res.append((w,h))
            i -= 1
        return res
    assert False


def build(st, W, H, multi=1):
    ones = [[(w,h)] for w in range(*W) for h in range(*H) if f(w,h)]
    zeroes = [[(w,h)] for w in range(*W) for h in range(*H) if f(w,h)==0]
    random.shuffle(ones)
    random.shuffle(zeroes)
    for c in st:
        for b in '{:08b}'.format(ord(c)):
            if b=='1':
                if multi>1:
                    yield subsetxor(random.randint(2, multi), range(1,100), W, H)
                else:
                    yield ones[0]
                    ones = ones[1:] + [ones[0]]
            else:
                if multi>1:
                    yield subsetxor(random.randint(2, multi), [0], W, H)
                else:
                    yield zeroes[0]
                    zeroes = zeroes[1:] + [zeroes[0]]

def fmt(games):
    if len(games) == 1:
        return 'OneGame %d %d' % games[0]
    else:
        return 'TwoGames (OneGame %d %d) (%s)' % (games[0][0], games[0][1], fmt(games[1:]))

splitat = flag.index('Grumpy')
games = (
    list(build(flag[:3], (4,6), (4,6)))+
    list(build(flag[3:5], (3,5), (3,5), multi=2))+
    list(build(flag[5:splitat], (W//2,W), (H//2,H)))+
    list(build(flag[splitat:], (W//2,W), (H//2,H), multi=10))
    )

with open('src/games.h', 'w') as f:
    f.write( ' ' + '\n ,'.join(fmt(x) for x in games))

with open('games.json', 'w') as f:
    f.write(json.dumps(games))
