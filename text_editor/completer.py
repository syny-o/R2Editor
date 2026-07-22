from PyQt5.QtCore import QEvent, QObject, QPoint, QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QCompleter, QListWidget


COMPLETER_FONT = QFont('Consolas', 10)


class Completer(QCompleter):
    cond_dict = {}
    cond_model = None
    a2l_model = None
    dspace_model = None

    insert_text = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.last_selected = ''

        self.setCompletionMode(QCompleter.PopupCompletion)
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setFilterMode(Qt.MatchContains)
        self.setMaxVisibleItems(15)
        self.popup().setFont(COMPLETER_FONT)

        self.highlighted[str].connect(self.set_highlighted)
        self.completer_tooltip = CompleterTooltipController(self)

    def set_highlighted(self, text):
        self.last_selected = text

    def get_selected(self):
        return self.last_selected

    def eventFilter(self, watched, event):
        if event.type() == QEvent.KeyRelease:
            if event.key() == Qt.Key_Up and not self.popup().currentIndex().isValid():
                last_row = self.completionModel().rowCount() - 1
                self.popup().setCurrentIndex(self.completionModel().index(last_row, 0))
            elif event.key() == Qt.Key_Down and not self.popup().currentIndex().isValid():
                self.popup().setCurrentIndex(self.completionModel().index(0, 0))
            elif event.key() in (Qt.Key_Left, Qt.Key_Right):
                self.popup().hide()

        return super().eventFilter(watched, event)


class CompleterTooltipController(QObject):
    def __init__(self, completer):
        super().__init__(completer)
        self.completer = completer
        self.tooltip = QListWidget()
        self.tooltip.setWindowFlags(Qt.ToolTip)
        self.tooltip.setObjectName('completer_tooltip')
        self.tooltip.setFont(COMPLETER_FONT)

        self.completer.highlighted[str].connect(self.show_tooltip)
        self.completer.popup().installEventFilter(self)

    def eventFilter(self, watched, event):
        if watched == self.completer.popup():
            if event.type() == QEvent.Hide:
                self.hide_tooltip()
            elif event.type() == QEvent.KeyPress and event.key() == Qt.Key_Escape:
                self.hide_tooltip()

        return super().eventFilter(watched, event)

    def show_tooltip(self, completion):
        model = self.completer.model()
        for row in range(model.rowCount()):
            item = model.item(row)
            if item.text() != completion:
                continue

            data = item.data(Qt.UserRole)
            if not data:
                self.hide_tooltip()
                return

            self.tooltip.clear()
            self.tooltip.addItems(data)
            self.adjust_size()
            QTimer.singleShot(0, self.position_tooltip)
            return

        self.hide_tooltip()

    def position_tooltip(self):
        popup = self.completer.popup()
        self.tooltip.move(popup.mapToGlobal(QPoint(popup.width(), 0)))
        if popup.isVisible():
            self.tooltip.show()

    def hide_tooltip(self):
        self.tooltip.hide()

    def adjust_size(self):
        if self.tooltip.count() == 0:
            return

        height = sum(
            self.tooltip.sizeHintForRow(row)
            for row in range(self.tooltip.count())
        ) + 8
        width = self.tooltip.sizeHintForColumn(0) + 20
        self.tooltip.setFixedSize(width, height)
