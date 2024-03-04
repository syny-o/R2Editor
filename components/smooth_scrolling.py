# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *

import sys

from PyQt5.QtCore import QObject, pyqtSlot, QVariant, QVariantAnimation
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QPushButton, QHBoxLayout


longText = "\n".join(["{}: long text - auto scrolling ".format(i) for i in range(100)])

class SmoothScrolling(QObject):
    def __init__(self, text_edit):
        super(SmoothScrolling, self).__init__()
        self.animation = QVariantAnimation(self)
        self.animation.valueChanged.connect(self.set_scrollbar_value)
        self.text_edit = text_edit


    def current_scrollbar_value(self):
        return self.text_edit.verticalScrollBar().value()
    
    def max_scrollbar_value(self):
        return self.text_edit.verticalScrollBar().maximum()
    

    @pyqtSlot()
    def move_2_line(self, desired_line):
        self.animation.stop()
        self.animation.setStartValue(self.current_scrollbar_value())
        self.animation.setEndValue(desired_line)
        self.animation.setDuration(200)
        self.animation.start()


    @pyqtSlot(QVariant)
    def set_scrollbar_value(self, i):
        self.text_edit.verticalScrollBar().setValue(i)

    def line_number_from_position(self, position):
        return self.self.text_edit.toPlainText()[:position].count("\n")       

class MyApp(QWidget):
    def __init__(self):
        super(MyApp, self).__init__()
        self.setFixedSize(600, 400)
        self.txt = QTextEdit()
        smooth_scrolling = SmoothScrolling(self.txt)
        self.btn = QPushButton("Start", self)
        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.txt)
        self.layout.addWidget(self.btn)
        self.txt.append(longText)
        # self.txt.moveToLine(0)
        self.btn.clicked.connect(lambda: smooth_scrolling.move_2_line(250))

        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())