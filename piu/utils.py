import StringIO
from datetime import datetime as dt
from pygments import lexers, formatters, highlight as highlight_

def key(format, *args):
    return 'piu:' + format % args

def dec(s):
    return s.decode('utf-8')

def toepoch(dt):
    return dt.strftime('%s')

def fromepoch(s):
    return dt.fromtimestamp(int(s))

def highlight(code, lexer='guess', formatter='codehtml'):
    try:
        if lexer == 'guess':
            lexer = lexers.guess_lexer(code)
        else:
            lexer = lexers.get_lexer_by_name(lexer)
    except lexers.ClassNotFound:
        lexer = lexers.get_lexer_by_name('text')

    formatter = CodeHtmlFormatter(
        linenos='table', anchorlinenos=True, lineanchors='l')

    return highlight_(code, lexer, formatter), lexer.aliases[0]

def style():
    f = formatters.HtmlFormatter()
    return f.get_style_defs('.code')

def lexerlist():
    lst = sorted(list(lexers.get_all_lexers()))
    for name, alias, _, _ in lst:
        yield alias[0], name


class CodeHtmlFormatter(formatters.HtmlFormatter):
    def _wrap_lineanchors(self, inner):
        s = self.lineanchors
        i = 0
        for t, line in inner:
            if t == 1:
                i += 1
                yield t, '<div class="line" id="%s-%d">%s</div>' % (s, i, line)
            else:
                yield t, line
