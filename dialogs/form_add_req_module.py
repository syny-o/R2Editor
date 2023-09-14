from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from ui.ui_form_add_req_module import Ui_Form


class AddRequirementsModule(QWidget, Ui_Form):
    """
    This "window" will appear after request for new req module is raised
    """
    # SIGNAL DEFINITION
    send_data = pyqtSignal(str, list, bool)

    def __init__(self, model_editor):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.send_data.connect(model_editor.receive_data_from_add_req_module_dialog)

        self.ui_btn_cancel.clicked.connect(self.close)
        self.ui_btn_ok.clicked.connect(self.ok_clicked)


    def ok_clicked(self):
        module_path = self.ui_le_module_path.text()
        columns_string = self.ui_le_module_columns.text().strip()
        columns = columns_string.split(',')

        coverage_check = self.ui_cb_check_coverage.isChecked()

        #  Form check if all mandatory items are filled
        if self.ui_le_module_path.text() == '':
            self.ui_le_module_path.setStyleSheet('border: 1px solid red')

        if self.ui_le_module_columns.text() == '':
            self.ui_le_module_columns.setStyleSheet('border: 1px solid red')

        else:

            self.send_data.emit(module_path, columns, coverage_check)

            self.close()


