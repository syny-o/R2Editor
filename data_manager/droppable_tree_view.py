from PyQt5.QtWidgets import QTreeView
from PyQt5.QtCore import pyqtSignal

class DroppableTreeView(QTreeView):

    send_data_from_drop = pyqtSignal(dict)

    def __init__(self, data_manager):
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragDropMode(QTreeView.DropOnly)
        self.setDropIndicatorShown(True)

        self.send_data_from_drop.connect(data_manager.receive_data_from_drop_or_file_manager)

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