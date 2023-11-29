from PyQt5.QtWidgets import QTextEdit, QToolTip, QWhatsThis, QWidget, QApplication, QVBoxLayout, QPushButton, QToolBar, QDesktopWidget, QSizePolicy
from PyQt5.QtGui import QTextCursor, QScreen, QIcon
from PyQt5.QtCore import Qt, QTimer


from data_manager.tooltips_req import tooltips_req as tooltips
# from config.font import font


from PyQt5.QtGui import QFont

font = QFont("Monospace", 30, QFont.Monospace)
font.setFamily("Monaco")
font.setLetterSpacing(QFont.AbsoluteSpacing, 1.3)
font.setStyle(QFont.StyleNormal)
font.setWeight(QFont.Normal)



class RequirementTextEdit(QTextEdit):

    tooltip_size = None

    selected_word = None

    widgets = []


    def __init__(self, main_window):
        super().__init__()
        self.scroll_bar = self.verticalScrollBar()
        self.main_window = main_window
        # self.main_window = data_manager.main_window
        self.setReadOnly(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.highlighter = RequirementTextHighlighter(self.document())
        self.setFont(font)
        self.setStyleSheet("font-size: 16px;")

    
    def mouseMoveEvent(self, event):

        # SAVE CURRENT SCROLLBAR POSITION
        scroll_pos = self.scroll_bar.value()
        # CREATE INSTANCE OF TEXT CURSOR
        tc = self.textCursor()
        # IF THERE IS NO SELECTED TEXT
        if tc.selectedText() == '':
            tc_original_pos = tc.position()
            textCursor = self.cursorForPosition(event.pos())
            textCursor.select(QTextCursor.WordUnderCursor)
            self.setTextCursor(textCursor)
            word = textCursor.selectedText()
            if word in tooltips:
                # self.show_tooltip(tooltips[word])
                self.viewport().setCursor(Qt.PointingHandCursor)
                RequirementTextEdit.selected_word = word
            else:
                # QToolTip.hideText()
                self.viewport().setCursor(Qt.ArrowCursor)
                RequirementTextEdit.selected_word = None
            # SET BACK THE TEXT CURSOR POSITION AND SCROLLBAR POSITION
            tc.setPosition(tc_original_pos)
            self.setTextCursor(tc)
            self.scroll_bar.setValue(scroll_pos)


        super().mouseMoveEvent(event)


    def mouseReleaseEvent(self, event):
        if RequirementTextEdit.selected_word:
            self.show_tooltip(tooltips[RequirementTextEdit.selected_word])

        return super().mouseReleaseEvent(event)


    def show_tooltip(self, tooltip_text):
        if tooltips:            
            self.w = MyWidget(self.main_window, tooltip_text)



class MyWidget(QWidget):
    def __init__(self, main_window, text):
        super().__init__()

        self.main_window = main_window

        RequirementTextEdit.widgets.append(self)
        # print(len(RequirementTextEdit.widgets))

        if len(RequirementTextEdit.widgets) == 1:
            RequirementTextEdit.tooltip_size = self.calculate_size(text)

        self.setWindowFlags(Qt.Popup)
        
        # self.setWindowOpacity(0.95)
        self.setMaximumSize(1280, 1024)
        self.setMinimumSize(200, 200)

        self.resize(*RequirementTextEdit.tooltip_size)
        

        self.setStyleSheet("color: #edf; background-color: #222; font-size: 14px;")

        btn = QPushButton(QIcon(u"ui/icons/check.png"), "Back")
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(self.close)

        toolbar = QToolBar()
        toolbar.addWidget(btn)


        # self.te = QTextEdit()
        self.te = RequirementTextEdit(self.main_window)
        self.te.setReadOnly(True)
        l = QVBoxLayout()
        l.addWidget(self.te)
        l.addWidget(toolbar)

        l.setSpacing(20)
        l.setContentsMargins(20, 20, 20, 20)
        
        self.setLayout(l)

        self.te.setPlainText(text)
        self.show()    


    def calculate_size(self, text):
        lines = text.splitlines()
        longest_line = 0
        for line in lines:
            if len(line) > longest_line:
                longest_line = len(line)
        return longest_line*10, len(lines) * 30


    def showEvent(self, event):
        if not event.spontaneous() and self.parent:
            geo = self.geometry()
            geo.moveCenter(self.main_window.geometry().center())
            QTimer.singleShot(0, lambda: self.setGeometry(geo))


    def closeEvent(self, e):
        RequirementTextEdit.is_visible = False
        return super().closeEvent(e)


    def closeEvent(self, e):        
        RequirementTextEdit.widgets.remove(self)
        print(len(RequirementTextEdit.widgets))
        return super().closeEvent(e)

















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

STYLES = {
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

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

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
            (r"(Hsb|SsmPb|Pbc)(In|Out)[a-zA-Z\n]+", 0, STYLES["pbc_variables"]),

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



# EPB_Chrysler_MY24_DTSyDesign_4778
