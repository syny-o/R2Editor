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
        # self.ui_tree_view = QTreeView()
        # self.ui_tree_view.setModel(self.main_window.data_manager.model)
        # self.ui_tree_view.setExpandsOnDoubleClick(True)
        # self.ui_tree_view.setHeaderHidden(True)

        # self.le_filter = QLineEdit()
        
        # btn_close = QPushButton(QIcon(u"ui/icons/check.png"), "Back")
        # btn_close.setCursor(Qt.PointingHandCursor)
        # btn_close.clicked.connect(self.close)

        # toolbar = QToolBar()
        # toolbar.addWidget(btn_close)  


        # layout_left = QVBoxLayout()
        
        # layout_left.addWidget(self.le_filter)
        # layout_left.addWidget(self.ui_tree_view)

        # layout_right = QVBoxLayout()
        # layout_right.addWidget(QLineEdit())
        # layout_right.addWidget(QLineEdit())
        # layout_right.addWidget(QLineEdit())
        # layout_right.addWidget(QLineEdit())
        # layout_right.addWidget(QTextEdit())
        

        self.layout_global = QHBoxLayout()
        # layout_global.setSpacing(20)
        # layout_global.setContentsMargins(20, 20, 20, 20)
        # layout_global.addLayout(layout_left)
        # layout_global.addLayout(layout_right)
        # layout_global.addWidget(toolbar)
        
        
        # self.setLayout(self.layout_global)     
        


        self.setLayout(self.layout_global)  

        





    def showEvent(self, event):

        if not event.spontaneous():
            self.resize(self.main_window.width()-int(self.main_window.width()/5), self.main_window.height()-200)
            geo = self.geometry()
            geo.moveCenter(self.main_window.geometry().center())
            QTimer.singleShot(0, lambda: self.setGeometry(geo))

        self.main_window.stackedWidget.removeWidget(self.main_window.data_manager)
        self.layout_global.addWidget(self.main_window.data_manager)
        self.main_window.data_manager.frame_17.setVisible(False)  
        # self.main_window.data_manager.frame_2.setVisible(False)      
        self.main_window.data_manager.show()

            # # HANDLE SCROLLBAR
            # scroll_bar = self.te.verticalScrollBar()
            # scroll_bar.setSliderPosition(0)


            



    def closeEvent(self, e):        
        self.layout_global.removeWidget(self.main_window.data_manager)
        self.main_window.stackedWidget.addWidget(self.main_window.data_manager)
        self.main_window.data_manager.frame_17.setVisible(True)  
        # self.main_window.data_manager.frame_2.setVisible(True) 
        self.text_edit.update_ctrl_pressed(False)
        return super().closeEvent(e)