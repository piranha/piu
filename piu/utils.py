import StringIO
from datetime import datetime as dt

from pygments import lexers, formatters, highlight as highlight_

import piu.ansi2html as _ansi2html


def dec(s):
    return s.decode('utf-8')


def toepoch(dt):
    return dt.strftime('%s')


def fromepoch(s):
    return dt.fromtimestamp(int(s))


def highlight(code, lexer=None):
    if lexer == 'ansi':
        return ansi2html(code), 'ansi'

    if lexer == None:
        lexer = lexers.guess_lexer(code)
    else:
        try:
            lexer = lexers.get_lexer_by_name(lexer)
        except lexers.ClassNotFound:
            lexer = lexers.get_lexer_by_name('text')

    formatter = CodeHtmlFormatter()

    return highlight_(code, lexer, formatter), lexer.aliases[0]


def style():
    f = formatters.HtmlFormatter()
    return f.get_style_defs('.code')


def lexerlist(with_fnames=False):
    lst = list(lexers.get_all_lexers())
    lst.append(('ANSI', ['ansi'], [], None))
    for name, aliases, fnames, _ in sorted(lst, key=lambda x: x[0].lower()):
        if with_fnames:
            yield aliases, fnames
        else:
            yield aliases[0], name


def linenos(linecount):
    lines = []
    for i in range(1, 1 + linecount):
        lines.append('<a rel="%d" id="a-%d">%d</a>' % (i, i, i))
    return ''.join(lines) # no newline so they can be displayed as blocks


def ansi2html(text):
    result = _ansi2html.ansi2html(text)
    return ('<table class="highlighttable"><tr>'
            '<td><pre class="linenos">%s</pre></td>'
            '<td class="code"><div class="highlight"><pre>%s</pre></div></td>'
            '</tr></table>') % (linenos(result.count('<div')), result)


class CodeHtmlFormatter(formatters.HtmlFormatter):
    def __init__(self, **kwargs):
        kwargs.update({'linenos': 'table',
                       'anchorlinenos': True,
                       'lineanchors': True})
        super(CodeHtmlFormatter, self).__init__(**kwargs)

    def _wrap_lineanchors(self, inner):
        i = 0
        for t, line in inner:
            if t == 1:
                i += 1
                yield t, '<div class="line" id="%s">%s</div>' % (i, (line or '&#13;'))
            else:
                yield t, line

    def _wrap_tablelinenos(self, inner):
        dummyoutfile = StringIO.StringIO()
        lncount = 0
        for t, line in inner:
            if t:
                lncount += 1
            dummyoutfile.write(line)

        # in case you wonder about the seemingly redundant <div> here: since the
        # content in the other cell also is wrapped in a div, some browsers in
        # some configurations seem to mess up the formatting...
        yield 0, ('<table class="%stable">' % self.cssclass +
                  '<tr><td><pre class="linenos">' +
                  linenos(lncount) + '</pre></td><td class="code">')
        yield 0, dummyoutfile.getvalue()
        yield 0, '</td></tr></table>'
