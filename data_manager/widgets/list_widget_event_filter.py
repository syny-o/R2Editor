from math import e
import re
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel


styles = """
QListWidget::item:hover {
    background-color: rgb(58, 89, 245);
}
"""


class ListWidgetWithEventFilter(QListWidget):
    
    def __init__(self):
        super().__init__()
        self.installEventFilter(self)
        self.setMouseTracking(True)
        self.setStyleSheet(styles)

    # def eventFilter(self, source, event):
    #     if event.type() == QEvent.MouseMove:
    #         print("HoverMove")
    #         # self.setCursor(Qt.ArrowCursor)
    #         # cursor = self.mapFromGlobal(self.cursor().pos())
    #         # index = self.indexAt(cursor)
    #         if self.itemAt(self.viewport().mapFromGlobal(event.globalPos())) is not None:
    #             self.setCursor(Qt.PointingHandCursor)
    #         else:
    #             self.setCursor(Qt.ArrowCursor)

    #     return super().eventFilter(source, event)
        
    def mouseMoveEvent(self, event):
        if self.itemAt(self.viewport().mapFromGlobal(event.globalPos())) is not None:
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        return super().mouseMoveEvent(event)
    



# class MainWindow(QMainWindow):
#     def __init__(self, parent) -> None:
#         super().__init__(parent)

#         l = QVBoxLayout()
#         self.w = QWidget()
#         self.w.setLayout(l)
#         self.setCentralWidget(self.w)
#         self.lw = ListWidgetWithEventFilter()
#         self.lw.addItems(["Item 1", "Item 2", "Item 3"])
#         l.addWidget(self.lw)



# if __name__ == "__main__":
#     import sys
#     app = QApplication(sys.argv)
#     w = MainWindow(None)
#     w.show()
#     sys.exit(app.exec_())

