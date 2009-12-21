{# -*- mode: python -*- #}#!/usr/bin/env python

from optparse import OptionParser
from fnmatch import fnmatch
import os, sys, urllib

LEXERS = {{ lexers }}
URI = 'http://paste.in.ua/'

def paste(data, lexer):
    post = {'data': data, 'lexer': lexer}
    return urllib.urlopen(URI, urllib.urlencode(post)).url

def findlexer(fn, default):
    fn = os.path.basename(fn)
    for pat, lexer in LEXERS.items():
        if fnmatch(fn, pat):
            return lexer
    return default

def result(url):
    print url
    utils = 'xclip pbcopy'.split()
    for util in utils:
        {# #}# not because 0 is success
        if not os.system('which %s > /dev/null 2>&1' % util):
            os.system('printf %s | %s' % (url, util))
            print 'url copied to clipboard using %s' % util

def print_lexers(*args, **kwargs):
    print '\n'.join(sorted(list(set(LEXERS.values()))))
    sys.exit()

def main():
    usage = 'usage: cat file | %prog  or  %prog file'
    parser = OptionParser(usage)
    parser.add_option('-t', '--type', type='string', default='',
                      help='input file type')
    parser.add_option('', '--types', action='callback', callback=print_lexers,
                      help='print available file types')
    opts, args = parser.parse_args()

    if not len(args):
        {# #}# is not a tty - we have data in stdin awaiting
        if not sys.stdin.isatty():
            data = sys.stdin.read()
        else:
            sys.exit(parser.print_help())
        lexer = opts.type
    else:
        data = file(args[0]).read()
        lexer = opts.type or findlexer(args[0], 'text')

    if lexer not in LEXERS.values():
        print 'abort: %s is not a valid file type' % lexer
        sys.exit(1)

    result(paste(data, lexer))

if __name__ == '__main__':
    main()
