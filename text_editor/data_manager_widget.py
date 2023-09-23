from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QToolBar, QVBoxLayout, QHBoxLayout, QTextEdit, QTreeView, QLineEdit
from PyQt5.QtGui import QIcon, QScreen, QPalette, QColor
from PyQt5.QtCore import Qt, QTimer


class DataManagerWidget(QWidget):
    selected_word = None
    is_visible = False

   

    

    def __init__(self, main_window, text_edit):
        super().__init__()
        self.main_window = main_window
        self.text_edit = text_edit

        self.palette = QPalette()
        self.palette.setColor(QPalette.Window, QColor(58,89,245))
        self.palette.setColor(QPalette.Text, QColor(200, 200, 200))
        self.palette.setColor(QPalette.WindowText, QColor(200, 200, 200))
        self.setPalette(self.palette)

        # self.setWindowFlags(Qt.Popup)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowOpacity(0.95)
        self.setStyleSheet("QFrame {color: #edf; background-color: rgb(33, 37, 43); background-color: black; font-size: 12px;}\
         QLineEdit {color: #edf; background-color: rgb(33, 37, 43); background-color: black; font-size: 12px;}\
         QLabel {color: #edf; background-color: rgb(33, 37, 43); background-color: black; font-size: 12px;}")
        
        

        self.create_layout()


        






    def create_layout(self):        
        self.layout_global = QHBoxLayout()  
        self.layout_global.setContentsMargins(1,1,1,1)


        self.setLayout(self.layout_global)  

        





    def showEvent(self, event):

        if not event.spontaneous():

            self.main_window.stackedWidget.removeWidget(self.main_window.data_manager)
            self.layout_global.addWidget(self.main_window.data_manager)
            self.main_window.data_manager.frame_17.setVisible(False)  
            # self.main_window.data_manager.frame_2.setVisible(False)      
            self.main_window.data_manager.show()

            self.resize(self.main_window.width()-int(self.main_window.width()/4), self.main_window.height()-300)
            geo = self.geometry()
            geo.moveCenter(self.main_window.geometry().center())
            QTimer.singleShot(0, lambda: self.setGeometry(geo))



    def keyPressEvent(self, event) -> None:

        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_Q:
            self.close()
            return

        # "ESC" Cancel Selection
        if event.key() == Qt.Key_Escape:
            self.close()
            return

        return super().keyPressEvent(event)



            



    def closeEvent(self, e):        
        self.layout_global.removeWidget(self.main_window.data_manager)
        self.main_window.stackedWidget.addWidget(self.main_window.data_manager)
        self.main_window.data_manager.frame_17.setVisible(True)  
        # self.main_window.data_manager.frame_2.setVisible(True) 
        self.text_edit.update_ctrl_pressed(False)
        return super().closeEvent(e)