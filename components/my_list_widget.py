from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QListWidget, QInputDialog, QListWidgetItem, QAction, QMenu

class MyListWidget(QListWidget):

 

    def __init__(self, context_menu=True):
        super(MyListWidget, self).__init__()
        self.setIconSize(QtCore.QSize(124, 124))
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.DragDrop)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        # self.setDefaultDropAction(QtCore.Qt.MoveAction)

        # self.setStyleSheet("border-color: rgb(80, 80, 80);")

        self.action_remove_item = QAction("Remove")
        self.action_remove_item.triggered.connect(self.remove_item)
        self.action_remove_all_items = QAction("Remove All")
        self.action_remove_all_items.triggered.connect(self.remove_all_items)        
        self.action_insert_item = QAction("Insert")
        self.action_insert_item.triggered.connect(self.insert_item)   

        if context_menu:
            self.setContextMenuPolicy(Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self._context_menu)      


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():

            event.accept()
        else:

            super(MyListWidget, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.MoveAction)
   
            event.accept()
        else:
  
            super(MyListWidget, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
        else:
            event.setDropAction(QtCore.Qt.MoveAction)
            super(MyListWidget, self).dropEvent(event)


    def get_all_items(self):
        items = []
        for index in range(self.count()):
            items.append(self.item(index).text())
        return items


    def _context_menu(self, point):
        selected_item_index = self.indexAt(point)
      

        menu = QMenu()
        menu.addAction(self.action_insert_item)
        if self.count() > 0 and selected_item_index.isValid():
            menu.addAction(self.action_remove_item)
        if self.count() > 0:
            menu.addAction(self.action_remove_all_items)

        menu.exec_(QCursor().pos())


    def insert_item(self):
        item_name, ok = QInputDialog().getText(
            None, 
            "Add Column", 
            f"Column Name: ")
        if ok and item_name:
            item = QListWidgetItem(item_name.strip())
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.addItem(item)
            
    
    def remove_item(self):
        row = self.currentRow()
        self.takeItem(row)

    def remove_all_items(self):
        self.clear()