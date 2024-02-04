import re
from PyQt5.QtGui import QPaintEvent, QPainter, QPen, QColor, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QRect

class ChartBar(QWidget):
    def __init__(self):
        super().__init__()

        self.resize(200, 200)

        # CUSTOM PROPERTIES
        self.value = 0
        self.max_value = 100
        self.number_covered = 0
        self.number_total = 0
        self.width = 200
        self.height = 200
        self.progress_width = 5
        self.progress_rounded_cap = True
        self.progress_color = "green"
        self.font_family = "Calibri"
        self.font_size = 24
        self.suffix = "%"
        self.text_color = "green"
        self.secondary_text_color = "gray"
        self.secondary_font_size = 12
        self.enable_shadow = False

        # SET DEFAULT SIZE W/O LAYOUT
        self.resize(self.width, self.height)

        if self.enable_shadow:
            self.add_shadow()

        self.setMinimumSize(self.width, self.height)
        # self.value = 81        

    
    def paintEvent(self, event: QPaintEvent) -> None:
        width = self.width - self.progress_width
        height = self.height - self.progress_width
        margin = int(self.progress_width / 2)
        value = self.value * 360 / self.max_value

        paint = QPainter(self)
        # paint.begin(self)
        paint.setRenderHint(QPainter.Antialiasing)

        # FONT
        paint.setFont(QFont(self.font_family, self.font_size))

        # CREATE RECTANGLE
        rect = QRect(0, 0, self.width, self.height)
        paint.setPen(Qt.NoPen)
        paint.drawRect(rect)

        # PEN
        pen = QPen()
        pen.setColor(QColor(self.progress_color))
        pen.setWidth(self.progress_width)
        
        # SET ROUND CAP
        if self.progress_rounded_cap:
            pen.setCapStyle(Qt.RoundCap)

        # CREATE ARC / CIRCIULAR PROGRESS
        paint.setPen(pen)
        paint.drawArc(margin, margin, width, height, -90 * 16, int(-value * 16))

        # PERCENTAGE TEXT
        pen.setColor(QColor(self.text_color))
        paint.setPen(pen)           
        paint.drawText(rect, Qt.AlignCenter, f"{self.value}{self.suffix}") 

        # HEADER TEXT
        pen.setColor(QColor(self.secondary_text_color))
        paint.setFont(QFont(self.font_family, self.secondary_font_size))
        paint.setPen(pen)
        upper_rect = QRect(0, 0, self.width, int(self.height / 2))
        paint.drawText(upper_rect, Qt.AlignCenter, "COVERAGE")

        # FOOTER TEXT
        lower_rect = QRect(0, 0, self.width, int((self.height/2) + (self.height)))
        paint.drawText(lower_rect, Qt.AlignCenter, f"{self.number_covered} / {self.number_total}")        

        # END
        paint.end()

        return super().paintEvent(event)


    def set_value(self, number_covered, number_total):
        self.number_covered = number_covered
        self.number_total = number_total
        self.value = int((number_covered / number_total) * 100)
        self.repaint()

    def add_shadow(self):
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.shadow)




