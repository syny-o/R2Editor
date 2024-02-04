from PyQt5.QtWidgets import QCompleter, QStyledItemDelegate, QStyleOptionViewItem
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QModelIndex, QRectF, QSize
from PyQt5.QtGui import QFont

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
        self.setCompletionRole(Qt.ToolTipRole)

        self.popup = self.popup()
        self.popup.setFont(mono_font)

        self.setMaxVisibleItems(15)

        # Built-in signal -->  signal is sent when an item in the popup() is highlighted by the user
        self.highlighted.connect(self.set_highlighted)

    def set_highlighted(self, text):
        self.last_selected = text
        # print(text)


    def get_selected(self):
        return self.last_selected

from PyQt5.QtWidgets import QCompleter, QStyledItemDelegate, QStyleOptionViewItem
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QModelIndex, QRectF, QSize
from PyQt5.QtGui import QFont, QColor, QPalette


class CompleterDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(CompleterDelegate, self).initStyleOption(option, index)
        option.backgroundBrush = QColor("red")
        option.palette.setBrush(QPalette.Text, QColor("blue"))
        option.displayAlignment = Qt.AlignCenter