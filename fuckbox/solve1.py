from subprocess import check_output
import string
import re
import json
import urllib
from jsfuck import MAPPING

f=open('payload.js').read()

def rep(x, y):
    global f
    f = f.replace(x, y)

def reg(x, y):
    global f
    f=re.sub(x,y,f)

try:
    cache=json.load(open('cache.json'))
except IOError:
    cache = {}

def ev(x):
    if x in cache:
        r=cache[x]
    else:
        r=check_output(['node','-e','console.log(JSON.stringify(%s))'%x]).strip()
        cache[x]=r
    return r

def e(x):
    r=ev(x)
    rep('(%s)'%x,'(%s)'%r)
    rep('[%s]'%x,'[%s]'%r)

def s(x):
    e('+'.join('"%s"'%c for c in x))

def strconcat():
    reg(r'''([\(\[]|"\+)"([^"\\]*)"\+"([^"\\]*)"([+\]\)])''', lambda m: m.group(1)+'"' + m.group(2)+m.group(3) + '"'+m.group(4))
    reg(r'''([\(\[])"([^"\\]*)"\+'"'([+\]\)])''', lambda m: m.group(1)+'"' + m.group(2) + '\\""'+m.group(3))

for _ in range(30):
    for x, y in MAPPING.items():
        if x != "'" and x != "\\":
            rep(y, '"%s"' % x)
    for i in range(1,10):
        e('!![]+'*(i-1) + '!![]')
    e('!![]+!![]+!![]+[0]')
    e('[]+[]')
    e('+[![]]')
    e('+[]')
    e('![]')
    s('entries')
    s('status')
    e('[][[]]')
    e('([false]+[][[]])["10"]')
    e('([]+[]["fill"])[3]')
    e('false+[]')
    e('[false]+undefined')
    e('1+[0]')
    e('undefined+[]')
    e('[false]+[][[]]')
    e('[]+[]["fill"]')
    e('!![]+[]["fill"]')
    e('![]+[]["fill"]')
    e('!![]+!![]+[0]')
    e('[!![]][+" "]')
    e('+[false]+[true]+[]["fill"]')
    e('+!![]')
    e('!![]+!![]')
    e('+!![]+[0]')
    e('!![]+[]')
    e('![]+[]')
    e('+!+[]')
    e('+[]')
    e('!+[]+!+[]+!+[]')
    e('!+[]+!+[]')
    e('[][[]]+[]')
    e('[![]]+[][[]]')
    e('+!+[]+[0]')
    e('+!![]+[3]')
    e('[true][+" "]')
    e('[]["entries"]()+[]')
    e('+[false]+[[true][+" "]]+[]["fill"]')
    e('[]+0["constructor"]')
    e('+[]+[0]+null+![]')
    e('+!![]+[1]')
    e('[]+(0)["constructor"]')
    e('+(+!![]+[1]+"e"+2+0)+[]')
    e('[]["filter"]+[]')
    e('!![]+[]["filter"]')
    e('+[false]+[]["filter"]')
    e('+!+[]+[1]')
    e('+![]+("")["constructor"]')
    e('+![]+[false]+("")["constructor"]')
    e('!+[]+!+[]+[0]')
    e('!+[]+!+[]+!+[]+[1]')
    e('!+[]+!+[]+[1]+[2]')
    e('+"212"')
    e('![]+[]["filter"]')
    e('+"11"')
    e('!+[]+!+[]+[1]+[1]')
    e('!+[]+!+[]+[1]')
    e('!+""+!+""+!+""+!+""+!+""+!+[]')
    e('!+""+!+""+[!+""+!+""+!+""+!+""+!+""+!+""+!+[]]')
    e('!+""+!+""+[3]')
    e('!+""+!+""+!+""+!+""+!+""+!+""+!+[]')
    e('!+""+!+""+!+""+!+""+!+[]')
    e('+(+!+"0"+[1])')
    e('this+[]')
    e('!+""+[]')
    e('+!+""+"e"+"1"+"0"+[0]')
    e('+"1e100"+[]')
    e('+!+""+"0"+[1]')
    e('+!+""+"e"+"1"+"0"+"0"+[0]')
    e('+[false]+[+"1e1000"]')
    e('!+""+!+""+!+""+!+""+[0]')
    e('!+""+!+""+!+""+!+""+!+""+!+""+!+""+!+""+!+[]')
    e('+!+""+[2]')
    e('+![]+false["constructor"]')
    e('+![]+[]["constructor"]')
    e('![]+[+![]]')
    e('!+""+!+""+[!+""+!+""+!+""+!+[]]')
    e('+(!+""+!+""+!+""+[2])')
    e('0["constructor"]+[]')
    e('"return/0"+"false0"["italics"]()["10"]')
    for x in range(10):
        e('!+""+!+""+!+""+[%d]'%x)
    e('(/0/)["constructor"]+[]')
    e('(/0/)["constructor"]()+[]')
    e('!+""+!+""+!+""+!+""+!+""+!+""+!+""+!+[]')
    e('+!+""+"e100"+[0]')
    e('+!+""+"e10"+[0]')
    e('!+""+!+""+!+""+!+[]')
    e('("")["fontcolor"]()["11"]')
    e('!+""+!+""+!+""+!+[]')
    for x in range(10):
        e('!+""+!+""+!+""+!+""+!+""+[%d]'%x)
    e('+!+""+!+[]')
    e('![]+![]')
    e('!![]+Date()')
    e('(new Date(24000000000))+[]')
    e('+[false]+Date()')

    reg(r'\+\("([^"]+)"\)', r'+"\1"')
    reg(r'\[\("([^"]+)"\)', r'["\1"')
    reg(r'\(\("([^"]+)"\)', r'("\1"')
    reg(r'\+\((\d+)\)', r'+\1')
    reg(r'\[\((\d+)\)', r'[\1')
    reg(r'\(\((\d+)\)', r'(\1')

    reg(r'"[^"]+"\[\d+\]', lambda m: ev(m.group(0)))
    reg(r'"[^"]+"\["\d+"\]', lambda m: ev(m.group(0)))
    strconcat()
    reg(r'''unescape\(([^\(\)]+)\)''', lambda m: urllib.unquote(ev(m.group(1))))

    rep('[]["fill"]["constructor"]("return eval")()', 'eval')
    rep('[]["fill"]["constructor"]("return statusbar")()', 'statusbar')
    rep('[]["fill"]["constructor"]("return atob")()', 'atob')
    rep('[]["fill"]["constructor"]("return btoa")()', 'btoa')
    rep('[]["fill"]["constructor"]("return escape")()', 'escape')
    rep('[]["fill"]["constructor"]("return unescape")()', 'unescape')
    rep('[]["filter"]["constructor"]("return eval")()', 'eval')
    rep('[]["filter"]["constructor"]("return statusbar")()', 'statusbar')
    rep('[]["filter"]["constructor"]("return atob")()', 'atob')
    rep('[]["filter"]["constructor"]("return btoa")()', 'btoa')
    rep('[]["filter"]["constructor"]("return escape")()', 'escape')
    rep('[]["filter"]["constructor"]("return unescape")()', 'unescape')
    rep('[]["filter"]["constructor"]("return this")()', 'this')
    rep('[]["filter"]["constructor"]("return/0/")()', '(/0/)')
    rep('[]["filter"]["constructor"]("return Date")()', 'Date')
    rep('[]["filter"]["constructor"]("return new Date(24000000000)")()', '(new Date(24000000000))')
    rep('statusbar+[]', '"[object BarProp]"')
    rep('atob("00nullfalse")[1]', '"C"')
    rep('+("")["constructor"]["n"+"a"+"m"+"e"]+', '+"String"+')
    rep('+(+"211")["toString"]("31")[1]+', '+"p"+')
    rep('+(+"211")["toString"]("31")[1]]', '+"p"]')
    rep('+212["toString"]("31")[1]+', '+"q"+')
    rep('+("")["fontcolor"]()["11"]+', '+"="+')
    rep('+[[]]["concat"]([[]])+', '+","+')
    rep('+11["toString"]("20")+', '+"b"+')
    rep('+(+"101")["toString"]("21")[1]+', '+"h"+')
    rep('+(+"20")["toString"]("21")+', '+"k"+')
    rep('+(this+[])[0]+', '+"["+')
    rep('+(+"40")["toString"]("21")[1]+', '+"j"+')
    rep('+"false0"["italics"]()["10"]+', '+"/"+')
    rep('+32["toString"]("33")+', '+"w"+')
    rep('+[]+', '+""+')
    rep('+11["toString"]("20"))', '+"b")')
    rep('+(+"101")["toString"]("34")[1]+', '+"x"+')
    rep('+(+"31")["toString"]("32")+', '+"v"+')
    for x in range(10):
        rep('+[%d]+'%x, '+"%d"+'%x)
    rep('escape("<")[0]', '"%"')
    rep('escape("<")[2]', '"C"')
    rep('unescape("%3b")', '";"')
    rep('+" "+[false]+""+', '+" false"+')
    rep(' "+[true]+""+', ' true"+')
    rep('+("")["fontcolor"]()["12"]+', '+\'"\'+')
    rep('+escape("=")[2]+', '+"D"+')

    for c in '+([':
        for x in ['undefined', 'false', 'true', 'null']:
            rep(c+'(%s)'%x,c+x)

    for x in range(0x100):
        rep('{:08b}'.format(x).replace('0', '_').replace('1', '$'), 'n%d'%x)

for _ in range(1000):
    strconcat()

print len(f)
json.dump(cache, open('cache.json', 'w'))
with open('payload2.js','w') as g:
    g.write(f)
