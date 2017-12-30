from subprocess import check_output, PIPE
import ast
from pwnlib.par import iter_parallel # https://github.com/niklasb/ctf-tools
import sys

def eval_game((w, h)):
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
        print 'running %s' % ' '.join("'%s'"%c for c in cmd)
        out = check_output(cmd, stdin=PIPE, stderr=PIPE)
        if 'SIGTRAP' in out and not 'SIGSEGV' in out:
            break
    else:
        assert False, "Too many retries for %d, %d" % (w, h)
    print 'done %d %d' % (w, h)
    sys.stdout.flush()
    return ast.literal_eval(out.split('START')[1].split('END')[0])

def eval_game2():
    # doesn't work
    for _ in range(10):
        out = check_output(['gdb', './patched',
            '-ex', 'br Main_moves_info',
            '-ex', 'r +RTS -qg -qb -I0 -V0 -C0 -N1 -maxN1 -i0 -qm -Z -A1G -H1G -ki20M',
            '-ex', 'set $r14=0x6E2D58',
            '-ex', 'set {long long}$rbp=0x4dfa20',
            '-ex', 'del br 1',
            '-ex', 'c',
            '-ex', 'source extract_gdb.py',
            '-ex', 'quit'], stdin=PIPE, stderr=PIPE)
        if 'SIGTRAP' in out and not 'SIGSEGV' in out:
            break
    else:
        assert False, "Too many retries"
    sys.stdout.flush()
    return ast.literal_eval(out.split('START')[1].split('END')[0])

if __name__ == '__main__':
    print eval_game((1,2))
    print eval_game2()
