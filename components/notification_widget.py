from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QToolBar, QVBoxLayout, QHBoxLayout, QTextEdit, QTreeView, QLineEdit, QLabel
from PyQt5.QtGui import QIcon, QScreen, QPalette, QColor, QPixmap
from PyQt5.QtCore import Qt, QTimer, QRunnable, QThreadPool, pyqtSlot


class NotificationWidget(QWidget):    

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        # self.setMinimumWidth(700)

        # self.setWindowFlags(Qt.Popup)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.ToolTip)
        self.setWindowOpacity(0.9)
        self.palette = QPalette()
        self.palette.setColor(QPalette.Window, QColor(23, 27, 33))
        self.palette.setColor(QPalette.Text, QColor(200, 200, 200))
        self.palette.setColor(QPalette.WindowText, QColor(200, 200, 200))
        # self.setPalette(self.palette)

        self.create_layout()





    def create_layout(self):        
        self.layout_global = QVBoxLayout()
        self.layout_global.setContentsMargins(50, 30, 50, 30)
        self.layout_global.setSpacing(20)
        picture = QLabel()
        # picture.setPixmap(QPixmap("ui\icons\check.png"))
        picture.setPixmap(QPixmap(r"ui/icons/info.png"))
        # picture.setScaledContents(True)
        picture.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        # self.layout_global.addWidget(picture)
        
        self.ui_notification_text = QLabel()
        font = self.ui_notification_text.font()
        font.setPointSize(12)
        self.ui_notification_text.setFont(font)
        self.ui_notification_text.setPalette(self.palette)
        self.ui_notification_text.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.layout_global.addWidget(self.ui_notification_text)



        self.setLayout(self.layout_global)  


    def showEvent(self, event):

        if not event.spontaneous():
            geo = self.geometry()
            geo_main_window = self.main_window.geometry()
            geo.moveCenter(geo_main_window.center())
            geo.moveBottom(geo_main_window.bottom() - 20)
            QTimer.singleShot(0, lambda: self.setGeometry(geo))
            QTimer.singleShot(4000, lambda: self.close())


    def closeEvent(self, e):        
        return super().closeEvent(e)


    def show_text(self, text):
        self.ui_notification_text.setText(text)
        self.show()
        # self.threadpool = QThreadPool()
        # self.threadpool.setMaxThreadCount(1)
        # self.worker = Worker(self)
        
        # self.threadpool.start(self.worker)



# class Worker(QRunnable):
#     def __init__(self, notification_widget):
#         super().__init__()
#         self.notification_widget = notification_widget

#     @pyqtSlot()
#     def run(self):
#         self.notification_widget.show()



