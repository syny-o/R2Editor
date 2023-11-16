import os, re, stat

from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QCheckBox, QTextEdit
from PyQt5.QtCore import Qt, pyqtSignal

from dialogs.dialog_message import dialog_message
from ui.form_general_ui import Ui_Form
from components.reduce_path_string import reduce_path_string


def find_replace_in_folder(folder_path, original_string, new_string, case_sensitive, whole_word):

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

                if whole_word:
                    original_string = rf"\b{original_string}\b"

                if case_sensitive:
                    new_file_text, count = re.subn(fr"{original_string}", new_string, file_text)
                else:
                    new_file_text, count = re.subn(original_string, new_string, file_text, flags=re.IGNORECASE)

                with open(full_path, 'w') as f:
                    f.write(new_file_text)

                # lock the file to be ReadOnly back again
                if is_read_only:
                    os.chmod(full_path, stat.S_IREAD)
                
                if count:
                    summary_text += f'{reduce_path_string(full_path)} was replaced {count}x \n'
    
    if not summary_text:
        summary_text = "No matches found!"

            
    return summary_text



def find_replace_in_text(text, original_string, new_string):
    new_text = text.replace(original_string, new_string)
    return new_text




class FindAndReplace(QWidget, Ui_Form):
    """
    This "window" will appear Find and Replace context menu item clicked
    """


    def __init__(self, folder_path):
        super().__init__()
        self.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(1000, 800)
        self.setWindowOpacity(0.95)           
        self.uiLabelTitle.setText(f"Find and Replace in {folder_path}")
        self.uiBtnTitleBarClose.clicked.connect(self.close)
        self.uiBtnStatusBarClose.clicked.connect(self.close)
        self.uiBtnOK.clicked.connect(self._run_clicked)        

        self.folder_path = folder_path

        self.uiLineEditOriginalString = QLineEdit()
        self.uiLineEditOriginalString.setPlaceholderText("Find")
        self.uiLineEditNewString = QLineEdit()
        self.uiLineEditNewString.setPlaceholderText("Replace")

        self.uiCheckBoxCaseSensitive = QCheckBox("Case Sensitive")
        self.uiCheckBoxWholeWord = QCheckBox("Match Word")

        self.uiTextEditSummary = QTextEdit()

        self.uiMainLayout_1.addWidget(self.uiLineEditOriginalString)
        self.uiMainLayout_1.addWidget(self.uiLineEditNewString)

        self.uiMainLayout_2.addWidget(self.uiCheckBoxCaseSensitive)
        self.uiMainLayout_2.addWidget(self.uiCheckBoxWholeWord)

        self.uiMainLayout_3.addWidget(self.uiTextEditSummary)








    def _run_clicked(self):

        original_string = self.uiLineEditOriginalString.text()
        new_string = self.uiLineEditNewString.text()

        case_sensitive = self.uiCheckBoxCaseSensitive.isChecked()
        whole_word = self.uiCheckBoxWholeWord.isChecked()

        #  Form check if all mandatory items are filled
        if self.uiLineEditOriginalString.text() == '':
            self.uiLineEditOriginalString.setStyleSheet('border: 1px solid red')

        else:
            try:
                summary_text = find_replace_in_folder(self.folder_path, original_string, new_string, case_sensitive, whole_word)
                self.uiTextEditSummary.setText(summary_text)

            except Exception as e:
                dialog_message(self, str(e))

