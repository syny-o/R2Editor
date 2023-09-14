from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal
from ui.ui_form_req_filter import Ui_Form


class RequirementFilter(QWidget, Ui_Form):
    """
    This "window" will appear after request for filter is raised
    """
    # SIGNAL DEFINITION
    send_data = pyqtSignal(list)

    def __init__(self, model_editor, req_file_node):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.req_file_node = req_file_node

        self.send_data.connect(model_editor.receive_data_from_req_filter_dialog)

        self.ui_btn_cancel.clicked.connect(self.close)
        self.ui_btn_ok.clicked.connect(self.ok_clicked)

        self.generate_layouts()

    def generate_layouts(self):
        self.list_of_line_edits = []
        columns_names = self.req_file_node.columns_names
        for c in columns_names:
            self.ui_layout_column_names.addWidget(QLabel(c))
            temp_line_edit = QLineEdit()
            self.ui_layout_column_data.addWidget(temp_line_edit)
            self.list_of_line_edits.append(temp_line_edit)

    def ok_clicked(self):

        filters_in_columns = [le.text() for le in self.list_of_line_edits]

        self.send_data.emit(filters_in_columns)

        self.close()


