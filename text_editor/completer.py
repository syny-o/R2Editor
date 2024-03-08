from json import tool
import re
from turtle import color
from PyQt5.QtWidgets import QCompleter, QStyledItemDelegate, QStyleOptionViewItem
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QModelIndex, QRectF, QSize, QTimer
from PyQt5.QtGui import QFocusEvent, QFont, QKeyEvent, QShowEvent, QIcon

import qtawesome as qta
from config import icon_manager


from config.icon_manager import IconManager


mono_font = QFont('Courier')
mono_font = QFont('Consolas')
mono_font.setPointSize(10)

class Completer(QCompleter):


#################### DATA 4 TEXT EDITOR #########################


    cond_dict = {}
    cond_model = None
    a2l_model = None
    dspace_model = None

    cond_tooltips = {}



#################################################################

    # Custom signal definition
    insert_text = pyqtSignal(str)

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Completer configuration
        self.setCompletionMode(QCompleter.PopupCompletion)
        self.setCaseSensitivity(Qt.CaseInsensitive)
        self.setFilterMode(Qt.MatchContains)
        # self.setCompletionRole(Qt.ToolTipRole)

        # self.popup = self.popup()
        # self.popup().setFont(mono_font)

        self.setMaxVisibleItems(15)

        # Built-in signal -->  signal is sent when an item in the popup() is highlighted by the user
        self.highlighted.connect(self.set_highlighted)

        self.completer_tooltip = CompleterToolTip(self)
        # self.completer_tooltip.setFont(mono_font)



    def set_highlighted(self, text):
        # print('highlighted:', text)
        self.last_selected = text
        # self.completer_tooltip.show_tooltip(text)
        


    def get_selected(self):
        return self.last_selected
    
    # def eventFilter(self, watched, event):
    #     if event.type() == QEvent.KeyRelease:
    #         if event.key() == Qt.Key_Up and not self.popup().currentIndex().isValid():
    #             self.popup().setCurrentIndex(self.completionModel().index(self.completionModel().rowCount()-1, 0))
    #         elif event.key() == Qt.Key_Down and not self.popup().currentIndex().isValid():
    #             self.popup().setCurrentIndex(self.completionModel().index(0, 0))

        # if event.type() == QEvent.MouseButtonPress:
        #     print(self.get_selected())
        #     print(watched)
            
        
        # return super().eventFilter(watched, event)   


    

    

    

    







from PyQt5.QtWidgets import QApplication, QTextEdit, QCompleter, QVBoxLayout, QWidget, QListView, QListWidget, QListWidgetItem, QToolBar, QPushButton, QSizePolicy
from PyQt5.QtGui import QMouseEvent, QTextCursor, QSyntaxHighlighter, QTextCharFormat, QColor, QTextDocument, QCursor
from PyQt5.QtCore import Qt, QEvent, QPoint, QSize, QRegExp







class CompleterToolTip(QWidget):
    def __init__(self, completer, parent=None):
        super(CompleterToolTip, self).__init__(parent=completer.popup())
        self.completer = completer
        self.tooltip = CustomListWidget()
        # self.tooltip.setEnabled(False)
        self.tooltip.setFocusPolicy(Qt.NoFocus)
        self.setWindowFlags(Qt.Popup)       
        # self.setWindowFlags(Qt.ToolTip)   
        self.setObjectName('completer_tooltip')
        self.setFont(mono_font)

        self.icon_manager = IconManager()

        # self.tooltip.setReadOnly(True)
        self.completer.highlighted[str].connect(self.show_tooltip)

        self.completer.popup().installEventFilter(self)
        self.tooltip.installEventFilter(self)
        self.installEventFilter(self)

        layout = QVBoxLayout()
        self.toolbar = QToolBar()
        self.toolbar.setObjectName('completer_tooltip_toolbar')
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.toolbar.addWidget(spacer)
        
        # self.uiBtnEdit = QPushButton('')
        self.uiBtnEdit = MyButton('Edit')
        self.uiBtnEdit.setMouseTracking(True)
        self.uiBtnEdit.setIconSize(QSize(30, 30))
        self.uiBtnEdit.clicked.connect(self.goto_index)
        self.uiBtnEdit.setIcon(qta.icon('mdi.pencil', color='#3a59f5'))
        self.uiBtnEdit.setCursor(QCursor(Qt.PointingHandCursor))
        self.uiBtnEdit.setShortcut('F4')
        self.toolbar.addWidget(self.uiBtnEdit)
        self.toolbar.setCursor(Qt.PointingHandCursor)

        # self.action_edit = toolbar.addAction(qta.icon('fa5s.edit', color='blue'), 'Edit', lambda: print('edit'))
        # toolbar.addAction(qta.icon('fa5s.times', color='blue'), 'Close', lambda: print('close'))
        # toolbar.setMaximumHeight(100)
        layout.addWidget(self.tooltip)
        layout.addWidget(self.toolbar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        self.setLayout(layout)
        self.setContentsMargins(0, 0, 0, 0)

        self.uiBtnEdit.setFocusPolicy(Qt.NoFocus)






    def goto_index(self):
        item_index = self.get_item_from_popup(self.completer.get_selected())
        self.completer.main_window.data_manager.goto_index(item_index) 
        self.completer.main_window.actual_text_edit.data_manager_widget.show()


    def eventFilter(self, watched, event):
        try:
            # if watched == self.completer.popup() and event.type() == QEvent.Enter:
            #     print('popup entered')
            #     QApplication.setOverrideCursor(QCursor(Qt.PointingHandCursor))
            
            # if watched == self.completer.popup() and self.tooltip.geometry().contains(self.tooltip.mapFromGlobal(QCursor.pos())):
            #     QApplication.setOverrideCursor(QCursor(Qt.PointingHandCursor))
            #     return False
                

            # if watched == self.completer.popup() and event.type() == QEvent.MouseButtonRelease:
            #     self.hide_tooltip()
            #     return False

            if watched == self and self.completer.popup().isVisible() and event.type() == QEvent.KeyPress:
                key = event.key()
                if key == Qt.Key_Down:
                    current_row = self.completer.popup().currentIndex().row()
                    self.completer.popup().setCurrentIndex(self.completer.popup().model().index(current_row+1, 0))
                    current_index = self.completer.popup().currentIndex()
                    if not current_index.isValid():
                        self.completer.popup().setCurrentIndex(self.completer.popup().model().index(0, 0))
                    return False
                
                if key == Qt.Key_Up:
                    current_row = self.completer.popup().currentIndex().row()
                    self.completer.popup().setCurrentIndex(self.completer.popup().model().index(current_row-1, 0))
                    current_index = self.completer.popup().currentIndex()
                    if not current_index.isValid():
                        self.completer.popup().setCurrentIndex(self.completer.popup().model().index(self.completer.popup().model().rowCount()-1, 0))
                    return False

                
                if key == Qt.Key_Return:
                    self.completer.insert_text.emit(self.completer.get_selected())
                    return False

                if key == Qt.Key_Escape:
                    # self.hide_tooltip()   
                    self.completer.popup().hide()
                    return False


                self.completer.main_window.actual_text_edit.keyPressEvent(event)
                
        
            if watched == self.completer.popup() and event.type() == QEvent.Hide:
                self.hide_tooltip()
                return False
            

            if watched == self and self.completer.popup().isVisible() and event.type() == QEvent.MouseButtonPress:
                return True
            


            # if watched == self.completer.popup() and event.type() == QEvent.KeyPress:
            #     key = event.key()
            #     if key not in [Qt.Key_Up, Qt.Key_Down]:
            #         self.hide_tooltip()   
                    
        except Exception as e:
            print(e)         
        
        return super(CompleterToolTip, self).eventFilter(watched, event)   



    # def mousePressEvent(self, a0: QMouseEvent | None) -> None:
    #     self.hide_tooltip()
    #     return super().mousePressEvent(a0)
    

    # def keyPressEvent(self, a0: QKeyEvent | None) -> None:
    #     print(a0.key())
    #     return super().keyPressEvent(a0)



    def get_item_from_popup(self, completion):
        model = self.completer.model()
        for i in range(model.rowCount()):
            item = model.item(i)
            if item.text() == completion:
                return item.data(Qt.UserRole+1)




    def show_tooltip(self, completion):


        model = self.completer.model()
        for i in range(model.rowCount()):
            item = model.item(i)
            if item.text() == completion:
                data = item.data(Qt.UserRole)
                if data:
                    self.tooltip.clear()
                    # self.tooltip.addItems(data)
                    for d in data:
                        item = QListWidgetItem(d)
                        item.setIcon(QIcon('ui/icons/ts.png'))
                        self.tooltip.addItem(item)
          
        





        # self.tooltip.setText(text)
        self.adjust_listwidget_size(self.tooltip)
        
        QTimer.singleShot(0, self.position_tooltip)



    def position_tooltip(self):
        if not self.completer.popup().isVisible():
            return        
        self.move(self.completer.popup().mapToGlobal(QPoint(self.completer.popup().width(), 0)))
        self.show()   
         



    def hide_tooltip(self):
        # self.hide() 
        QTimer.singleShot(0, self.hide)



    def adjust_listwidget_size(self, listwidget):
        height = sum([listwidget.sizeHintForRow(i) for i in range(listwidget.count())]) + 12
        width = max([listwidget.sizeHintForColumn(i) for i in range(listwidget.count())]) + 20
        # listwidget.setFixedSize(width, height) 
        self.setFixedSize(width+10, height+35) 
        self.adjustSize()     





    

class MyButton(QPushButton):
    def enterEvent(self, event):
        QApplication.setOverrideCursor(QCursor(Qt.PointingHandCursor))
        super().enterEvent(event)

    def leaveEvent(self, event):
        QApplication.restoreOverrideCursor()
        super().leaveEvent(event)    



class CustomListWidget(QListWidget):
    def mousePressEvent(self, event):
        event.ignore()        

    def mouseReleaseEvent(self, event):
        event.ignore()

    def mouseDoubleClickEvent(self, event):
        event.ignore()

    def mouseMoveEvent(self, e: QMouseEvent | None) -> None:
        e.ignore()

      




# class CompleterToolTip(QTextEdit):
#     def __init__(self, completer, parent=None):
#         super(CompleterToolTip, self).__init__(parent)
#         self.completer = completer
#         self.tooltip = QTextEdit()
#         self.tooltip = QListWidget()
#         self.tooltip.setWindowFlags(Qt.ToolTip)
#         self.tooltip.setObjectName('completer_tooltip')
#         self.tooltip.setFont(mono_font)

#         self.icon_manager = IconManager()

#         # self.tooltip.setReadOnly(True)
#         self.completer.highlighted[str].connect(self.show_tooltip)

#         self.completer.popup().installEventFilter(self)

        





#     def eventFilter(self, watched, event):
#         try:
        
#             if watched == self.completer.popup() and event.type() == QEvent.Hide:
#                 self.hide_tooltip()
#                 return False

#             if watched == self.completer.popup() and event.type() == QEvent.KeyPress:
#                 key = event.key()
#                 if key == Qt.Key_Escape:
#                     self.hide_tooltip()   
                    
#         except Exception as e:
#             print(e)         
        
#         return super(CompleterToolTip, self).eventFilter(watched, event)        






#     def show_tooltip(self, completion):
#         model = self.completer.model()
#         for i in range(model.rowCount()):
#             item = model.item(i)
#             if item.text() == completion:
#                 data = item.data(Qt.UserRole)
#                 if data:
#                     self.tooltip.clear()
#                     self.tooltip.addItems(data)
#                     # for d in data:
#                     #     item = QListWidgetItem(d)
#                     #     item.setIcon(self.icon_manager.ICON_TEST_STEP)
#                     #     self.tooltip.addItem(item)
        





#         # self.tooltip.setText(text)
#         self.adjust_listwidget_size(self.tooltip)
        
#         QTimer.singleShot(0, self.position_tooltip)


#     def position_tooltip(self):
#         self.tooltip.move(self.completer.popup().mapToGlobal(QPoint(self.completer.popup().width(), 0)))
#         self.tooltip.show()   


#     def hide_tooltip(self):
#         self.tooltip.hide() 



#     def adjust_listwidget_size(self, listwidget):
#         height = sum([listwidget.sizeHintForRow(i) for i in range(listwidget.count())]) + 8
#         width = max([listwidget.sizeHintForColumn(i) for i in range(listwidget.count())]) + 20
#         listwidget.setFixedSize(width, height)        
                




