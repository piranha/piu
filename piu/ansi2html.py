"""
Code inspired by https://github.com/lambdaisland/ansi
"""
import re

def t(s):
    return tuple(s.split())

# https://en.wikipedia.org/wiki/ANSI_escape_code#3/4_bit
COLORS = {
    0: t('  0   0   0'),
    1: t('194  54  33'),
    2: t(' 37 188  36'),
    3: t('173 173  39'),
    4: t(' 73  46 225'),
    5: t('211  56 211'),
    6: t(' 51 187 200'),
    7: t('203 204 205'),
}

BRIGHT = {
    0: t('129 131 131'),
    1: t('252  57  31'),
    2: t(' 49 231  34'),
    3: t('234 236  35'),
    4: t(' 88  51 255'),
    5: t('249  53 248'),
    6: t(' 20 240 240'),
    7: t('233 235 235'),
}


COLOR_RE = re.compile('\033\\[([^m]+)m')
BOLD = 'font-weight: bolder'


def color(n):
    if 30 <= n <= 37:
        return 'color: rgb(%s, %s, %s)' % COLORS[n - 30]
    if n == 39: # default foreground
        return 'color: inherit'
    if 40 <= n <= 47:
        return 'background-color: rgb(%s, %s, %s)' % COLORS[n - 40]
    if n == 49: # default background
        return 'background-color: inherit'
    if 90 <= n <= 97: # bright foreground
        return 'color: rgb(%s, %s, %s)' % BRIGHT[n - 90]
    if 100 <= n <= 107: # bright foreground
        return 'background-color: rgb(%s, %s, %s)' % BRIGHT[n - 100]


def ansi2html(text):
    def sub(match):
        codes = map(int, match.group(1).split(';'))

        attrs = []
        for code in codes:
            if code == 0:
                return '</span>'
            elif code == 1:
                attrs.append(BOLD)
            else:
                attrs.append(color(code))

        return '<span style="%s">' % ';'.join(attrs)

    result = COLOR_RE.sub(sub, text)
    return ''.join(
        '<div class="line" id="%s">%s</div>' % (i + 1, (item or '&#13;'))
        for i, item in enumerate(result.splitlines()))
