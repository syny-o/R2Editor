from PyQt5.QtWidgets import QCompleter, QStyledItemDelegate, QStyleOptionViewItem
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QModelIndex, QRectF, QSize, QTimer
from PyQt5.QtGui import QFont, QKeyEvent

mono_font = QFont('Courier')


class Completer(QCompleter):


#################### DATA 4 TEXT EDITOR #########################


    cond_dict = {}
    cond_model = None
    a2l_model = None
    dspace_model = None

    cond_tooltips = {}



#################################################################

    # Custom signal definition
    insert_text = pyqtSignal(str)

    def __init__(self, parent = None):
        super().__init__(parent)

        # Completer configuration
        self.setCompletionMode(QCompleter.PopupCompletion)
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setFilterMode(Qt.MatchContains)
        # self.setCompletionRole(Qt.ToolTipRole)

        # self.popup = self.popup()
        self.popup().setFont(mono_font)

        self.setMaxVisibleItems(15)

        # Built-in signal -->  signal is sent when an item in the popup() is highlighted by the user
        self.highlighted.connect(self.set_highlighted)

        self.completer_tooltip = CompleterTextEdit(self)



    def set_highlighted(self, text):
        self.last_selected = text
        # self.completer_tooltip.show_tooltip(text)
        


    def get_selected(self):
        return self.last_selected
    

    

    

    







from PyQt5.QtWidgets import QApplication, QTextEdit, QCompleter, QVBoxLayout, QWidget
from PyQt5.QtGui import QMouseEvent, QTextCursor, QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt5.QtCore import Qt, QEvent, QPoint, QSize, QRegExp







class CompleterTextEdit(QTextEdit):
    def __init__(self, completer, parent=None):
        super(CompleterTextEdit, self).__init__(parent)
        self.completer = completer
        self.tooltip = QTextEdit()
        self.tooltip.setWindowFlags(Qt.ToolTip)
        self.tooltip.setReadOnly(True)
        self.completer.highlighted[str].connect(self.show_tooltip)






    def show_tooltip(self, completion):
        text = None
        model = self.completer.model()
        for i in range(model.rowCount()):
            item = model.item(i)
            if item.text() == completion:
                data = item.data(Qt.UserRole)
                if data:
                    text = '\n'.join(data)
                break

        
        if not text:
            return


        
        self.tooltip.setText(text)
        
        # self.tooltip.move(self.completer.popup().mapToGlobal(QPoint(self.completer.popup().width(), 0)))
        # self.tooltip.show()
        QTimer.singleShot(0, self.position_tooltip)


    def position_tooltip(self):
        self.tooltip.move(self.completer.popup().mapToGlobal(QPoint(self.completer.popup().width(), 0)))
        self.tooltip.show()   


    def hide_tooltip(self):
        self.tooltip.hide() 
                   







