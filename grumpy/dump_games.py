import ezgdb
import struct
import json

head=0x708798
con_onegame = (0x40b710, 0x40b730)
ez = ezgdb.EzGdb()

def r64(x):
    return struct.unpack("<Q", bytes(ez.read(x, 8)))[0]

def readgame(x):
    assert not x&7
    con = r64(x)
    a = r64(x+8)&~7
    b = r64(x+16)&~7
    if con in con_onegame:
        return [(r64(a+8), r64(b+8))]
    else:
        return readgame(a)+readgame(b)

x = head
games = []
while r64(x) == 0x47AE50:
    game = r64(x+8)&~7
    games.append(readgame(game))
    x = r64(x+16)&~7

with open('games.json', 'w') as g:
    g.write(json.dumps(games))
