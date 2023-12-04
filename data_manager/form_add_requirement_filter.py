from PyQt5.QtWidgets import QWidget, QLabel, QListWidget, QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPalette

from dialogs.dialog_message import dialog_message
from ui.form_general_ui import Ui_Form


class FormAddCoverageFilter(QWidget, Ui_Form):

   

    send_data = pyqtSignal(str, list)

    def __init__(self, data_manager, requirement_file_node):
        super().__init__()
        self.setupUi(self)
        self.setMinimumSize(1200, 600)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowOpacity(0.95)        
        self.uiLabelTitle.setText("Coverage Filter")
        self.uiBtnStatusBarClose.clicked.connect(self.close)
        self.uiBtnTitleBarClose.clicked.connect(self.close)
        self.uiBtnOK.clicked.connect(self._ok_clicked)

        self.requirement_file_node = requirement_file_node
        self.data_manager = data_manager
        self.send_data.connect(data_manager.receive_data_from_add_req_module_dialog)


        i = 0
        column_names_with_hint = []
        for column_name in self.requirement_file_node.columns_names:
            column_names_with_hint.append(f"column[{i}] => {column_name}")
            i += 1

        
        uiListWidgetColumns = QListWidget()
        uiListWidgetColumns.insertItems(0, column_names_with_hint)


        self.ui_le_final_filter =  QLineEdit()
        self.ui_le_final_filter.setMinimumWidth(600) 
        if f := self.requirement_file_node.coverage_filter:
            self.ui_le_final_filter.setText(str(f))
        self.ui_label_number_filtered_requirements = QLabel()
        self.ui_label_number_total_requirements = QLabel()
        self.ui_label_number_ignored_requirements = QLabel()
        self.uiMainLayout_1.addWidget(uiListWidgetColumns)
        self.uiMainLayout_2.addWidget(self.ui_le_final_filter)
        self.uiMainLayout_3.addWidget(self.ui_label_number_total_requirements)
        self.uiMainLayout_3.addWidget(self.ui_label_number_filtered_requirements)
        self.uiMainLayout_3.addWidget(self.ui_label_number_ignored_requirements)

        self.show()  


        



    def _ok_clicked(self):

        # SAVE FILTER TO REQUIREMENT FILE NODE

        filter_string = self.ui_le_final_filter.text().strip()
        
        self.requirement_file_node.coverage_filter = filter_string


        # SET COVERAGE (is_covered) TO ALL CHILDREN (REQUIREMENT NODES)
        IGNORED = 0
        FILTERED = 0
        TOTAL = 0
        

        def browse_children(parent_node, string):
                
            nonlocal IGNORED, FILTERED, TOTAL
            for row in range(parent_node.rowCount()):
                item = parent_node.child(row)


                try:
                    column = item.columns_data
                    evaluation = eval(string)
                    
                except Exception as ex:
                    self.requirement_file_node.coverage_check = False
                    self.requirement_file_node.coverage_filter = None
                    dialog_message(self, "Wrong Filter: " + str(ex))
                    break
                    
                    

                # TODO: "DRY" IS NOT RESPECTED --> SAME FUNCTION IS IN REQUIREMENT MODULE METHOD
                TOTAL += 1    
                if evaluation:
                    if item.reference not in self.requirement_file_node.ignore_list:
                        FILTERED += 1
                        item.update_coverage(False)
                    else:
                        IGNORED += 1
                        item.update_coverage(None)
                
                else:
                    item.update_coverage(None)

                browse_children(item, string)
            


        # filter_string = '(item.columns_data[0] == "SW - HSB" or item.columns_data[0] == "SW - SSM") and (("Approved" in item.columns_data[1] or item.columns_data[2] == "04 Approved") and item.columns_data[3] == "Requirement" and "EPBi Host" in item.columns_data[4])'
        # filter_string = '(column[0] == "SW - HSB" or column[0] == "SW - SSM") and (("Approved" in column[1] or column[2] == "04 Approved") and column[3] == "Requirement" and "EPBi Host" in column[4])'
    
        browse_children(self.requirement_file_node, filter_string)
        self.data_manager.update_data_summary()
        self.ui_label_number_total_requirements.setText("Total Items: " + str(TOTAL))
        self.ui_label_number_filtered_requirements.setText("Filtered Items: " + str(FILTERED))
        self.ui_label_number_ignored_requirements.setText("Ignored Items: " + str(IGNORED))
        if FILTERED:
            self.requirement_file_node.coverage_check = True
            # self.requirement_file_node.apply_coverage_filter()
            self.data_manager.create_dict_from_scripts_for_coverage_check()
            # self.data_manager.show_only_items_with_coverage(self.requirement_file_node)
        else:
            self.requirement_file_node.coverage_check = False
            self.requirement_file_node.remove_coverage_filter()

