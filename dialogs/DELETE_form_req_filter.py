from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit
from PyQt5.QtCore import Qt, pyqtSignal
from ui.ui_form_req_filter import Ui_Form

from dialogs.dialog_message import dialog_message


class RequirementFilter(QWidget, Ui_Form):
    """
    This "window" will appear after request for filter is raised
    """
    # SIGNAL DEFINITION
    send_data = pyqtSignal(str)

    def __init__(self, data_manager, req_file_node):
        super().__init__()
        self.setupUi(self)
        # self.setWindowModality(Qt.ApplicationModal)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Create Filter")

        self.requirement_file_node = req_file_node
        self.data_manager = data_manager

        self.send_data.connect(data_manager.receive_data_from_req_filter_dialog)

        self.ui_btn_cancel.clicked.connect(self.close)
        self.ui_btn_ok.clicked.connect(self._ok_clicked)

        self._generate_layout()



    def _generate_layout(self):
        # self.list_of_line_edits = []
        # columns_names = self.req_file_node.columns_names
        # current_filter = self.req_file_node.coverage_filter
        # for i in range(len(columns_names)):
        #     self.ui_layout_column_names.addWidget(QLabel(columns_names[i]))
        #     temp_line_edit = QLineEdit()
        #     if current_filter:
        #         temp_line_edit.setText(current_filter[i])
        #     self.ui_layout_column_data.addWidget(temp_line_edit)
        #     self.list_of_line_edits.append(temp_line_edit)


        self.ui_le_final_filter =  QLineEdit()
        self.ui_le_final_filter.setMinimumWidth(1000) 
        if f := self.requirement_file_node.coverage_filter:
            self.ui_le_final_filter.setText(str(f))
        self.ui_label_number_filtered_requirements = QLabel()
        self.ui_label_number_total_requirements = QLabel()
        self.ui_label_number_ignored_requirements = QLabel()
        self.ui_layout_column_names.addWidget(self.ui_le_final_filter)
        self.ui_layout_column_names.addWidget(self.ui_label_number_total_requirements)
        self.ui_layout_column_names.addWidget(self.ui_label_number_ignored_requirements)
        self.ui_layout_column_names.addWidget(self.ui_label_number_filtered_requirements)
        



    def _ok_clicked(self):

        # filters_in_columns = [le.text() for le in self.list_of_line_edits]

        # self.send_data.emit(filters_in_columns)
        # self.send_data.emit(self.ui_le_final_filter.text().strip())

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
                        # if TOTAL % 50 == 0:
                        #     item.update_coverage(False)
                        # else:
                        #     item.update_coverage(True)
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
        self.ui_label_number_total_requirements.setText("Total Items: " + str(TOTAL))
        self.ui_label_number_filtered_requirements.setText("Filtered Items: " + str(FILTERED))
        self.ui_label_number_ignored_requirements.setText("Ignored Items: " + str(IGNORED))
        if FILTERED:
            self.requirement_file_node.coverage_check = True
            # self.data_manager.show_only_items_with_coverage(self.requirement_file_node)
        else:
            self.requirement_file_node.coverage_check = False
        # print("FILTERED:  " + str(FILTERED))


