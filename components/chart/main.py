import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor, QPainter
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout,QHBoxLayout, QApplication, QMainWindow, QFrame

from chart_bar import ChartBar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle("My App")

        layout = QVBoxLayout()

        # chart_widget = ChartWidget()
        # layout.addWidget(chart_widget)

        self.container = QFrame()
        self.container.setStyleSheet("background-color: transparent; ")

        self.layout = QHBoxLayout()
        self.container.setLayout(self.layout)


        self.chart = ChartBar()
        self.chart.setMinimumSize(self.chart.width, self.chart.height)
        self.chart.value = 75
        self.layout.addWidget(self.chart, Qt.AlignCenter, Qt.AlignCenter)
        self.setCentralWidget(self.container)
        
        # self.setLayout(layout)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())