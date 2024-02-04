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
    'keyword': format('#ff0040', 'bold'),
    'keyword_primary': format('#fff', 'bold', '#e30e0e'),
    'keyword_secondary': format('orange', 'bold'),
    'keyword_if': format('#2dbdd6', 'bold'),
    'keyword_for': format('#e3a736', 'bold'),
    'pbc_variables': format('grey', 'italic'),
    # 'comment': format('#00ffff', 'italic'),
    'comment': format('#777', 'italic'),
    'string': format('#00ff80'),
    'numbers': format('#00ffff'),
    'values': format('#C82C2C'),
    'operator': format('orange'),
    'brace': format('#C82C2C'),



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
    'string': format('#dd2222'),
    'numbers': format('blue'),
    'values': format('#C82C2C'),
    'operator': format('black'),
    'brace': format('#C82C2C'),
}


class RapitTwoHighlighter(QSyntaxHighlighter):

    # RapitTwo keywords
    keywords = [
        'EXPECTEDRESULT', 'COM',

    ]

    keywords_primary = [
        'TESTCASE', 'CHAPTER', 'END CHAPTER', 'Testcase',
    ]

    keywords_secondary = [
        'HIL', 'PRE', 'SEV', 'REF','REMARK',
    ]

    keywords_if = [
        'IF', 'ELSE', 'ELSE IF','ENDIF', 'THEN', 'If', 'Else', 'Endif', 'Then', 'OR', 'or', 'Or', 'AND', 'and', 'And',
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

        # Keyword, operator, and brace rules
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
        rules += [(r'%s' % o, 0, STYLES['operator'])
            for o in RapitTwoHighlighter.operators]
        rules += [(r'%s' % b, 0, STYLES['brace'])
            for b in RapitTwoHighlighter.braces]

        # All other rules
        rules += [
            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),

            # Double-quoted string, possibly containing escape sequences ### "\"([^\"]*)\"" ### "\"(\\w)*\""
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),

            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),

            # From "'" until a newline
            (r"'[^\n]*", 0, STYLES["comment"]),

            # Pbc
            #(r"[A-Za-z]*Pbc[a-zA-Z]*", 0, STYLES["pbc_variables"]),

            # Value after '='
            #(r"=[^\n]*", 0, STYLES["values"]),

        ]

        # Build a QRegExp for each pattern
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

