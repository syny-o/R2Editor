from PyQt5.QtWidgets import QWidget, QPushButton, QToolBar, QVBoxLayout, QLabel, QListWidget, QLineEdit, QComboBox, QHBoxLayout, QInputDialog, QListWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QIcon

from ui.form_general_ui import Ui_Form

from components.my_list_widget import MyListWidget



from pathlib import Path
import json




columns_file_path_string = ".//doors//columns.json"


style = """
        QWidget {
            background-color: rgb(50, 50, 50);
            background-color: rgb(58, 89, 245);
            background-color: rgb(40, 40, 40);
            font-size: 14px;
            color: rgb(200, 200, 200);
            }

        QLineEdit {
            background-color: rgb(50, 50, 50);
            background-color: transparent;
            font-size: 14px;
            color: rgb(200, 200, 200);
            }            

        QComboBox, QLineEdit, QListWidget{
            padding: 5px;
            color: rgb(200, 200, 200);
            font-size: 14px;
            border: 1px solid rgb(180, 180, 180);
        }

        QPushButton {
            background-color: rgb(20, 20, 20);
            color: white;
            width: 100px;
            height: 30px;
            margin: 10px;
            padding: 5px;
            },

        QListWidget::item {
            padding: 5px;
            margin: 10px;
            },

        QListWidget::item:edited{
            padding: 0px;
            margin: 0px;
            },

        }
    """    

predefined_paths = [
    "/EPB CUSTOMER PROJECT Tailor/02 System Specifications/01 System Requirements/FSC",    
    "/EPB CUSTOMER PROJECT Tailor/02 System Specifications/01 System Requirements/SyRS",
    "/EPB CUSTOMER PROJECT Tailor/02 System Specifications/01 System Requirements/VC-EPBi",    

    "/EPB CUSTOMER PROJECT Tailor/02 System Specifications/02 System Design/Req2OEM",
    "/EPB CUSTOMER PROJECT Tailor/02 System Specifications/02 System Design/SyDesign",    
    "/EPB CUSTOMER PROJECT Tailor/02 System Specifications/02 System Design/TSC",

    "/EPB CUSTOMER PROJECT Tailor/021 System Interface Table/SIT",

    "/EPB CUSTOMER PROJECT Tailor/023 System Diagnostic Tables/DET - PBC",
    "/EPB CUSTOMER PROJECT Tailor/023 System Diagnostic Tables/DMT - PBC",    
    

    "/EPB CUSTOMER PROJECT Tailor/025 System Component Interfaces/CT_Datatypes",

    "/EPB CUSTOMER PROJECT Tailor/025 System Component Interfaces/PBC-CT",
    "/EPB CUSTOMER PROJECT Tailor/025 System Component Interfaces/SSM_PB-CT",
    "/EPB CUSTOMER PROJECT Tailor/025 System Component Interfaces/HSB-CT",
    "/EPB CUSTOMER PROJECT Tailor/025 System Component Interfaces/ESS-CT",
    "/EPB CUSTOMER PROJECT Tailor/025 System Component Interfaces/PWI-CT",   

    "/EPB CUSTOMER PROJECT Tailor/03 Software/010 SwRS EPB" 

]    


predefined_columns = [
    "Object Text",    
    "Object Text_DXL",    
    "010_Object Type",
    "011_Object State",
    "011_DXL_Object State",
    "820_EPBi Variant",
    "050_Test Department",
    "840_Responsible Stakeholder",
    "000_Core_Veh-Var",
    "Project1 Veh-Var1",
    "100_Minimal Value",
    "102_Maximal Value",
    "110_Technical Comment",
    "303_Unit",
    "TRW DTC Name",
    "TRW Func Actuator Apply Left",
    "TRW Func Actuator Apply Right",
    "TRW Func Actuator Release Left",
    "TRW Func Actuator Release Right",
    "TRW Func Dynamic Apply RWU",
    "TRW Func Auto Adjust",
    "TRW Func GDA",
    "TRW Func RAR",
    "TRW Func HTR",
    "TRW Func Rollerbench Apply"    
    ]








class FormAddModule(QWidget, Ui_Form):

   

    send_data = pyqtSignal(str, list)

    def __init__(self, data_manager):
        super().__init__()
        self.setupUi(self)
        self.setWindowOpacity(0.95)           
        self.uiLabelTitle.setText("Add Module")
        self.uiBtnTitleBarClose.clicked.connect(self.close)
        self.uiBtnStatusBarClose.clicked.connect(self.close)
        self.uiBtnOK.clicked.connect(self._ok_clicked)

        
        self.input = QInputDialog(self)
        
        # self.input.setStyleSheet("QLineEdit { color: white; background-color: black; } QPushButton { background-color: red; color: blue; }")

        self.data_manager = data_manager
        self.send_data.connect(data_manager.receive_data_from_add_req_module_dialog)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)
        
        # self.setWindowOpacity(0.9)
        self.setMinimumSize(1024, 768)

        self.uiLineEditCustomer = QLineEdit("")
        self.uiLineEditCustomer.setPlaceholderText("CUSTOMER")
        self.uiLineEditProject = QLineEdit("")
        self.uiLineEditProject.setPlaceholderText("PROJECT")
        








        # uiBtnCancel = QPushButton("Close")
        # uiBtnCancel.clicked.connect(self.close)
        # uiBtnOK = QPushButton("Insert Module")
        # uiBtnOK.clicked.connect(self._ok_clicked)

        uiBtnInsertColumn = QPushButton("New")
        uiBtnInsertColumn.clicked.connect(self._insert_column)
        uiBtnRemoveColumn = QPushButton("Remove")
        

        uiBtnClearAllFinal = QPushButton("Remove All")
        uiBtnClearAllFinal.clicked.connect(self._remove_all)
        uiBtnRemoveColumnFinal = QPushButton("Remove")
               


        # uiToolbar = QToolBar()
        # uiToolbar.addWidget(uiBtnOK)
        # uiToolbar.addWidget(uiBtnCancel)

        # uiTitleBarLayout = QHBoxLayout()
        # uiTitleBarLayout.setContentsMargins(0,0,0,20)
        # uiTitleBarLayout.setSpacing(0)
        # uiTitleBarLayout.addWidget(QLabel("Add New Module"))
        # uiBtnClose = QPushButton("Close")
        # uiBtnClose.setIcon(QIcon(u"ui/icons/20x20/cil-x.png"))
        
        # uiBtnClose.setStyleSheet("background-color: transparent;")
        # uiBtnClose.setMaximumSize(50,30)
        # uiBtnClose.setMinimumSize(100,50)
        # uiBtnClose.setCursor(Qt.PointingHandCursor)

        # uiTitleBarLayout.addWidget(uiBtnClose)
        # uiBtnClose.clicked.connect(lambda: print("CLIOCEKD"))


        self.uiComboModuleLocation = QComboBox()
        self.uiComboModuleLocation.setEditable(True)
        self.uiComboModuleLocation.insertItems(0, predefined_paths)


        self.uiListFinalColumns = MyListWidget()
        self.uiListFinalColumns.setDefaultDropAction(Qt.MoveAction)

        self.uiListPredefinedColumns = MyListWidget()
        self.uiListPredefinedColumns.setAcceptDrops(False)


        uiBtnRemoveColumnFinal.clicked.connect(lambda: self._remove_column(self.uiListFinalColumns))
        uiBtnRemoveColumn.clicked.connect(lambda: self._remove_column(self.uiListPredefinedColumns))
        

        if Path(columns_file_path_string).exists():
            try:
                with open(columns_file_path_string, "r") as file:
                    data_for_import = json.load(file)

                project = data_for_import.get("project")
                columns = data_for_import.get("columns")
                customer = data_for_import.get("customer")

                self.uiLineEditCustomer.setText(customer)
                self.uiLineEditProject.setText(project)
                self.uiListPredefinedColumns.insertItems(0, columns)

            except Exception as e:
                print(e)
        
        else:
            self.uiListPredefinedColumns.addItems(predefined_columns)

        for index in range(self.uiListPredefinedColumns.count()):
            item = self.uiListPredefinedColumns.item(index)
            item.setFlags(item.flags() | Qt.ItemIsEditable)


        uiLineEditsLayout = QHBoxLayout()
        uiLineEditsLayout.addWidget(self.uiLineEditCustomer)
        uiLineEditsLayout.addWidget(self.uiLineEditProject)
        
        uiBtnLayoutPredefined = QVBoxLayout()
        uiBtnLayoutPredefined.setAlignment(Qt.AlignCenter)
        # uiBtnLayoutPredefined.addWidget(uiBtnInsertColumn)
        # uiBtnLayoutPredefined.addWidget(uiBtnRemoveColumn)
        uiBtnLayoutPredefined.addWidget(QLabel("Predefined Columns:"))
        uiBtnLayoutPredefined.addWidget(self.uiListPredefinedColumns)
        uiBtnLayoutPredefined.setSpacing(6)

        uiBtnLayoutFinal = QVBoxLayout()
        uiBtnLayoutFinal.setAlignment(Qt.AlignCenter)
        # uiBtnLayoutFinal.addWidget(uiBtnClearAllFinal)
        # uiBtnLayoutFinal.addWidget(uiBtnRemoveColumnFinal)
        uiBtnLayoutFinal.addWidget(QLabel("Actual Columns:"))
        uiBtnLayoutFinal.addWidget(self.uiListFinalColumns)
        uiBtnLayoutFinal.setSpacing(6)
        
        uiListLayout = QHBoxLayout()
        uiListLayout.addLayout(uiBtnLayoutPredefined)
        
        # uiListLayout.addWidget(self.uiListFinalColumns)
        uiListLayout.addLayout(uiBtnLayoutFinal)
        


        self.uiMainLayout_1.addWidget(QLabel("Customer/Project:"))
        self.uiMainLayout_1.addLayout(uiLineEditsLayout)
        self.uiMainLayout_2.addWidget(QLabel("Module Path (Case Sensitive):"))
        self.uiMainLayout_2.addWidget(self.uiComboModuleLocation)
        self.uiMainLayout_3.addLayout(uiListLayout)


        self.uiLineEditCustomer.textChanged.connect(self._update_customer_project_name)
        self.uiLineEditProject.textChanged.connect(self._update_customer_project_name)

        self.show()  

        self._update_customer_project_name()


    def _update_customer_project_name(self):

        customer_name = self.uiLineEditCustomer.text()
        project_name = self.uiLineEditProject.text()

        paths = [path.replace("CUSTOMER", customer_name).replace("PROJECT", project_name) for path in predefined_paths]



        self.uiComboModuleLocation.clear()
        self.uiComboModuleLocation.addItems(paths)        
    


    def _insert_column(self):
        column_name, ok = self.input.getText(
            None, 
            "Add Column", 
            f"Column Name: ")
        if ok and column_name:
            column_item = QListWidgetItem(column_name)
            column_item.setFlags(column_item.flags() | Qt.ItemIsEditable)
            self.uiListPredefinedColumns.addItem(column_item)
            
    
    def _remove_column(self, listwidget):
        row = listwidget.currentRow()
        listwidget.takeItem(row)

    def _remove_all(self):
        for _ in range(self.uiListFinalColumns.count()):
            self.uiListFinalColumns.takeItem(0)

    def _ok_clicked(self):
        path = self.uiComboModuleLocation.currentText()
        columns = self.uiListFinalColumns.get_all_items()

        # Form check if all mandatory items are filled
        if self.uiListFinalColumns.count() == 0:
            self.uiListFinalColumns.setStyleSheet('border-color: red')

        elif self.uiComboModuleLocation.currentText() == '':
            self.uiComboModuleLocation.setStyleSheet('border-color: red')

        else:

            self.send_data.emit(path, columns)
            self.uiListFinalColumns.setStyleSheet('border-color: rgb(100,100,100);')
            self.uiComboModuleLocation.setStyleSheet('border-color: rgb(100,100,100);')
            self._form_save()

            # self.close()



    def _form_save(self) -> None:

        data_2_save = self._provide_data_for_export()
        
        with open(columns_file_path_string, "w+") as file:
                json.dump(data_2_save, file)



    
    def _provide_data_for_export(self):
        columns = []
        for row in range(self.uiListPredefinedColumns.count()):
            columns.append(self.uiListPredefinedColumns.item(row).text())


        data = dict(
            customer = self.uiLineEditCustomer.text(),
            project = self.uiLineEditProject.text(),
            columns = columns,
        )

        return data


