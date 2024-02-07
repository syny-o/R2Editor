from PyQt5.QtWidgets import QTreeView, QSizePolicy
from PyQt5.QtCore import pyqtSignal, Qt


MAX_STORED_INDEXES = 40

class DataTreeView(QTreeView):

    send_data_from_drop = pyqtSignal(dict)

    previous_indexes = []

    def __init__(self, PARENT):
        super().__init__()

        self.PARENT = PARENT

        self.setHeaderHidden(True)
        self.setExpandsOnDoubleClick(True)
        self.setAnimated(True) 
        self.setMouseTracking(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)        


        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.setAcceptDrops(True)
        self.setDragDropMode(QTreeView.DropOnly)
        self.setDropIndicatorShown(True)

        self.expanded.connect(self._node_was_expanded)
        self.collapsed.connect(self._node_was_collapsed)
        self.clicked.connect(lambda index: self.setExpanded(index, False) if self.isExpanded(index) else self.setExpanded(index, True))
        
        self.send_data_from_drop.connect(self.PARENT.uiDataTreeView_received_files)  # TODO: REFACTOR


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()  # list of paths

            for url in urls:
                path = url.toLocalFile()
                if path.lower().endswith('.con'):
                    self.send_data_from_drop.emit(
                        {'Conditions Files': [path]}
                    )
                    # event.acceptProposedAction()
                    event.accept()
                elif path.lower().endswith('dspacemapping.py'):
                    self.send_data_from_drop.emit(
                        {'DSpace Files': [path]}
                    )
                    event.accept()
                elif path.lower().endswith('.a2l'):
                    self.send_data_from_drop.emit(
                        {'A2L Files': [path]}
                    )
                    event.accept()


    def mouseMoveEvent(self, event):
        if self.indexAt(self.viewport().mapFromGlobal(event.globalPos())).isValid():
            self.setCursor(Qt.PointingHandCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        return super().mouseMoveEvent(event)                        


    def currentChanged(self, current, previous) -> None:
        self.previous_indexes.append(previous)
        if len(self.previous_indexes) > MAX_STORED_INDEXES:
            self.previous_indexes.pop(0)
        
        self.PARENT.uiDataTreeView_current_index_changed(current, previous)

    
        return super().currentChanged(current, previous)



    def _node_was_collapsed(self, node_index):
        pass      

    def _node_was_expanded(self, node_index):
        self.previous_indexes.append(tuple(["expanded", node_index]))


    
    
    
############################################################################################################
# INTERFACE:
############################################################################################################
            
    def collapse_all_children(self):
        index = self.currentIndex()
        if not index.isValid():
            return
        item = index.model().itemFromIndex(index)
        
        def _browse_children(node):         
            for row in range(node.rowCount()):
                requirement_node = node.child(row)
                requirement_node_index = requirement_node.index()
                self.collapse(requirement_node_index)

                _browse_children(requirement_node)        
        
        _browse_children(item)
        self.collapse(index)

    
    def expand_all_children(self):    
        index = self.currentIndex()
        if not index.isValid():
            return            
        self.expandRecursively(index)        


    def goto_previous_index(self):
        try:
            if len(self.previous_indexes) > 2:

                previous_index = self.previous_indexes.pop()
                while type(previous_index) is tuple:
                    expanded_index = previous_index[1]
                    self.collapse(expanded_index)
                    previous_index = self.previous_indexes.pop()
                else:            
                    self.setCurrentIndex(previous_index)
                    self.scrollTo(previous_index)
                    self.previous_indexes.pop()
        except:
            pass        