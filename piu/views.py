import uuid
import os.path as op
from hashlib import sha1
from datetime import datetime as dt

from pygments import lexers
from bottle import route, request, redirect, send_file, response
from bottle import jinja2_template as template

from piu import redis
from piu.utils import key, highlight, style, lexerlist, dec
from piu.utils import toepoch, fromepoch

cookie = {'expires': 60*60*24*30*12}

def sign(id, data):
    return sha1(str(id) + data.encode('utf-8')).hexdigest()

def paste(id, data, lexer):
    '''actually paste data in redis'''
    response.set_cookie('lexer', lexer, **cookie)
    # BUG: this does not override old cookie
    response.set_cookie('edit-%s' % id, sign(id, data), **cookie)

    redis.sadd(key('%s:list', id), 1)
    redis.set(key('%s:1:raw', id), data)
    result, lexer = highlight(data, lexer)
    redis.set(key('%s:1:lexer', id), lexer)
    redis.set(key('%s:1:html', id), result)
    redis.set(key('%s:1:date', id), toepoch(dt.now()))

@route('/static/:name#.*#')
@route('/:name#favicon.ico#')
@route('/:name#robots.txt#')
def static(name):
    if name == 'style.css':
        response.content_type = 'text/css'
        return style()
    return send_file(name, root=op.join(op.dirname(__file__), 'static'))

@route('/')
def index():
    return template('index', lexers=lexerlist())

@route('/', method='POST')
def new():
    data = dec(request.POST.get('data'))
    if not data:
        return redirect('/', 302)
    lexer = request.POST.get('lexer', 'guess')
    id = redis.incr(key('next-id'))

    paste(id, data, lexer)
    return redirect('/%s/' % id, 302)


@route('/:id/')
def show(id):
    data = redis.sort(key('%s:list', id), get=key('%s:*:html', id))
    if not data:
        return redirect('/', 302)

    edit = request.COOKIES.get('edit-%s' % id, '')
    owner = edit == sign(id, redis[key('%s:1:raw', id)])

    lexer = lexers.get_lexer_by_name(redis[key('%s:1:lexer', id)]).name

    return template('show', data=data, id=id, owner=owner, lexer=lexer,
                    date=fromepoch(redis.get(key('%s:1:date', id)) or 0))

@route('/:id/raw/')
def show_raw(id):
    data = redis.sort(key('%s:list', id), get=key('%s:*:raw', id))
    if not data:
        return redirect('/', 302)

    response.content_type = 'text/plain; charset=utf-8'
    return data[0]

@route('/:id/edit/')
@route('/:id/edit/', method='POST')
def edit(id):
    lst = redis.smembers(key('%s:list', id))
    if not lst:
        return redirect('/', 302)

    edit = request.COOKIES.get('edit-%s' % id, '')
    owner = edit == sign(id, redis[key('%s:1:raw', id)])
    if not owner:
        return redirect('/%s/' % id, 302)

    if request.method == 'POST':
        data = dec(request.POST.get('data'))
        lexer = request.POST.get('lexer', 'guess')
        paste(id, data, lexer)
        return redirect('/%s/' % id, 302)

    # beware of 0 here!
    data = redis.sort(key('%s:list', id), get=key('%s:*:raw', id))[0]
    return template('index', data=data, id=id, lexers=lexerlist())

@route('/piu')
def piu():
    lexdict = {}
    lexlist = []
    for _, names, fnames, _ in lexers.get_all_lexers():
        lexlist.extend(names)
        for fn in fnames:
            lexdict[fn] = names[0]
    response.content_type = 'text/plain'
    return template('piu.py', extmap=lexdict, lexers=lexlist)

@route('/about/')
def about():
    return template('about')
