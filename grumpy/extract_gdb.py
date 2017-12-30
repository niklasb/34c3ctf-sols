import ezgdb
import struct

heap = 0x730000
con_onegame = (0x40b710, 0x40b730)
ez = ezgdb.EzGdb()

def r64(x):
    return struct.unpack("<Q", bytes(ez.read(x, 8)))[0]

def collect(x):
    assert not x&7
    con = r64(x)
    a = r64(x+8)&~7
    b = r64(x+16)&~7
    if con in con_onegame:
        return [(r64(a+8), r64(b+8))]
    else:
        return collect(a)+collect(b)

cnt = r64(heap)
games = []
for i in range(cnt):
    game = r64(heap+8*(i+1))
    games.append(collect(game))
print('START')
print(repr(games))
print('END')
