from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QToolBar, QVBoxLayout, QTextEdit, QSizePolicy
from PyQt5.QtGui import QIcon, QScreen, QPalette, QColor
from PyQt5.QtCore import Qt, QTimer


class TextEditTooltipWidget(QWidget):
    selected_word = None
    is_visible = False
    

    def __init__(self, main_window, text_edit, text):
        super().__init__()
        self.main_window = main_window
        self.text_edit = text_edit

        TextEditTooltipWidget.is_visible = True
        TextEditTooltipWidget.shift_pressed = False

        self.setWindowFlags(Qt.Popup)
        self.setWindowOpacity(0.9)
        self.setMaximumSize(1024, 768)
        self.setMinimumSize(640, 480)
        self.palette = QPalette()
        self.palette.setColor(QPalette.Window, QColor(58,89,245))
        self.palette.setColor(QPalette.Text, QColor(200, 200, 200))
        self.palette.setColor(QPalette.WindowText, QColor(200, 200, 200))
        # self.setPalette(self.palette)

        self.resize(*self.calculate_size(text))

        # self.setStyleSheet("color: #edf; background-color: #222; font-size: 12px;")




        
        
        

        btn = QPushButton(QIcon(u"ui/icons/16x16/cil-x.png"), " Close (Esc)")
        btn.setCursor(Qt.PointingHandCursor)
        btn.clicked.connect(self.close)

        toolbar = QToolBar()
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolbar.addWidget(spacer)
        toolbar.addWidget(btn)
        

        # self.te = QTextEdit()
        self.te = QTextEdit()
        self.te.setReadOnly(True)
        l = QVBoxLayout()
        l.addWidget(self.te)
        l.addWidget(toolbar)

        l.setSpacing(20)
        l.setContentsMargins(20, 20, 20, 20)
        
        self.setLayout(l)

        self.te.append(text)



        self.show()    


    def calculate_size(self, text):
        lines = text.splitlines()
        longest_line = 0
        for line in lines:
            if len(line) > longest_line:
                longest_line = len(line)
        
        if len(lines) < 5:
            return longest_line*5, len(lines) * 300

        return longest_line*5, len(lines) * 30


    def showEvent(self, event):
        if not event.spontaneous():
            geo = self.geometry()
            geo.moveCenter(self.main_window.geometry().center())
            QTimer.singleShot(0, lambda: self.setGeometry(geo))

            # HANDLE SCROLLBAR
            scroll_bar = self.te.verticalScrollBar()
            scroll_bar.setSliderPosition(0)


    def closeEvent(self, e):
        TextEditTooltipWidget.is_visible = False
        self.text_edit.update_ctrl_pressed(False)
        return super().closeEvent(e)