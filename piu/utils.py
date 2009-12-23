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

    def _wrap_tablelinenos(self, inner):
        dummyoutfile = StringIO.StringIO()
        lncount = 0
        for t, line in inner:
            if t:
                lncount += 1
            dummyoutfile.write(line)

        fl = self.linenostart
        mw = len(str(lncount + fl - 1))
        sp = self.linenospecial
        st = self.linenostep
        la = self.lineanchors
        aln = self.anchorlinenos
        if sp:
            lines = []

            for i in range(fl, fl+lncount):
                if i % st == 0:
                    if i % sp == 0:
                        if aln:
                            lines.append('<a href="#%s-%d" class="special">%*d</a>' %
                                         (la, i, mw, i))
                        else:
                            lines.append('<span class="special">%*d</span>' % (mw, i))
                    else:
                        if aln:
                            lines.append('<a href="#%s-%d">%*d</a>' % (la, i, mw, i))
                        else:
                            lines.append('%*d' % (mw, i))
                else:
                    lines.append('')
            ls = '\n'.join(lines)
        else:
            lines = []
            for i in range(fl, fl+lncount):
                if i % st == 0:
                    if aln:
                        lines.append('<a href="#%s-%d">%*d</a>' % (la, i, mw, i))
                    else:
                        lines.append('%*d' % (mw, i))
                else:
                    lines.append('')
            ls = ''.join(lines)

        # in case you wonder about the seemingly redundant <div> here: since the
        # content in the other cell also is wrapped in a div, some browsers in
        # some configurations seem to mess up the formatting...
        yield 0, ('<table class="%stable">' % self.cssclass +
                  '<tr><td class="linenos"><div class="linenodiv">' +
                  ls + '</div></td><td class="code">')
        yield 0, dummyoutfile.getvalue()
        yield 0, '</td></tr></table>'
