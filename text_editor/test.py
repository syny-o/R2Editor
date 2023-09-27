import sys
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit


def get_word_under_cursor(text_cursor):
    is_end_of_word = False
    is_start_of_word = False
    
    text_cursor.select(QTextCursor.WordUnderCursor)    
    while not is_end_of_word:
        if text_cursor.atEnd() or text_cursor.atBlockEnd():
            is_end_of_word = True
        
        text_cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)

        if text_cursor.atEnd() or text_cursor.atBlockEnd():
            is_end_of_word = True

        if text_cursor.selectedText().endswith((" ", "\n", "\t", "=", ",", '"')):
            is_end_of_word = True
            text_cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor)
            
            break

    text_cursor.clearSelection()

    while not is_start_of_word:
        if text_cursor.atStart() or text_cursor.atBlockStart():
            is_start_of_word = True
        
        
        text_cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor)

        if text_cursor.atStart() or text_cursor.atBlockStart():
            is_start_of_word = True

        if text_cursor.selectedText().startswith((" ", "\n", "\t", "=", ",", '"')):
            is_start_of_word = True
            text_cursor.movePosition(QTextCursor.NextCharacter, QTextCursor.KeepAnchor)
            break

    return text_cursor.selectedText()


class MyTextEdit(QTextEdit):
    def mouseMoveEvent(self, event):
        text_cursor = self.cursorForPosition(event.pos())

        text = get_word_under_cursor(text_cursor)

        print(text)

        super().mouseMoveEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        te = MyTextEdit("PbcIn.ApplyReleaseRequest.Debug \n Ahoj")
        # Set the central widget of the Window.
        self.setCentralWidget(te)


app = QApplication(sys.argv)


window = MainWindow()
window.show()
app.exec_()