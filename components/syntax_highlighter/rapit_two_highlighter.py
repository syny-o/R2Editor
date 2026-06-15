from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter


def format(color, style='', background_color = None):
# Return a QTextCharFormat with the given attributes.
    _color = QColor()
    _color.setNamedColor(color)

    _background_color = QColor()
    _background_color.setNamedColor(background_color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)
    if 'italicbold' in style:
        _format.setFontItalic(True)
        _format.setFontWeight(QFont.Bold)

    if background_color:
        _format.setBackground(_background_color)
    return _format




STYLES_DARK_MODE = {
    'keyword': format('#ff0040'),
    'keyword_primary': format('#fff', 'bold'),
    'keyword_secondary': format('violet'),
    'keyword_if': format('#2dbdd6', 'bold'),
    'keyword_for': format('violet', 'bold'),
    'pbc_variables': format('grey', 'italic'),
    # 'comment': format('#00ffff', 'italic'),
    'comment': format('#777', 'italic'),
    'string': format('#00ff80'),
    'numbers': format('#00ffff'),
    'values': format('#C82C2C'),
    'operator': format('orange'),
    'brace': format('#C82C2C'),

    'angle_keyword': format('#ffaa00'),
    'quoted_keyword': format('#00ffaa'),    



}

STYLES_LIGHT_MODE = {
    'keyword': format('#ff0040', 'bold'),
    'keyword_primary': format('#fff', 'bold', '#e30e0e'),
    'keyword_secondary': format('brown', 'bold'),
    'keyword_if': format('#2dbdd6', 'bold'),
    'keyword_for': format('#e3a736', 'bold'),
    'pbc_variables': format('grey', 'italic'),
    # 'comment': format('#00ffff', 'italic'),
    'comment': format('#777', 'italic'),
    'string': format('green'),
    'numbers': format('blue'),
    'values': format('#C82C2C'),
    'operator': format('black'),
    'brace': format('#C82C2C'),

    'angle_keyword': format('#cc8800'),
    'quoted_keyword': format('#008855'),
}


class RapitTwoHighlighter(QSyntaxHighlighter):

    keywords = [
        'TEST.NEW', 'TEST.END', 'TEST.SUBPROGRAM', 'TEST.SCRIPT_FEATURE',
    ]

    keywords_primary = [
        'TEST.NAME',
    ]

    keywords_secondary = [
        'TEST.SLOT', 'TEST.REQUIREMENT_KEY',
    ]

    keywords_if = [
        'IF', 'ELSE', 'ELSE IF','ENDIF', 'THEN', 'If', 'Else', 'Endif', 'Then', 'OR', 'or', 'Or', 'AND', 'and', 'And', 'if', 'else', 'endif'
    ]

    keywords_for = [
        'FOR', 'DO', 'NEXT', 'For', 'Do', 'Next'
    ]


    # Operators
    operators = [
        '=',
        # Comparison
        '==', '!=', '<', '<=', '>', '>=',
        # Arithmetic
        '\+', '-', '\*', '/', '//', '\%', '\*\*',
        # In-place
        '\+=', '-=', '\*=', '/=', '\%=',
        # Bitwise
        '\^', '\|', '\&', '\~', '>>', '<<',

        '\$',
    ]

    # Braces
    braces = [
        '\{', '\}', '\(', '\)', '\[', '\]',
    ]

    def __init__(self, document, dark_mode = True):
        QSyntaxHighlighter.__init__(self, document)


        if dark_mode:
            STYLES = STYLES_DARK_MODE
        else:
            STYLES = STYLES_LIGHT_MODE


        rules = []

        # --- HLAVNÍ KLÍČOVÁ SLOVA ---
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
            for w in RapitTwoHighlighter.keywords]

        rules += [(r'\b%s\b' % s, 0, STYLES['keyword_primary'])
            for s in RapitTwoHighlighter.keywords_primary]

        rules += [(r'\b%s\b' % t, 0, STYLES['keyword_secondary'])
            for t in RapitTwoHighlighter.keywords_secondary]

        rules += [(r'\b%s\b' % i, 0, STYLES['keyword_if'])
            for i in RapitTwoHighlighter.keywords_if]

        rules += [(r'\b%s\b' % f, 0, STYLES['keyword_for'])
            for f in RapitTwoHighlighter.keywords_for]


        # --- STRUKTURA SCRIPTU ---
        rules += [
            (r'--\s*COMPOUND TESTS', 0, STYLES['keyword_for']),
            (r'^\s*TEST\.NAME:.*', 0, STYLES['keyword_primary']),
            (r'^\s*TEST\.SLOT:.*', 0, STYLES['keyword_secondary']),
            (r'^\s*TEST\.REQUIREMENT_KEY:.*', 0, STYLES['keyword_if']),
            (r'TEST\.[A-Z_]+:', 0, STYLES['keyword']),
        ]


        # ✅ --- SLOT FORMÁTOVÁNÍ (KLÍČOVÁ ČÁST) ---

        rules += [

            # --- "<<KEYWORD>>" uvnitř uvozovek ---
            (r'(?<=")<<[^<>]+>>(?=")', 0, STYLES['angle_keyword']),

            # --- obsah stringu (bez << >>) ---
            (r'(?<=")[^"<>\n,]+(?=")', 0, STYLES['quoted_keyword']),

            # --- čísla uvnitř uvozovek ---
            (r'(?<=")\d+(?=")', 0, STYLES['numbers']),

            # --- uvozovky ---
            (r'"', 0, format('#ffffff')),

            # --- čárky ---
            (r',', 0, format('#ffffff')),
        ]


        # --- DALŠÍ ČITELNOST ---
        rules += [

            # čísla
            # (r'\b[0-9]+\b', 0, STYLES['numbers']),
            (r'(?<=")\d+(?=")', 0, STYLES['numbers']),

            # komentáře
            (r'--[^\n]*', 0, STYLES["comment"]),
        ]


        # Build regex
        self.rules = [(QRegExp(pat), index, fmt)
            for (pat, index, fmt) in rules]


    def highlightBlock(self, text):

    # Apply syntax highlighting to the given block of text.

        # Do other syntax formatting
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)

        self.setCurrentBlockState(0)

