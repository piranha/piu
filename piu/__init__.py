import sys
import os.path as op

from opster import command
import bottle
from bottle import run, default_app, CherryPyServer
from redis import Redis, ConnectionError

bottle.TEMPLATE_PATH = [op.join(op.dirname(__file__), 'templates')]
redis = None

def pathmw(app):
    def mw(e, sr):
        path = e['PATH_INFO']
        method = e['REQUEST_METHOD']
        if (not app.match_url(path, method)[0] and
            not path.endswith('/') and
            app.match_url(path + '/', method)[0]):
            sr('301 Moved Permanently', [('Location', path + '/')])
            return ''
        return app(e, sr)
    return mw

@command(usage='[OPTS]')
def main(address    = ('a', 'localhost', 'ip address (host) to bind'),
         port       = ('p', 8080, 'port to use'),
         reloader   = ('r', False, 'use reloader'),
         debug      = ('d', False, 'enable debug'),
         redis_host = ('', 'localhost', 'host of redis'),
         redis_port = ('', 6379, 'port of redis'),
         db         = ('', 8, 'redis db number')):
    '''paste.in.ua
    '''
    try:
        global redis
        redis = Redis(host=redis_host, port=redis_port, db=db)
        redis.connect()
    except ConnectionError, e:
        sys.stderr.write('redis: %s\n' % e)
        sys.exit(1)

    # import views to register them
    import views

    kwargs = not debug and {'server': CherryPyServer} or {}
    app = pathmw(default_app())
    sys.exit(run(app=app, host=address, port=port, reloader=reloader,
                 debug=debug, **kwargs))

if __name__ == '__main__':
    main()
