from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QToolBar, QVBoxLayout, QHBoxLayout, QTextEdit, QTreeView, QLineEdit
from PyQt5.QtGui import QIcon, QScreen
from PyQt5.QtCore import Qt, QTimer


class DataManagerWidget(QWidget):
    selected_word = None
    is_visible = False

   

    

    def __init__(self, main_window, text_edit):
        super().__init__()
        self.main_window = main_window
        self.text_edit = text_edit

        self.setWindowFlags(Qt.Popup)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowOpacity(0.95)
        self.setStyleSheet("color: #edf; background-color: rgb(33, 37, 43); font-size: 12px;")

        self.create_layout()


        






    def create_layout(self):        
        self.layout_global = QHBoxLayout()  
        


        self.setLayout(self.layout_global)  

        





    def showEvent(self, event):

        if not event.spontaneous():

            self.main_window.stackedWidget.removeWidget(self.main_window.data_manager)
            self.layout_global.addWidget(self.main_window.data_manager)
            self.main_window.data_manager.frame_17.setVisible(False)  
            # self.main_window.data_manager.frame_2.setVisible(False)      
            self.main_window.data_manager.show()

            self.resize(self.main_window.width()-int(self.main_window.width()/5), self.main_window.height()-200)
            geo = self.geometry()
            geo.moveCenter(self.main_window.geometry().center())
            QTimer.singleShot(0, lambda: self.setGeometry(geo))





            



    def closeEvent(self, e):        
        self.layout_global.removeWidget(self.main_window.data_manager)
        self.main_window.stackedWidget.addWidget(self.main_window.data_manager)
        self.main_window.data_manager.frame_17.setVisible(True)  
        # self.main_window.data_manager.frame_2.setVisible(True) 
        self.text_edit.update_ctrl_pressed(False)
        return super().closeEvent(e)