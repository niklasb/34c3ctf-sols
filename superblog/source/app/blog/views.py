import re
import json
import traceback
import random

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.views.decorators.http import require_safe, require_POST
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import models
from random import SystemRandom

def get_user_posts(user):
    if not user.is_authenticated:
        return []
    else:
        return models.Post.objects.filter(author=user).all()

gen = SystemRandom()
def generate_captcha(req):
    n = 2
    d = 8
    ops = '+'
    while True:
        nums = [gen.randint(10**(d-1), 10**d-1) for _ in range(n)]
        ops = [gen.choice(ops) for _ in range(n-1)]
        captcha = ' '.join('%s %s' % a for a in zip(nums,ops+[1]))[:-2]
        answer = eval(captcha)
        if -2**31 + 10 <= answer <= 2**31-10:
            break
    # print 'Captcha:', captcha
    req.session['captcha'] = captcha
    req.session['captcha_answer'] = str(eval(captcha))
    if random.random() < 0.003:
        req.session['captcha'] = r'(__import__("sys").stdout.write("I WILL NOT RUN UNTRUSTED CODE FROM THE INTERNET\n"*1337), %s)[1]'%req.session['captcha']
    return req.session.get('captcha')

def check_captcha(req):
    res = req.POST.get('captcha_answer') == req.session.get('captcha_answer')
    # if not res:
        # print 'Captcha failed:', req.POST.get('captcha_answer'), req.session.get('captcha_answer')
    return res

@require_safe
def index(req):
    if not req.user.is_authenticated:
        return redirect('login')
    return render(req, 'blog/index.html', {
        'posts': get_user_posts(req.user),
        'captcha': generate_captcha(req),
        })

@require_safe
def post(req, postid):
    post = models.Post.objects.get(secretid=postid)
    return render(req, 'blog/post.html', {
        'post': post,
        'captcha': generate_captcha(req),
        })

def contact(req):
    if req.method == 'POST':
        if not check_captcha(req):
            messages.add_message(req, messages.ERROR, 'Invalid or outdated captcha')
            return redirect('contact')
        postid = req.POST.get('postid')
        valid = False
        try:
            models.Post.objects.filter(secretid=postid).get()
            valid = True
        except:
            traceback.print_exc()

        if not valid:
            messages.add_message(req, messages.ERROR,
                'That does not look like a valid post ID')
            return redirect('contact')
        url = 'http://localhost:1342/post/' + postid
        models.Feedback(url=url).save()
        messages.add_message(req, messages.INFO,
                'Thank you for your feedback, an admin will look at it ASAP')
        return redirect('index')
    else:
        feedback_count = models.Feedback.objects.filter(visited=False).count()
        return render(req, 'blog/contact.html', {
            'feedback_count': feedback_count,
            'captcha': generate_captcha(req),
            })

def signup(req):
    if req.method == 'POST':
        form = UserCreationForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(req, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(req, 'blog/signup.html', {'form': form})

def get_flag(req, num):
    if req.user.username == 'admin' and req.META.get('REMOTE_ADDR') == '127.0.0.1':
        with open('/asdjkasecretflagfile%d' % num) as f:
            return f.read()
    else:
        return '34C3_JUSTKIDDINGGETADMINANDACCESSFROMLOCALHOSTNOOB'

@require_safe
def feed(req):
    posts = get_user_posts(req.user)
    posts_json = json.dumps([
        dict(author=p.author.username, title=p.title, content=p.content)
        for p in posts])
    type_ = req.GET.get('type')
    if type_ == 'json':
        resp = HttpResponse(posts_json)
        resp['Content-Type'] = 'application/json; charset=utf-8'
    elif type_ == 'jsonp':
        callback = req.GET.get('cb')
        bad = r'''[\]\\()\s"'\-*/%<>~|&^!?:;=*%0-9[]+'''
        if not callback.strip() or re.search(bad, callback):
            raise PermissionDenied
        resp = HttpResponse('%s(%s)' % (callback, posts_json))
        resp['Content-Type'] = 'text/javascript; charset=utf-8'
    return resp

@require_POST
def publish(req):
    if req.user.username == 'admin':
        messages.add_message(req, messages.INFO,
                'Sorry but admin cannot post for security reasons')
        return redirect('/')

    if not check_captcha(req):
        messages.add_message(req, messages.ERROR, 'Invalid or outdated captcha')
        return redirect('/')

    models.Post(author=req.user,
            content=req.POST.get('post'),
            title=req.POST.get('title')).save()
    return redirect('/')

@require_POST
def flag_api(req):
    if not check_captcha(req):
        raise PermissionDenied
    resp = HttpResponse(json.dumps(get_flag(req, 2)))
    resp['Content-Type'] = 'application/json; charset=utf-8'
    return resp

@require_safe
def flag1(req):
    return render(req, 'blog/flag1.html', {'flag': get_flag(req, 1)})

@require_safe
def flag2(req):
    return render(req, 'blog/flag2.html', {'captcha': generate_captcha(req)})
