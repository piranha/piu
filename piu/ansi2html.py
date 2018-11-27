import re

COLOR_DICT = {
     '2': [(160, 160, 160), (128,   0,   0)],
    '30': [(  0,   0,   0), (128,   0,   0)],
    '31': [(160,   0,   0), (128,   0,   0)],
    '32': [(  0, 160,   0), (  0, 128,   0)],
    '33': [(160, 160,   0), (128, 128,   0)],
    '34': [(  0,   0, 160), (  0,   0, 128)],
    '35': [(160,   0, 160), (128,   0, 128)],
    '36': [(  0, 160, 160), (  0, 128, 128)],
    '37': [(160, 160, 160), (160, 160, 160)],
}

COLOR_REGEX = re.compile(r'\[(?P<a1>\d+)(;(?P<a2>\d+)(;(?P<a3>\d+))?)?m')

BOLD = 'font-weight: bolder'
COLOR = 'color: rgb%s'
TEMPLATE = '<span style="%s">'

def ansi2html(text):
    text = text.replace('[m', '</span>').replace('[0m', '</span>')

    def single_sub(match):
        args = match.groupdict()
        a1, a2, a3 = args['a1'], args['a2'], args['a3']
        bold = '1' in [a1, a2, a3]
        color = COLOR_DICT.get(a1) or COLOR_DICT.get(a2) or COLOR_DICT.get(a3)

        styles = []
        if bold:
            styles.append(BOLD)
        if color:
            styles.append(COLOR % (color[bold], ))
        return TEMPLATE % (';'.join(styles))

    result = COLOR_REGEX.sub(single_sub, text)
    return ''.join(
        '<div class="line" id="%s">%s</div>' % (i + 1, (item or '&#13;'))
        for i, item in enumerate(result.splitlines()))
