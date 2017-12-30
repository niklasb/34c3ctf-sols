from __future__ import print_function
import gdb
import re
import tempfile
import threading
import traceback

import util

REGISTERS = {
    8 : ['al', 'ah', 'bl', 'bh', 'cl', 'ch', 'dl', 'dh'],
    16: ['ax', 'bx', 'cx', 'dx'],
    32: ['eax', 'ebx', 'ecx', 'edx', 'esi', 'edi', 'ebp', 'esp', 'eip'],
    64: ['rax', 'rbx', 'rcx', 'rdx', 'rsi', 'rdi', 'rbp', 'rsp', 'rip',
         'r8', 'r9', 'r10', 'r11', 'r12', 'r13', 'r14', 'r15']
}
FLAGS_REG = 'eflags'

def is_ascii(c):
    return 0x20 <= c <= 0x7e or chr(c) in '\r\n\t'

class EzGdb(object):
    def __init__(self):
        self.mx = threading.Lock()

    def execute(self, cmd):
        with self.mx:
            #print('Executing command {}'.format(cmd))
            return gdb.execute(cmd, False, True)

    @util.memoize
    def get_arch(self):
        out = self.execute('maintenance info sections ?')
        m = re.search(r'file type ([^\.]+)', out)
        assert m
        arch = m.group(1)
        return arch, 64 if '64' in arch else 32

    def get_bits(self):
        return self.get_arch()[1]

    def get_stack_reg(self):
        return REGISTERS[self.get_bits()][7]

    def get_ip_reg(self):
        return REGISTERS[self.get_bits()][8]

    def get_breakpoints(self):
        out = self.execute('info breakpoints')
        result = []
        for line in out.splitlines():
            if re.match(r'^(\d+).*', line):
                addr = line.split()[4]
                num = line.split()[0]
                if addr.startswith('0x'):
                    result.append((int(num), int(addr, 16)))
        return result

    def is_mapped(self, addr):
        try:
            self.execute('x/1b {}'.format(addr))
            return True
        except gdb.MemoryError:
            return False

    def make_smart(self, val):
        # is it a pointer at all?
        if self.is_mapped(val):
            # is it code?
            if self.is_executable(val):
                return {
                    'type': 'instruction',
                    'value': self.disassemble(val, 1),
                    'address': val,
                }

            # is it an ASCII string?
            bytes = self.read(val, 8)
            strlen = next((i for i, b in enumerate(bytes) if not b), 8)
            if strlen >= 4 and all(map(is_ascii, bytes[:strlen])):
                return {
                    'type': 'string',
                    'value': self.read_c_str(val),
                    'address': val,
                }
            # just a regular pointer, read target and recurse
            target32 = util.unpack_le(self.read(val, 4))
            # herustic: detect pointer to 32-bit integer
            if target32 <= 2**16:
                target = { 'type': 'number', 'value': target32 }
            else:
                target64 = util.unpack_le(self.read(val, 8))
                target = self.make_smart(target64)
            return {
                'type': 'pointer',
                'value': val,
                'target': target,
            }

        # no pointer, assume integer
        return { 'type': 'number', 'value': val }

    def get_registers(self):
        regs = {}
        for line in self.execute('info registers').splitlines():
            parts = line.split()
            regs[parts[0]] = int(parts[1], 16)
        return regs

    def get_reginfo(self):
        values = self.get_registers()
        regs = REGISTERS[self.get_bits()] + [FLAGS_REG]
        return [
            {
                'name': r,
                'value': values[r],
            }
            for r in regs]

    def get_ip(self):
        return self.get_registers()[self.get_ip_reg()]

    def disassemble(self, addr, n):
        gdb.execute('set disassembly-flavor intel')
        asm = self.execute('x/{}i {}'.format(n, addr))
        lines = asm.splitlines()
        # We need to support at least two different formats:
        # 1. ADDR <label+X>: INS
        # 2. ADDR: INS
        #
        # With disassemble command, we could also get prefix
        # "Dump of function label:", then instruction format
        # 3. ADDR <+X>: INS
        func = None
        if lines[0][-1] == ':':
            func = lines[0].split()[-1][:-1]
            lines = lines[1:]
        ins = []
        lines = iter(lines)
        for line in lines:
            parts = line.split()
            if parts[0] == '=>':
                parts = parts[1:]

            label = None
            addr = int(parts[0].rstrip(':'), 16)

            if parts[1].startswith('<'):
                label = parts[1][1:-2]
                if label[0] == '+':
                    label = func + label
                parts = parts[2:]
            else:
                parts = parts[1:]

            # join with succeeding line if wrapped
            if not parts:
                parts += next(lines).split()
            mnemonic = parts[0]
            op_str = ' '.join(parts[1:])
            ins.append({
                'address': addr,
                'label': label,
                'mnemonic': mnemonic,
                'op_str': op_str,
            })
        return ins

    def get_breakpoint_num(self, addr):
        bps = self.get_breakpoints()
        return next((num for num, bp in bps if bp == addr), None)

    def set_breakpoint(self, addr):
        if self.get_breakpoint_num(addr) is None:
            self.execute('break *{}'.format(addr))

    def delete_breakpoint(self, addr):
        num = self.get_breakpoint_num(addr)
        if num is not None:
            self.execute('delete breakpoint {}'.format(num))

    def read(self, start, size):
        out = self.execute('x/{}bx {}'.format(size, start))
        res = []
        for line in out.splitlines():
            res += [int(x, 16) for x in line.split(':')[1].split()]
        assert len(res) == size
        return res

    def read_c_str(self, addr):
        res = ''
        while True:
            b = self.read(addr, 1)[0]
            if not b:
                break
            res += chr(b)
            addr += 1
        return res

    def eval_location(self, expr):
        out = self.execute('x/1b {}'.format(expr))
        return int(out.split(':')[0], 16)

    def get_pid(self):
        out = self.execute('info proc')
        return int(out.splitlines()[0].split()[-1])

    def get_maps(self):
        maps = []
        with open('/proc/{}/maps'.format(self.get_pid())) as f:
            for line in f:
                parts = line.split()
                start, end = [int(x, 16) for x in parts[0].split('-')]
                mode = parts[1]
                offset = int(parts[2], 16)
                fname = None
                if len(parts) > 5:
                    fname = parts[-1]
                maps.append({
                    'start': start,
                    'end': end,
                    'mode': mode,
                    'offset': offset,
                    'file': fname,
                })
        return maps

    def get_map_for_address(self, addr):
        maps = self.get_maps()
        return next((m for m in self.get_maps() if m['start'] <= addr < m['end']), None)

    def has_mode(self, addr, mode):
        return mode in self.get_map_for_address(addr)['mode'][:3]

    def is_executable(self, addr):
        return self.has_mode(addr, 'x')
