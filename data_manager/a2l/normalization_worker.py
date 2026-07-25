import os
import stat

from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot

from data_manager.a2l.normalizer import (
    find_missing_signals,
    normalize_a2l_text,
)
from dialogs.dialog_message import dialog_message


class A2lNormalizationWorker(QRunnable):
    def __init__(self, a2l_file_node, data_manager):
        super().__init__()
        self.a2l_file_node = a2l_file_node
        self.signals = WorkerSignals()
        self.signals.status.connect(data_manager.update_progress_status)
        self.signals.finished.connect(
            data_manager.a2l_normalisation_finished
        )

    @pyqtSlot()
    def run(self):
        self.signals.status.emit(
            True,
            "Normalising according to VDA spec...",
        )
        try:
            with open(self.a2l_file_node.path, "r") as file:
                a2l_text = file.read()
        except Exception as ex:
            print(
                f"Unable to open file {self.a2l_file_node.path}, "
                f"reason: {str(ex)}"
            )
            self.signals.status.emit(False, "")
            return

        normalized_text, report_data, duplicated_signals = (
            normalize_a2l_text(
                a2l_text,
                status_callback=lambda message: self.signals.status.emit(
                    True,
                    message,
                ),
            )
        )
        missing_signals = find_missing_signals(normalized_text)

        try:
            is_read_only = not os.access(
                self.a2l_file_node.path,
                os.W_OK,
            )
            if is_read_only:
                os.chmod(self.a2l_file_node.path, stat.S_IWRITE)

            with open(self.a2l_file_node.path, "w") as file:
                file.write(normalized_text)

            self.a2l_file_node.remove_all_children()
            self.a2l_file_node.file_2_tree()
            self.signals.finished.emit(
                report_data,
                missing_signals,
                duplicated_signals,
            )
        except Exception as ex:
            message = (
                f"Unable to save file {self.a2l_file_node.path}, "
                f"reason: {str(ex)}"
            )
            print(message)
            dialog_message(self.a2l_file_node.data_manager, message)
        finally:
            self.signals.status.emit(False, "")


class WorkerSignals(QObject):
    finished = pyqtSignal(dict, list, list)
    status = pyqtSignal(bool, str)
