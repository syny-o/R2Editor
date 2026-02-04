from PyQt5.QtWidgets import (
    QWidget, QPushButton, QVBoxLayout, QLabel,
    QListWidget, QLineEdit, QHBoxLayout, QInputDialog, QListWidgetItem
)
from PyQt5.QtCore import Qt, pyqtSignal
from ui.form_general_ui import Ui_Form
import components.my_list_widget

from pathlib import Path
import json

columns_file_path_string = ".//doors//columns.json"


class FormAddModule(QWidget, Ui_Form):

    send_data = pyqtSignal(str, list)

    def __init__(self, data_manager):
        from importlib import reload
        reload(components.my_list_widget)

        super().__init__()
        self.setupUi(self)

        self.uiLabelTitle.setText("Add Module")
        self.uiBtnTitleBarClose.clicked.connect(self.close)
        self.uiBtnStatusBarClose.clicked.connect(self.close)
        self.uiBtnOK.clicked.connect(self._ok_clicked)
        self.uiBtnOK.setText("Add")

        self.input = QInputDialog(self)

        self.data_manager = data_manager
        self.send_data.connect(data_manager.receive_data_from_add_req_module_dialog)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setMaximumSize(800, 300)

        self.uiComboModuleLocation = QLineEdit()

        # List widgets
        self.uiListFinalColumns = components.my_list_widget.MyListWidget()
        self.uiListFinalColumns.setDefaultDropAction(Qt.MoveAction)

        self.uiListPredefinedColumns = components.my_list_widget.MyListWidget()
        self.uiListPredefinedColumns.setAcceptDrops(False)

        # Buttons
        uiBtnRemoveColumn = QPushButton("Remove")
        uiBtnRemoveColumn.clicked.connect(lambda: self._remove_column(self.uiListPredefinedColumns))

        uiBtnRemoveColumnFinal = QPushButton("Remove")
        uiBtnRemoveColumnFinal.clicked.connect(lambda: self._remove_column(self.uiListFinalColumns))

        # Layout: Predefined
        uiLayoutPredefined = QVBoxLayout()
        uiLayoutPredefined.setAlignment(Qt.AlignCenter)
        uiLayoutPredefined.addWidget(QLabel("Predefined Columns:"))
        uiLayoutPredefined.addWidget(self.uiListPredefinedColumns)

        # Layout: Final
        uiLayoutFinal = QVBoxLayout()
        uiLayoutFinal.setAlignment(Qt.AlignCenter)
        uiLayoutFinal.addWidget(QLabel("Actual Columns:"))
        uiLayoutFinal.addWidget(self.uiListFinalColumns)

        # Combined list layout
        uiListLayout = QHBoxLayout()
        uiListLayout.addLayout(uiLayoutPredefined)
        uiListLayout.addLayout(uiLayoutFinal)

        # Add to UI
        self.uiMainLayout_2.addWidget(QLabel("Module Path (Case Sensitive):"))
        self.uiMainLayout_2.addWidget(self.uiComboModuleLocation)

        self.show()

    # -------------------------------
    # List operations
    # -------------------------------

    def _insert_column(self):
        column_name, ok = self.input.getText(None, "Add Column", "Column Name:")
        if ok and column_name:
            item = QListWidgetItem(column_name)
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.uiListPredefinedColumns.addItem(item)

    def _remove_column(self, listwidget):
        row = listwidget.currentRow()
        if row >= 0:
            listwidget.takeItem(row)

    def _remove_all(self):
        self.uiListFinalColumns.clear()

    # -------------------------------
    # OK button handler
    # -------------------------------

    def _ok_clicked(self):
        path = self.uiComboModuleLocation.text()
        columns = self.uiListFinalColumns.get_all_items()

        if not path:
            self.uiComboModuleLocation.setStyleSheet("border-color: red")
            return

        self.send_data.emit(path, columns)
        self.uiComboModuleLocation.setStyleSheet("border-color: rgb(100,100,100)")
        self._form_save()
        self.uiComboModuleLocation.clear()

    # -------------------------------
    # Save predefined column list
    # -------------------------------

    def _form_save(self):
        data = self._provide_data_for_export()
        with open(columns_file_path_string, "w+") as file:
            json.dump(data, file)

    def _provide_data_for_export(self):
        columns = [
            self.uiListPredefinedColumns.item(i).text()
            for i in range(self.uiListPredefinedColumns.count())
        ]

        return {"customer": "", "project": "", "columns": columns}