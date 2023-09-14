import sys
from PyQt5.QtWidgets import QTextEdit, QApplication, QMainWindow, QToolTip
from PyQt5.QtGui import QTextCursor
from PyQt5.QtCore import Qt


tooltips = {'Hello': ('Tooltip for Hello' * 2 + '\n') * 100 }


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.text_edit = MyTextEdit("Hello")
        self.setCentralWidget(self.text_edit)
        self.resize(800, 600)

class MyTextEdit(QTextEdit):
    def __init__(self, text):
        super().__init__(text)    
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):

        if QToolTip.isVisible():
            print("Prdel")
            return

        tc = self.textCursor()
        
        tc_temp = self.cursorForPosition(event.pos())
        tc_temp.select(QTextCursor.WordUnderCursor)
        word = tc_temp.selectedText()
        
        if word in tooltips:
            self.show_tooltip(tooltips[word])
        else:
            QToolTip.hideText()

        self.setTextCursor(tc)
        
        super().mouseMoveEvent(event)


    def show_tooltip(self, tooltip_text):
        if tooltips:
            pos = self.cursorRect(self.textCursor()).bottomRight()
            pos = self.mapToGlobal(pos)
            
            QToolTip.showText(pos, tooltip_text)        


app = QApplication(sys.argv)
win = MainWindow()
win.show()
app.exec_()