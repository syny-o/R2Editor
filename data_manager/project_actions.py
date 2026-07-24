from PyQt5.QtWidgets import QFileDialog, QMessageBox

from dialogs.dialog_message import dialog_message


PROJECT_FILE_FILTER = 'RapitTwo Editor Project (*.json)'
PROJECT_DIRECTORY = './/Projects'


class ProjectActions:
    def __init__(self, parent, project_manager, show_notification):
        self.parent = parent
        self.project_manager = project_manager
        self.show_notification = show_notification

    def connect_actions(self):
        self.parent.btn_project_open.clicked.connect(self.open)
        self.parent.btn_project_new.clicked.connect(self.new)
        self.parent.btn_project_save.clicked.connect(self.save)
        self.parent.btn_project_save_as.clicked.connect(self.save_as)

    def new(self):
        if not self._confirm_discard_unsaved_project():
            return
        self.project_manager.new_project()

    def save(self):
        success, message = self.project_manager.save_project()
        if success:
            self.show_notification(message)
        elif message == 'NO JSON PATH':
            self.save_as()
        else:
            dialog_message(self.parent, message)

    def autosave(self):
        _, message = self.project_manager.save_project()
        self.show_notification(f'autosaving... {message}')

    def save_as(self):
        path, _ = QFileDialog.getSaveFileName(
            parent=self.parent,
            caption='Save Project',
            directory=PROJECT_DIRECTORY,
            filter=PROJECT_FILE_FILTER,
        )
        if not path:
            return

        success, message = self.project_manager.save_project_as(path)
        if success:
            self.show_notification(message)
        else:
            dialog_message(self.parent, message)

    def open(self):
        if not self._confirm_discard_unsaved_project():
            return

        path, _ = QFileDialog.getOpenFileName(
            parent=self.parent,
            caption='Open Project',
            directory=PROJECT_DIRECTORY,
            filter=PROJECT_FILE_FILTER,
        )
        if not path:
            return

        success, error_message = self.project_manager.open_project(path)
        if not success:
            dialog_message(
                self.parent,
                f'Failed to Open Project!\n{error_message}',
            )

    def _confirm_discard_unsaved_project(self):
        if self.project_manager.is_project_saved():
            return True

        answer = QMessageBox.question(
            self.parent,
            'R2ScriptEditor',
            'Current project is not saved.\n\n'
            'Do you want to proceed (all changes will be lost)?',
            QMessageBox.Yes | QMessageBox.No,
        )
        return answer == QMessageBox.Yes
