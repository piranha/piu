import uuid
import os.path as op

from piu import redis
from piu.utils import key, highlight, style, lexerlist, dec
from bottle import route, request, redirect, send_file, response
from bottle import jinja2_template as template

def dec(s):
    return s.decode('utf-8')

@route('/')
def index():
    return template('index', lexers=lexerlist(),
                    deflexer=request.COOKIES.get('lexer'))

@route('/', method='POST')
def paste():
    data = dec(request.POST.get('data'))
    if not data:
        return redirect('/', 302)
    lexer = request.POST.get('lexer', 'guess')
    response.set_cookie('lexer', lexer)
    id = redis.incr(key('next-id'))

    redis.sadd(key('%s:list', id), 1)
    redis.set(key('%s:1:raw', id), data)
    result, lexer = highlight(data, lexer)
    redis.set(key('%s:1:html', id), result)
    redis.set(key('%s:1:lexer', id), lexer)

    return redirect('/%s/' % id, 302)

@route('/:id/')
def show(id):
    lst = redis.smembers(key('%s:list', id))
    if not lst:
        return redirect('/', 302)
    data = [redis[key('%s:%s:html', id, pk)] for pk in lst]
    return template('show', data=data, id=id)

@route('/static/:name#.*#')
def static(name):
    if name == 'style.css':
        response.content_type = 'text/css'
        return style()
    return send_file(name, root=op.join(op.dirname(__file__), 'static'))
