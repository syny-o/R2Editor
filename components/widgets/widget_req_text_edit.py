from PyQt5.QtWidgets import QTextEdit, QToolTip, QWhatsThis, QWidget, QApplication, QVBoxLayout, QPushButton, QToolBar, QDesktopWidget, QSizePolicy
from PyQt5.QtGui import QTextCursor, QScreen, QIcon
from PyQt5.QtCore import Qt, QTimer

from components.syntax_highlighter.requirement_text_highlighter import RequirementTextHighlighter
from config.tooltips_req import tooltips_req as tooltips
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


    def set_text(self, text):
        self.setPlainText(text)
        self.update_syntax_highlighter()


    def update_syntax_highlighter(self):
        dark_mode = self.data_manager.MAIN.app_settings.theme == "Dark"
        self.highlighter = RequirementTextHighlighter(self.document(), dark_mode=dark_mode)


    def __init__(self, data_manager):
        super().__init__()
        self.scroll_bar = self.verticalScrollBar()
        self.data_manager = data_manager
        # self.main_window = data_manager.main_window
        self.setReadOnly(True)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        
        # self.setFont(font)
        self.setStyleSheet("font-size: 13px;")

    
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
            self.w = MyWidget(self.data_manager, tooltip_text)



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
        

        # self.setStyleSheet("color: #edf; background-color: #222; font-size: 14px;")

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



















# EPB_Chrysler_MY24_DTSyDesign_4778
