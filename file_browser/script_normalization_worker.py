import os
import stat

from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot

from file_browser.script_normalizer import normalize_script_text


class ScriptNormalizationWorker(QRunnable):
    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        for root, _, files in os.walk(self.folder_path):
            for filename in files:
                if not filename.endswith((".par", ".txt")):
                    continue

                full_path = os.path.join(root, filename)
                self.signals.current_file.emit(full_path)

                is_read_only = not os.access(full_path, os.W_OK)
                if is_read_only:
                    os.chmod(full_path, stat.S_IWRITE)

                with open(full_path, "r") as file:
                    text = file.read()

                text, replacements = normalize_script_text(text)
                if replacements:
                    self.signals.replacements.emit(
                        full_path,
                        replacements,
                    )

                with open(full_path, "w") as file:
                    file.write(text)

                if is_read_only:
                    os.chmod(full_path, stat.S_IREAD)

        self.signals.finished.emit()


class WorkerSignals(QObject):
    replacements = pyqtSignal(str, list)
    current_file = pyqtSignal(str)
    finished = pyqtSignal()
