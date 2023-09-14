from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from ui.ui_form_find_replace import Ui_Form

import os, re, stat


def find_replace_in_folder(folder_path, original_string, new_string):

    summary_text = ""

    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith((".par", ".txt")):

                full_path = (root + '\\' + filename)
                
                # Check if the file ReadOnly and if so, unlock it:
                is_read_only = not(os.access(full_path, os.W_OK))
                if is_read_only:
                    os.chmod(full_path, stat.S_IWRITE)

                with open(full_path, 'r') as f:
                    file_text = f.read()
                
                # method subn returns tuple: (new text, number of replacements)
                new_file_text, count = re.subn(original_string, new_string, file_text)

                with open(full_path, 'w') as f:
                    f.write(new_file_text)

                # lock the file to be ReadOnly back again
                if is_read_only:
                    os.chmod(full_path, stat.S_IREAD)
                
                summary_text += f'{full_path} has been replaced {count}x times'
            
    return summary_text


# def find_replace_in_file(file_path, original_string, new_string):
#     is_read_only = not(os.access(file_path, os.W_OK))
#     if is_read_only:
#         os.chmod(file_path, stat.S_IWRITE)

#     with open(file_path, 'r') as f:
#         file_text = f.read()
    
#     # method subn returns tuple: (new text, number of replacements)
#     new_file_text, count = re.subn(original_string, new_string, file_text)

#     with open(file_path, 'w') as f:
#         f.write(new_file_text)

#     # lock the file to be ReadOnly back again
#     if is_read_only:
#         os.chmod(file_path, stat.S_IREAD)
    
#     summary_text += f'{file_path} has been replaced {count}x times'
            
#     return summary_text


def find_replace_in_text(text, original_string, new_string):
    new_text = text.replace(original_string, new_string)
    return new_text




class FindAndReplace(QWidget, Ui_Form):
    """
    This "window" will appear Find and Replace context menu item clicked
    """


    def __init__(self, folder_path=None, actual_text_edit=None):
        super().__init__()
        self.setupUi(self)
        # self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.ui_btn_close.clicked.connect(self.close)
        self.ui_btn_run.clicked.connect(self.run_clicked)

        self.folder_path = folder_path
        self.actual_text_edit = actual_text_edit

        if self.actual_text_edit:
            tc = self.actual_text_edit.textCursor()
            if tc.selectedText():
                self.ui_le_original_string.setText(tc.selectedText())



    def run_clicked(self):

        original_string = self.ui_le_original_string.text()
        new_string = self.ui_le_new_string.text()

        case_sensitive = self.ui_cb_case_sensitive.isChecked()
        whole_word = self.ui_cb_whole_word.isChecked()

        #  Form check if all mandatory items are filled
        if self.ui_le_original_string.text() == '':
            self.ui_le_original_string.setStyleSheet('border: 1px solid red')

        else:
            if self.folder_path:
                summary_text = find_replace_in_folder(self.folder_path, original_string, new_string)
                self.ui_te_summary.setText(summary_text)
            elif self.actual_text_edit:
                text = self.actual_text_edit.toPlainText()
                new_text = find_replace_in_text(text, original_string, new_string)
                self.actual_text_edit.setPlainText(new_text)

