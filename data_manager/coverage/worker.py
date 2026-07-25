from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot

from data_manager.coverage.scanner import scan_requirement_references


class CoverageWorker(QRunnable):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.signals = CoverageWorkerSignals()
        self.signals.status.connect(data_manager.update_progress_status)
        self.signals.finished.connect(data_manager.check_coverage)

    @pyqtSlot()
    def run(self):
        references = scan_requirement_references(
            self.data_manager.PROJECT_MANAGER.disk_project_path(),
            progress=lambda text: self.signals.status.emit(True, text),
        )
        self.signals.status.emit(
            False,
            'Updating coverage, please wait...',
        )
        self.signals.finished.emit(references)


class CoverageWorkerSignals(QObject):
    finished = pyqtSignal(dict)
    status = pyqtSignal(bool, str)
