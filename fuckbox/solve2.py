import re

f= open('payload3.js').read()
g = open('payload4.js', 'w')
v = open('payload4_vars.js', 'w')

vars = {}
def cb(m):
    name=m.group(1).strip()
    x = m.group(2).strip()
    vars[name] = x
    return '_'+name+'_'

for x in range(0x100):
    reg = r'\bn%d\b'%x
    f = re.sub(reg, str(x), f)

f = re.sub(r'EXPR ([^ ]+)((.|\n)*?)END', cb, f)
f = f.replace('_NUMS_','')
f = f.replace('_NUMVARS_','')
v.write('_ARY1_=%s;\n'%(vars['ARY1']))
v.write('_ARY2_=%s;\n'%(vars['ARY2']))
v.write('_ARY3_=%s;\n'%(vars['ARY3']))
v.write('_ARY4_=%s;\n'%(vars['ARY4']))
v.write('_ARY5_=%s;\n'%(vars['ARY5']))
v.write('_ARY6_=%s;\n'%(vars['ARY6']))
v.write('_ARY7_=%s;\n'%(vars['ARY7']))

g.write(f)
