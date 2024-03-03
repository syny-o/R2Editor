import openpyxl

from PyQt5.QtWidgets import QWidget, QTabWidget, QHBoxLayout, QListWidget, QListWidgetItem, QTextEdit, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel
import ui

from ui.form_general_ui import Ui_Form

from data_manager.nodes.requirement_module import RequirementModule
from dialogs.dialog_message import dialog_message



class FormReqDataComparasion(QWidget, Ui_Form):

    def __init__(self, modules_data: dict[RequirementModule, tuple[dict, dict]]):
        super().__init__()
        self.setupUi(self)
        self.setWindowOpacity(0.95)  
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)        
        # self.setMaximumSize(400, 600)                 
        self.uiLabelTitle.setText("Requirements downloaded successfully.")
        self.uiLabelTitle.setStyleSheet("")
        
        self.modules_data = modules_data

        self.uiBtnTitleBarClose.clicked.connect(self.close)
        self.uiBtnStatusBarClose.clicked.connect(self.close)
        self.uiBtnStatusBarClose.setText("Close")
        self.uiBtnOK.setVisible(False)
        

        self.show() 

        if not self.modules_data:
            self.uiMainLayout_1.addWidget(QLabel("No differences were found."))
            self.resize(400, 100)

        else:
            self.uiMainLayout_1.addWidget(QLabel("The following differences were found:"))
            self.uiTabWidget = QTabWidget()
            self.uiMainLayout_2.addWidget(self.uiTabWidget)
            

            for module_path, (module_columns, module_data_old, module_data_new) in self.modules_data.items():
                
                if module_data_new != module_data_old:

                    items = self._get_key_diff(module_columns, module_data_old, module_data_new)
                    items += self._get_value_diff(module_columns, module_data_old, module_data_new)

                    self.uiTabWidget.addTab(MyWidget(items), module_path)

    




    def _get_key_diff(self, module_columns, module_data_old: dict, module_data_new: dict):
        items = []
        # get missing keys
        missing_keys = set(module_data_old.keys()) - set(module_data_new.keys())
        for missing_key in missing_keys:
            item = QListWidgetItem()
            item.setData(Qt.DisplayRole, missing_key)
            item.setData(Qt.UserRole, "missing")
            items.append(item)
            
        # get added keys
        added_keys = set(module_data_new.keys()) - set(module_data_old.keys())
        for added_key in added_keys:
            item = QListWidgetItem()
            item.setData(Qt.DisplayRole, added_key)
            item.setData(Qt.UserRole, "new")
            items.append(item)

        return items



    
    def _get_value_diff(self, module_columns, module_data_old: dict, module_data_new: dict):
        items = []
        for identifier, columns_data in module_data_old.items():
            if identifier in module_data_new:
                if columns_data != module_data_new[identifier]:
                    item = QListWidgetItem()
                    item.setData(Qt.DisplayRole, identifier)
                    items.append(item)
                    user_data = ""
                    for i in range(len(columns_data)):
                        if columns_data[i] != module_data_new[identifier][i]:
                            user_data += f"\nORIGINAL {module_columns[i]}:\n\n{columns_data[i]} \n\nACTUAL {module_columns[i]}:\n\n{module_data_new[identifier][i]}\n"
                    item.setData(Qt.UserRole, user_data)
                        
        
        return items




class MyWidget(QWidget):

    def __init__(self, items: list[QListWidgetItem]) -> None:
        super().__init__()

        self.uiListWidget = QListWidget()
        for item in items:
            self.uiListWidget.addItem(item)

        self.uiTextEdit = QTextEdit()
        
        self.uiLayout = QHBoxLayout()
        self.uiLayout.addWidget(self.uiListWidget)
        self.uiLayout.addWidget(self.uiTextEdit)

        self.setLayout(self.uiLayout)

        self.uiListWidget.currentRowChanged.connect(self._current_row_changed)
        self.uiListWidget.setCurrentRow(0)


    def _current_row_changed(self, row: int):
        self.uiTextEdit.clear()
        item = self.uiListWidget.item(row)
        self.uiTextEdit.setText(item.data(Qt.UserRole))











        


        


