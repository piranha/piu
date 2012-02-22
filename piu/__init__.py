import sys
import os.path as op

from opster import command
import bottle
from bottle import run, default_app, debug as debug_

import fstore

bottle.TEMPLATE_PATH = [op.join(op.dirname(__file__), 'templates')]
store = None

@command(usage='[OPTS]')
def main(address    = ('a', 'localhost', 'ip address (host) to bind'),
         port       = ('p', 8080, 'port to use'),
         reloader   = ('r', False, 'use reloader'),
         debug      = ('d', False, 'enable debug'),
         path       = ('', 'store', 'path to store'),
         regenerate = ('', False, 'regenerate *:html in database')):
    '''paste.in.ua
    '''
    global store
    store = fstore.FStore(path, create=True)

    # import views to register them
    import views

    if regenerate:
        views.regenerate()
        sys.exit()

    app = default_app()
    if debug:
        debug_()
    sys.exit(run(app=app, host=address, port=port, reloader=reloader,
                 server='tornado'))

if __name__ == '__main__':
    main.command()
