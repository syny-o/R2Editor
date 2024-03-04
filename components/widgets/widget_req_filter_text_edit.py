import sys

from PyQt5.QtWidgets import QCompleter, QTextEdit, QGridLayout, QWidget, QApplication, QTextEdit
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QTextCursor


columns = ["102_Reference", "Object Text", "Object Text_DXL", "Objet Type"]


class Completer(QCompleter):

    # Custom signal definition
    insert_text = pyqtSignal(str)

    def __init__(self, parent = None):
        super().__init__(parent)

        # Completer configuration
        self.setCompletionMode(QCompleter.PopupCompletion)
        # self.setCaseSensitivity(Qt.CaseInsensitive)
        # self.popup = self.popup()


        # Built-in signal -->  signal is sent when an item in the popup() is highlighted by the user
        self.highlighted.connect(self.set_highlighted)

    def set_highlighted(self, text):
        self.last_selected = text


    def get_selected(self):
        return self.last_selected
    




class RequirementFilterTextEdit(QTextEdit):
    def __init__(self, completions: list = []):
        super().__init__()

        self.completer = Completer(completions)
        self.completer.setWidget(self)
        self.completer.insert_text.connect(self.insert_completion)
        self.setPlaceholderText("Press 'Alt' to get suggestions")




    def insert_completion(self, completion):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.StartOfWord, QTextCursor.KeepAnchor)
        cursor.insertText(completion)
        self.setTextCursor(cursor)



    def keyPressEvent(self, event):
        if self.completer.popup().isVisible():
            if event.key() in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Escape):
                event.ignore()
                self.completer.popup().hide()
                return
            
            if event.key() == Qt.Key_Return:
                self.completer.insert_text.emit(self.completer.get_selected())
                self.completer.popup().hide()
                return
            
        if event.key() == Qt.Key_Escape:
            event.ignore()
            return
        
        if event.key() == Qt.Key_Alt:
            cursor = self.textCursor()
            cursor.select(QTextCursor.WordUnderCursor)
            completion_prefix = cursor.selectedText()
            # print(f"--{completion_prefix}--")
            if completion_prefix is not None:
                # if len(completion_prefix) > 0:
                    self.completer.setCompletionPrefix(completion_prefix)
                    popup = self.completer.popup()
                    popup.setCurrentIndex(self.completer.completionModel().index(0, 0))
                    cr = self.cursorRect()
                    cr.setWidth(self.completer.popup().sizeHintForColumn(0) + self.completer.popup().verticalScrollBar().sizeHint().width())
                    self.completer.complete(cr)
                # else:
                #     self.completer.popup().hide()            
        
            
        super().keyPressEvent(event)









# class Window(QWidget):
#     def __init__(self):
#         QWidget.__init__(self)
#         layout = QGridLayout()
#         self.setLayout(layout)


#         # create line edit and add auto complete                                
#         self.requirement_filter_text_edit = RequirementFilterTextEdit(columns)
#         layout.addWidget(self.requirement_filter_text_edit, 0, 0)



# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     screen = Window()
#     screen.show()
#     sys.exit(app.exec_())            

