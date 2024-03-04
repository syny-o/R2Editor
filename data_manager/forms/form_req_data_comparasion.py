
from PyQt5.QtWidgets import QWidget, QTabWidget, QHBoxLayout, QListWidget, QListWidgetItem, QTextEdit, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCharFormat, QColor, QTextCursor
import difflib

from pyparsing import col

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
        self.setContentsMargins(0, 0, 0, 0)             
        self.uiLabelTitle.setText("Requirements downloaded successfully.")
        self.uiLabelTitle.setStyleSheet("")
        
        self.modules_data = modules_data

        self.uiBtnTitleBarClose.clicked.connect(self.close)
        self.uiBtnStatusBarClose.clicked.connect(self.close)
        self.uiBtnStatusBarClose.setText("Close")
        self.uiBtnOK.setVisible(False)
        


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

                    if len(module_path) > 40:
                        module_path = "..." + module_path[-40:]
                        
                    self.uiTabWidget.addTab(MyWidget(items), module_path)

    
        self.show() 




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
                    # user_data = ""
                    l = []
                    for i in range(len(columns_data)):
                        if columns_data[i] != module_data_new[identifier][i]:
                            # user_data += f"\nORIGINAL {module_columns[i]}:\n\n{columns_data[i]} \n\nACTUAL {module_columns[i]}:\n\n{module_data_new[identifier][i]}\n"
                            l.append((module_columns[i] ,columns_data[i], module_data_new[identifier][i]))
                    
                    item.setData(Qt.UserRole, l)
                            
                    # item.setData(Qt.UserRole, user_data)
                        
        
        return items
    






class MyWidget(QWidget):

    def __init__(self, items: list[QListWidgetItem]) -> None:
        super().__init__()

        self.format_diff = QTextCharFormat()
        self.format_diff.setForeground(QColor("red"))
        self.format_column_status = QTextCharFormat()
        self.format_column_status.setForeground(QColor("orange"))
        self.format_column_name = QTextCharFormat()
        self.format_column_name.setFontWeight(99)


        self.uiListWidget = QListWidget()
        self.uiListWidget.setMaximumWidth(300)
        for item in items:
            self.uiListWidget.addItem(item)

        self.uiTextEdit = QTextEdit()
        
        self.uiLayout = QHBoxLayout()
        self.uiLayout.setContentsMargins(0, 0, 0, 0)
        self.uiLayout.setSpacing(1)
        self.uiLayout.addWidget(self.uiListWidget)
        self.uiLayout.addWidget(self.uiTextEdit)

        self.setLayout(self.uiLayout)

        self.uiListWidget.currentRowChanged.connect(self._current_row_changed)
        self.uiListWidget.setCurrentRow(0)


    def _current_row_changed(self, row: int):
        self.uiTextEdit.clear()
        item = self.uiListWidget.item(row)
        # self.uiTextEdit.setText(item.data(Qt.UserRole))
        if item.data(Qt.UserRole) == "missing":
            self.uiTextEdit.setText("MISSING")
        elif item.data(Qt.UserRole) == "new":
            self.uiTextEdit.setText("NEW")
        else:
            for column, old, new in item.data(Qt.UserRole):
                self._display_differences(column, old, new)
                



    def _display_differences(self, column, string1, string2):
        
        diff = difflib.ndiff(string1, string2)

        cursor = self.uiTextEdit.textCursor()
        cursor.setCharFormat(self.format_column_name)
        cursor.insertText(f"{column}: ")
        cursor.setCharFormat(self.format_column_status)
        cursor.insertText(f"(original)\n\n") 
        cursor.setCharFormat(QTextCharFormat())

        for i, s in enumerate(diff):
            if s[0] == ' ':
                cursor.insertText(s[2:])
            elif s[0] == '-':
                cursor.setCharFormat(self.format_diff)
                cursor.insertText(s[2:])
                cursor.setCharFormat(QTextCharFormat())

        diff = difflib.ndiff(string1, string2)

        cursor.setCharFormat(self.format_column_name)
        cursor.insertText(f"\n\n{column}: ")
        cursor.setCharFormat(self.format_column_status)
        cursor.insertText(f"(updated)\n\n")
        cursor.setCharFormat(QTextCharFormat())
        for i, s in enumerate(diff):
            if s[0] == ' ':
                cursor.insertText(s[2:])
            elif s[0] == '+':
                cursor.setCharFormat(self.format_diff)
                cursor.insertText(s[2:])
                cursor.setCharFormat(QTextCharFormat()) 

        cursor.insertText("\n\n\n\n")   











        


        


