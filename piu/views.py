import os.path as op
from hashlib import sha1
from datetime import datetime as dt

from pygments import lexers
from bottle import route, request, redirect, send_file, response
from bottle import jinja2_template as template

from piu import store
from piu.utils import highlight, style, lexerlist, dec
from piu.utils import toepoch, fromepoch

cookie = {'expires': 60*60*24*30*12}

def sign(id, data):
    if isinstance(data, unicode):
        data = data.encode('utf-8')
    return sha1(str(id) + data).hexdigest()

def paste(item, data, lexer):
    '''actually paste data in redis'''
    try:
        response.set_cookie('lexer', lexer, **cookie)
        # BUG: this does not override old cookie
        response.set_cookie('edit-%s' % id, sign(id, data), **cookie)
    except AttributeError:
        pass

    item['raw'] = data
    result, lexer = highlight(data, lexer)
    item['lexer'] = lexer
    item['html'] = result
    item['date'] = toepoch(dt.now())

def regenerate():
    for k in store:
        with store[k] as i:
            i['html'] = highlight(i['raw'], i['lexer'])[0]

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
    return template('index', lexers=lexerlist(),
                    deflexer=request.COOKIES.get("lexer", "guess"))

@route('/', method='POST')
def new():
    data = dec(request.POST.get('data'))
    if not data:
        return redirect('/', 302)
    lexer = request.POST.get('lexer', 'guess')
    item = store.new()
    paste(item, data, lexer)
    return redirect('/%s/' % id, 302)

@route('/:id')
def redirect_show(id):
    return redirect('/%s/' % id, 301)

@route('/:id/')
def show(id):
    try:
        id = int(id)
        item = store[id]
    except (ValueError, KeyError):
        return redirect('/', 302)

    edit = request.COOKIES.get('edit-%s' % id, '')
    owner = edit == sign(id, item['raw'])

    lexer = lexers.get_lexer_by_name(item['lexer']).name

    return template('show', item=item, owner=owner, lexer=lexer,
                    date=fromepoch(item.get('date', 0)))

@route('/:id/raw/')
def show_raw(id):
    try:
        id = int(id)
        item = store[id]
    except (ValueError, KeyError):
        return redirect('/', 302)

    response.content_type = 'text/plain; charset=utf-8'
    return item['raw'].encode('utf-8')

@route('/:id/edit/')
@route('/:id/edit/', method='POST')
def edit(id):
    try:
        id = int(id)
        item = store[id]
    except (ValueError, KeyError):
        return redirect('/', 302)

    edit = request.COOKIES.get('edit-%s' % id, '')
    owner = edit == sign(id, item['raw'])
    if not owner:
        return redirect('/%s/' % id, 302)

    if request.method == 'POST':
        data = dec(request.POST.get('data'))
        lexer = request.POST.get('lexer', 'guess')
        paste(item, data, lexer)
        return redirect('/%s/' % id, 302)

    return template('index', data=item['raw'], id=id, lexers=lexerlist())

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

@route('/piu.el')
def piuel():
    response.content_type = 'text/plain'
    return template('piu.el')

@route('/about/')
def about():
    return template('about')
