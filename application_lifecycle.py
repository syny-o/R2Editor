from PyQt5.QtWidgets import QMessageBox


class ApplicationLifecycle:
    def __init__(self, main_window, project_manager):
        self.main_window = main_window
        self.project_manager = project_manager

    def close(self, event):
        self.main_window.app_settings.save_settings_2_disk()

        if self._has_modified_documents() and not self._confirm(
            'Some opened files have been modified.\n\n'
            'Do you want to discard changes?'
        ):
            event.ignore()
            return

        if not self.project_manager.is_project_saved() and not self._confirm(
            'Current project is not saved.\n\n'
            'Do you want to exit (all changes will be lost)?'
        ):
            event.ignore()
            return

        event.accept()

    def _has_modified_documents(self):
        return any(
            text_edit.is_modified()
            for text_edit, _ in self.main_window.tab_manager.iter_text_edits()
        )

    def _confirm(self, message):
        answer = QMessageBox.question(
            self.main_window,
            'R2ScriptEditor',
            message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        return answer == QMessageBox.Yes
