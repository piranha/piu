import os
import os.path as op
import json
import re
import sys
from hashlib import sha1
from datetime import datetime as dt

from pygments import lexers
from bottle import route, request, redirect, static_file, response, abort
from bottle import jinja2_template as template

from piu import store
from piu.utils import highlight, ansi2html, style, lexerlist, dec
from piu.utils import toepoch, fromepoch


COOKIE = {'max_age': 60*60*24*30*12, 'path': '/'}
SPAMRE = re.compile('^comment\d+,')
SECRET = os.environ.get('SECRET')
if not SECRET:
    sys.stderr.write("\nWARNING: set 'SECRET' env variable to be secure\n\n")
    SECRET = 'epic-secret'


def sign(id, data):
    if isinstance(data, unicode):
        data = data.encode('utf-8')
    return sha1(SECRET + str(id) + data).hexdigest()


def paste(item, data, lexer):
    '''actually store data'''
    response.set_cookie('lexer', lexer, **COOKIE)
    response.set_cookie('edit-%s' % item.id, item.id, secret=SECRET, **COOKIE)

    item['raw'] = data
    result, lexer = highlight(data, lexer)
    item['lexer'] = lexer
    item['html'] = result
    item['date'] = toepoch(dt.now())
    item.save()


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
    return static_file(name, root=op.join(op.dirname(__file__), 'static'))


@route('/')
def index():
    lexer = (request.GET.get('lexer') or
             request.cookies.get('lexer') or
             'guess')
    return template('index', lexers=lexerlist(), deflexer=lexer)


@route('/', method='POST')
def new():
    if not request.POST.get('data'):
        abort(400, "You have to supply 'data' field")

    data = dec(request.POST['data'])
    if not data:
        abort(400, "Empty 'data' field")

    if SPAMRE.search(data):
        abort(402, 'Wanna spam? Pay me money! ;)')

    lexer = request.POST.get('lexer', 'guess')
    item = store.new()
    paste(item, data, lexer)
    return redirect('/%s/' % item.id, 303)


@route('/:id')
def redirect_show(id):
    return redirect('/%s/' % id, 301)


@route('/:id/')
def show(id):
    try:
        item = store[int(id)]
    except (ValueError, KeyError):
        return redirect('/', 302)

    owner = bool(request.get_cookie('edit-%s' % id, '', secret=SECRET))

    lexer = request.GET.get('as') or item['lexer']

    if lexer == 'ansi':
        item['html'] = ansi2html(item['raw'])
    elif lexer == 'json' and 'pretty' in request.GET:
        try:
            data = json.dumps(json.loads(item['raw']), sort_keys=True, indent=4)
            item['html'] = highlight(data, lexer)[0]
        except ValueError:
            pass
    elif lexer != item['lexer']:
        item['html'] = highlight(item['raw'], lexer)[0]

    return template('show', item=item, owner=owner, lexer=lexer,
                    lexers=lexerlist(), date=fromepoch(item.get('date', 0)))


@route('/:id/raw/')
def show_raw(id):
    try:
        item = store[int(id)]
    except (ValueError, KeyError):
        return redirect('/', 302)

    ctype = request.GET.get('as', 'text/plain')
    response.content_type = '%s; charset=utf-8' % ctype
    return item['raw'].encode('utf-8')


@route('/:id/edit/')
@route('/:id/edit/', method='POST')
def edit(id):
    try:
        item = store[int(id)]
    except (ValueError, KeyError):
        return redirect('/', 302)

    owner = bool(request.get_cookie('edit-%s' % id, secret=SECRET))
    if not owner:
        return redirect('/%s/' % id, 302)

    if request.method == 'POST':
        data = dec(request.POST.get('data'))
        lexer = request.POST.get('lexer', 'guess')
        paste(item, data, lexer)
        return redirect('/%s/' % id, 302)

    return template('index', data=item['raw'], id=id,
                    deflexer=item['lexer'], lexers=lexerlist())


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
