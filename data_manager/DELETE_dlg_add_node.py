from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from ui.ui_form_add_node import Ui_Form


class DlgAddNode(QWidget, Ui_Form):
    """
    This "window" will appear after request for new node is raised
    """
    # SIGNAL DEFINITION
    # send_data = pyqtSignal(str, str, str, str, str, str, str, str, str)
    send_data = pyqtSignal(dict)

    def __init__(self, data_manager, condition_data=None, dspace_data=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        

        self.send_data.connect(data_manager.receive_data_from_add_node_dialog)
        self.ui_btn_cancel.clicked.connect(self.close)
        self.ui_btn_ok.clicked.connect(self.ok_clicked)
        self.ui_le_dspace_path.editingFinished.connect(self.handle_dspace_input)

        if condition_data:
            self.frame_dspace.setVisible(False)
            condition = condition_data[0]
            value = condition_data[1]
            self.ui_le_condition.setText(condition)
            if condition: self.ui_le_condition.setEnabled(False)
            self.ui_le_value.setText(value)
            if value: self.ui_le_value.setEnabled(False)

        if dspace_data:
            self.frame_condition.setVisible(False)
            definition = dspace_data
            self.ui_le_dspace_definition.setText(definition)
            self.ui_le_dspace_definition.setEnabled(False)
            

    def ok_clicked(self):
        condition = self.ui_le_condition.text()
        value = self.ui_le_value.text()
        test_step_name = self.ui_le_test_step_name.text()
        test_step_action = self.ui_le_test_step_action.text()
        test_step_comment = self.ui_le_test_step_comment.text()
        test_step_nominal = self.ui_le_test_step_nominal.text()

        dspace_name = self.ui_le_dspace_name.text()
        dspace_value = self.ui_le_dspace_value.text()
        dspace_path = self.ui_le_dspace_path.text()

        # Form check if all mandatory items are filled
        # --> for Condition items:
        if self.frame_condition.isVisible():
            if self.validated_inputs(self.ui_le_condition, self.ui_le_value, self.ui_le_test_step_action):
                self.send_data.emit(dict(
                    cond_data = dict(
                        condition=condition,
                        value=value,
                        test_step_name=test_step_name,  
                        test_step_comment=test_step_comment, 
                        test_step_nominal=test_step_nominal, 
                        test_step_action=test_step_action)))

                self.close()

        # --> for DSpace items:
        else:
            if self.validated_inputs(self.ui_le_dspace_name, self.ui_le_dspace_path, self.ui_le_dspace_value):
                self.send_data.emit(dict(
                    dspace_data = dict(
                        dspace_name=dspace_name, 
                        dspace_value=dspace_value, 
                        dspace_path=dspace_path)))

                self.close()


    def handle_dspace_input(self):
        """
        1. strip "platform.." once whole path of variable is pasted directly from Control Desk
        2. automatically extract variable name from this path and put it into variable name line edit
        3. automatically put variable value as None

        Possible ds_path_text values:
            'DS1006()://Model Root/CD In Sub/BCM_Sub/BCM_COMMAND_Disable/Value'
            'DS1006()://Model Root/CD In Sub/ORC_Sub/AIRBAG1_Sub/SBR1RowCentralSeatSts/Value'
            'DS1006()://BusSystems/CAN/Vehicle_CAN2/AIRBAG1/TX/SBR1RowCentralSeatSts'
        """
        
        # load pasted text from line edit, strip quotes and DS1006 and send it back to line edit 
        ds_path_text = self.ui_le_dspace_path.text()
        ds_path_text = ds_path_text.strip("'").lstrip("DS1006()://")        
        self.ui_le_dspace_path.setText(ds_path_text)

        # extract dspace variable name from path
        last_part = ds_path_text.split("/")[-1]
        try:
            pre_last_part = ds_path_text.split("/")[-2]
        except IndexError:
            pre_last_part = ""

        # send final variable name to line edit
        if last_part == "Value":  # its CD block --> Model Root...
            self.ui_le_dspace_name.setText(pre_last_part)
        else:  # its CD variable --> BusSystems...
            self.ui_le_dspace_name.setText(last_part)

        
        # send None as default value to line edit
        self.ui_le_dspace_value.setText("None")


    def validated_inputs(self, *line_edits):
        all_validated = True
        for le in line_edits:
            if not le.text():
                le.setStyleSheet('border: 1px solid red')
                all_validated = False
            else:
                le.setStyleSheet('border: 1px solid grey')
        return all_validated
