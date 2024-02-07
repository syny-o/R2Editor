from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QListWidget, QMainWindow, QApplication, QWidget, QTreeWidget, QTreeView


class WidgetPointingHand(QWidget):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        if self.itemAt(self.viewport().mapFromGlobal(event.globalPos())) is not None:
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        return super().mouseMoveEvent(event)



class ListWidgetPointingHand(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        if self.itemAt(self.viewport().mapFromGlobal(event.globalPos())) is not None:
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        return super().mouseMoveEvent(event)     
        
           

class TreeWidgetPointingHand(QTreeWidget, WidgetPointingHand):
    pass



class TreeViewPointingHand(QTreeView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        if self.indexAt(self.viewport().mapFromGlobal(event.globalPos())).isValid():
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

