import uuid
import os.path as op
from hashlib import sha1

from piu import redis
from piu.utils import key, highlight, style, lexerlist, dec
from bottle import route, request, redirect, send_file, response
from bottle import jinja2_template as template

cookie = {'expires': 60*60*24*30*12}

def paste(id, data, lexer):
    '''actually paste data in redis'''
    response.set_cookie('lexer', lexer, **cookie)
    # BUG: this does not override old cookie
    response.set_cookie('edit-%s' % id, sha1(unicode(id) + data).hexdigest(),
                        **cookie)

    redis.sadd(key('%s:list', id), 1)
    redis.set(key('%s:1:raw', id), data)
    result, lexer = highlight(data, lexer)
    redis.set(key('%s:1:html', id), result)
    redis.set(key('%s:1:lexer', id), lexer)
    print response.wsgiheaders()

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
    lst = redis.smembers(key('%s:list', id))
    if not lst:
        return redirect('/', 302)
    try:
        data = [redis[key('%s:%s:html', id, pk)] for pk in lst]
    except KeyError:
        return redirect('/', 302)

    edit = request.COOKIES.get('edit-%s' % id, '')
    owner = edit == sha1(id + redis[key('%s:1:raw', id)]).hexdigest()

    return template('show', data=data, id=id, owner=owner)

@route('/:id/edit/')
@route('/:id/edit/', method='POST')
def edit(id):
    lst = redis.smembers(key('%s:list', id))
    if not lst:
        return redirect('/', 302)

    edit = request.COOKIES.get('edit-%s' % id, '')
    owner = edit == sha1(id + redis[key('%s:1:raw', id)]).hexdigest()
    if not owner:
        return redirect('/%s/' % id, 302)

    if request.method == 'POST':
        data = dec(request.POST.get('data'))
        lexer = request.POST.get('lexer', 'guess')
        paste(id, data, lexer)
        return redirect('/%s/' % id, 302)

    # beware of 0 here!
    data = [redis[key('%s:%s:raw', id, pk)] for pk in lst][0]
    return template('index', data=data, id=id, lexers=lexerlist())

