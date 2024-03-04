import openpyxl

from PyQt5.QtWidgets import QWidget, QCheckBox, QVBoxLayout, QFileDialog, QTreeView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel

from ui.form_general_ui import Ui_Form

from data_manager.nodes.requirement_module import RequirementModule
from dialogs.dialog_message import dialog_message



class FormExportModule(QWidget, Ui_Form):

    def __init__(self, requirement_module: RequirementModule, tree: QTreeView, model: QStandardItemModel):
        super().__init__()
        self.setupUi(self)
        self.setWindowOpacity(0.95)  
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)        
        self.setMaximumSize(400, 600)                 
        self.uiLabelTitle.setText("Export")
        self.uiLabelTitle.setStyleSheet("")
        
        self.requirement_module = requirement_module 
        self.tree = tree
        self.model = model
        self.columns_names_checkboxes = []
        self.columns_names_2_export = []
        self.columns_indexes = []
        self.include_note = False

        self.uiBtnTitleBarClose.clicked.connect(self.close)
        self.uiBtnStatusBarClose.clicked.connect(self.close)
        self.uiBtnStatusBarClose.setText("Close")
        self.uiBtnOK.setText("Export")
        self.uiBtnOK.clicked.connect(self._export_clicked)
        
        self._generate_layout()

        self.show() 







    def _export_clicked(self):
        self._export_file()




    def _generate_layout(self):
        self.uiMainLayout_3.setSpacing(10)
        self._generate_layout_for_columns()
        

    def _generate_layout_for_columns(self):
        uiLayoutColumns = QVBoxLayout()
        for column in self.requirement_module.columns_names_backup:
            uiCheckboxColumn = QCheckBox(column)
            self.columns_names_checkboxes.append(uiCheckboxColumn)
            uiLayoutColumns.addWidget(uiCheckboxColumn)

        self.uiCheckboxNote = QCheckBox("Include user note")

        self.uiMainLayout_2.addLayout(uiLayoutColumns)
        self.uiMainLayout_3.addWidget(self.uiCheckboxNote)



    def _prepare_indexes(self):
        self.columns_indexes.clear()
        for (index, checkbox) in enumerate(self.columns_names_checkboxes):
            if checkbox.isChecked():
                self.columns_indexes.append(index) 


    def _prepare_note(self):
        if self.uiCheckboxNote.isChecked():
            self.include_note = True       

    
    def _prepare_header(self):
        header = ['Identifier', ]
        header += [self.requirement_module.columns_names_backup[i] for i in self.columns_indexes]
        if self.include_note:
            header += ['User note',]

        return header


    def _prepare_data(self):
        
        items_2_export = []
        data_2_export = []


        def _browse_all_children(node):
            for row in range(node.rowCount()):
                node_child = node.child(row)
                if node_child:
                    if not self.tree.isRowHidden(row, node.index()) and not node_child.hasChildren():
                        items_2_export.append(node_child)
                _browse_all_children(node_child)
        
        _browse_all_children(self.requirement_module)

        for item in items_2_export:
            one_data = [item.reference, ]
            for index in self.columns_indexes:
                one_data.append(item.columns_data[index])
            if self.include_note:
                one_data.append(item.note)
            
            data_2_export.append(one_data)

        return data_2_export
            
            

        
        



    

    

    
    def _generate_excel_sheet(self):
        self._prepare_note()
        self._prepare_indexes()
        header = self._prepare_header()
        data = self._prepare_data()

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(header)
        for row in data:
            sheet.append(row)
        
        return workbook
        



    
    def _export_file(self):

        path, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption='Export',
            filter="MS Excel (*.xlsx)"
        )

        if not path:
            return

        workbook = self._generate_excel_sheet()
        try:
            workbook.save(path)
            dialog_message(self, "The file has been exported successfully.", "Success")
        except PermissionError:
            dialog_message(self, "The file is already open. Please close it and try again.", "Error")
            return
        except Exception as e:
            dialog_message(self, str(e), "Error")
            return





        


        


