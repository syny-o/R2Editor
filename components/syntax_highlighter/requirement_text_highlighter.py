

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



color_keyword_primary = ("#000000")

STYLES_LIGHT = {
    'keyword': format('red', 'bold'),
    'pbc_variables': format('blue', ''),
    'comment': format('#777', 'italic'),
    'string': format('green', ''),
    'numbers': format('#00ffff'),
    'values': format('#C82C2C'),
    'operator': format('black', ''),
    'brace': format('black', ''),
    'COLUMNS': format('black', 'bold'),
    'TEXT_HEADINGS': format('green', 'bold'),

}


STYLES_DARK = {
    'keyword': format('#fa8ca6', 'bold'),
    'keyword': format('#ffb8f0', 'bold'),
    # 'keyword': format('#cbb9fa', 'bold'),

    'pbc_variables': format('#DDD', 'bold'),
    'pbc_variables': format('#fff9a3', ''),


    #7cfc93
    # 'comment': format('#00ffff', 'italic'),
    'comment': format('#777', 'italic'),
    'string': format('#f2cc8f', ''),
    'string': format('#fff9a3', ''),


    'numbers': format('#00ffff'),
    'values': format('#C82C2C'),
    'operator': format('white', ''),
    'brace': format('white', ''),
    'COLUMNS': format('#00bbff'),
    'TEXT_HEADINGS': format('#DDD', 'bold'),

}


class RequirementTextHighlighter(QSyntaxHighlighter):

    # RapitTwo keywords
    keywords = [
        'IF', 'ELSE', 'ELSE IF','ENDIF', 'THEN', 'OR', 'AND', 'NOT',

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
            STYLES = STYLES_DARK
        else:
            STYLES = STYLES_LIGHT

        rules = []

        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, STYLES['keyword'])
            for w in RequirementTextHighlighter.keywords]                      
        rules += [(r'%s' % o, 0, STYLES['operator'])
            for o in RequirementTextHighlighter.operators]
        rules += [(r'%s' % b, 0, STYLES['brace'])
            for b in RequirementTextHighlighter.braces]

        # All other rules
        rules += [
            # Numeric literals
            # (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
            # (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
            # (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),

            # Double-quoted string, possibly containing escape sequences ### "\"([^\"]*)\"" ### "\"(\\w)*\""
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),

            # Single-quoted string, possibly containing escape sequences
            # (r"'[^'\\]*(\\.[^'\\]*)*\S'", 0, STYLES['string']),
            (r"'[^\s]+'", 0, STYLES['string']),

            # COLUMNS NAMES
            (r"^<[\w\s\n/-]+>:$", 0, STYLES["COLUMNS"]),

            # Small headings in Object Text
            (r"^[\w\s]+:$", 0, STYLES["TEXT_HEADINGS"]),

            # Pbc
            (r"(Hsb|SsmPb|Pbc)(In|Out)[a-zA-Z0-9\n]+", 0, STYLES["pbc_variables"]),

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