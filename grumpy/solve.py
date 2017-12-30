from subprocess import check_output, PIPE
import ast, random, json, os, sys

# https://github.com/niklasb/ctf-tools
from pwnlib.par import iter_parallel
from pwnlib.tools import x86_64


# Patch out some GC/multi-threading stuff that gets in the way
dat = open('files/grumpy').read()
dat = bytearray(dat)

space = 0x4dfa00  # some free buffer in r-x memory
base = 0x400000   # binary base

heap = 0x730000   # free heap space

payload = x86_64.assemble(r'''
align 0x10
dq 0
dq 0
dq 0
dq 0x3F00000020

entry:
jmp forcelist

align 0x10
dq 0
dq 0
dq 0
dq 0x3F00000020

forcelist:
and rbx, ~7
cmp qword [rbx], 0x47ae30
jne done

push rbx
mov rbx, [rbx+8]
lea rax, [rel next]
mov [rbp-8], rax
sub rbp, 8
jmp [rbx]


align 0x10
dq 0
dq 0
dq 0
dq 0x3F00000020

next:
and rbx, ~7
mov rax, [{element_cnt}]
lea rax, [{element_ary}+rax*8]
mov [rax], rbx
inc qword [{element_cnt}]

; rbx is game element here
pop rbx
mov rbx, [rbx+16]
lea rax, [rel forcelist]
mov [rbp-8], rax
sub rbp, 8
jmp [rbx]

done:
int3
int3
int3

'''.format(element_cnt=heap, element_ary=heap+8))

assert len(payload) < 800
dat[space-base:space-base+len(payload)] = payload

# nop out preemption (see https://ghc.haskell.org/trac/ghc/wiki/Commentary/Rts/Scheduler)
dat[0x47E490-base]='\xc3'  # contextSwitchAllCapabilities
dat[0x47E4E0-base]='\xc3'  # interruptAllCapabilities
with open('patched', 'w') as f:
    f.write(dat)

# extract games to be evaluated
check_output(['gdb', 'files/grumpy',
    '-ex', 'br Main_main_info',
    '-ex', 'source dump_games.py'], stdin=PIPE, stderr=PIPE)

def eval_game((w, h)):
    ''' uses dynamic analysis to evaluate the moves function '''
    for _ in range(10):
        cmd = ['gdb', './patched',
            '-ex', 'br Main_moves_info',
            '-ex', 'r +RTS -qg -qb -I0 -V0 -C0 -N1 -maxN1 -i0 -qm -Z -A1G -H1G -ki20M',
            '-ex', 'set {long long}0x6e3500=%d'%w,
            '-ex', 'set {long long}0x6e3510=%d'%h,
            '-ex', 'set {long long}$rbp=0x4dfa20',
            '-ex', 'c',
            '-ex', 'source extract_gdb.py',
            '-ex', 'quit']
        #print 'running %s' % ' '.join("'%s'"%c for c in cmd)
        out = check_output(cmd, stdin=PIPE, stderr=PIPE)
        if 'SIGTRAP' in out and not 'SIGSEGV' in out:
            break
    else:
        assert False, "Too many retries for %d, %d" % (w, h)
    print 'done %d %d' % (w, h)
    sys.stdout.flush()
    return ast.literal_eval(out.split('START')[1].split('END')[0])

games = [(w, h) for w in range(51) for h in range(51)]

if os.path.exists('moves.json'):
    print 'using file moves.json'
    moves = json.load(open('moves.json'))
else:
    moves = iter_parallel(eval_game, games, n=20)
    with open('moves.json', 'w') as f:
        f.write(json.dumps(moves))

moves = dict(zip(games, moves))

memo = {}
def mex(s):
    for i in range(1000):
        if i not in s:
            return i
    assert False

def f(w, h):
    ''' original function for verification purposes '''
    if w==0 or h==0:
        return 0
    if (w,h) in memo:
        return memo[w,h]

    s = set()
    for x in [1,2,3]:
        if ((w-x)%2) ^ (w==42):
            for l in range(0, w-x+1):
                # print w, h, l,h,w-l-x,h
                s.add(f(l,h)^f(w-l-x,h))
    for x in [1,2,3]:
        if ((h-x)%2) ^ (h==42):
            for l in range(0, h-x+1):
                # print w, h, w,l,w,h-l-x
                s.add(f(w,l)^f(w,h-l-x))
    memo[w,h] = mex(s)
    return memo[w,h]

memo2 = {}
def f2(w, h):
    ''' solver function using sprague-grundy theorem '''
    if (w,h) in memo2:
        return memo2[w,h]
    s = set()
    for nxt in moves[w,h]:
        # print w, h, nxt
        x = 0
        for nw, nh in nxt:
            x ^= f2(nw, nh)
        s.add(x)
    memo2[w,h] = mex(s)
    return memo2[w,h]

for i in range(51):
    for j in range(51):
        assert f2(i,j)==f(i,j)

bits = ''
games = json.load(open('games.json'))
for g in games:
    x = 0
    for w,h in g:
        assert f(w,h) == f2(w,h)
        x ^= f(w,h)
    if x:
        bits += '1'
    else:
        bits += '0'
res = ''
for i in range(0,len(bits),8):
    res += chr(int(bits[i:i+8],2))
print res
