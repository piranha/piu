from pygments import lexers, formatters, highlight as highlight_

def key(format, *args):
    return 'piu:' + format % args

def dec(s):
    return s.decode('utf-8')

OPTIONS = {'html': {'linenos': 'table'}}

def highlight(code, lexer='guess', formatter='html'):
    try:
        if lexer == 'guess':
            lexer = lexers.guess_lexer(code)
        else:
            lexer = lexers.get_lexer_by_name(lexer)
    except lexers.ClassNotFound:
        lexer = lexers.get_lexer_by_name('text')

    try:
        formatter = formatters.get_formatter_by_name(
            formatter, **OPTIONS.get(formatter, {}))
    except formatters.ClassNotFound:
        formatter = formatters.NullFormatter()

    return highlight_(code, lexer, formatter), lexer.name.lower()

def style():
    f = formatters.HtmlFormatter()
    return f.get_style_defs('.code')

def lexerlist():
    lst = sorted(list(lexers.get_all_lexers()))
    for name, alias, _, _ in lst:
        yield alias[0], name
