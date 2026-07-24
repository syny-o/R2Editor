from pathlib import Path

from PyQt5.QtWidgets import (
    QLabel,
    QPlainTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QWidget,
)
from PyQt5.QtCore import Qt, pyqtSlot, QThreadPool

from ui.form_general_ui import Ui_Form
from components.reduce_path_string import reduce_path_string

from dialogs.dialog_message import dialog_message
from file_browser.script_normalizer import normalize_script_text
from file_browser.script_normalization_worker import (
    ScriptNormalizationWorker,
)





class ScriptNormReport(QWidget, Ui_Form):
    """
    This "window" will appear after successfull SCRIPT/FOLDER normalisation is finished
    """


    def __init__(self, path):
        super().__init__()
        self.setupUi(self)
        # self.uiMainLayout_1.setContentsMargins(0,0,0,0)
        self.uiMainLayout_2.setContentsMargins(0,0,0,0)
        self.uiMainLayout_3.setContentsMargins(0,0,0,0)
        self.uiMainLayout_4.setContentsMargins(0,0,0,0)
        # self.uiMainLayout_5.setContentsMargins(0,0,0,0)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(1024, 768)
        self.setWindowOpacity(0.95)  
        self.uiBtnOK.setVisible(False)         
        self.uiLabelTitle.setText(f"VDA Normalisation: {path}")
        self.uiBtnTitleBarClose.clicked.connect(self.close)
        self.uiBtnStatusBarClose.clicked.connect(self.close)
        # self.uiBtnOK.clicked.connect(self.close)     
        self.uiBtnStatusBarClose.setEnabled(False) 
        self.uiBtnStatusBarClose.setText("Close") 


        # THREAD CONFIGURATION
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)



        self.path = path

        if Path(self.path).is_file():
            results = self._normalise_one_script()
            self._create_ui_output_from_one_script(results)
            self.uiBtnStatusBarClose.setEnabled(True)

        else:
            self.file_count = 0
            self._normalise_multiple_scripts()




##############################################################################################################################
#                                    ONE SCRIPT (FILE):
##############################################################################################################################


  
    def _normalise_one_script(self):

        try:
            with open(self.path, 'r') as file:
                text = file.read()
        except Exception as e:
            dialog_message(self, f"Error while opening {self.path}: {e}")
            return

        text, results = normalize_script_text(text)
            
        try:
            with open(self.path, 'w') as file:
                file.write(text)
        except Exception as e:
            dialog_message(self, f"Error while saving {self.path}: {e}")
            return  

        return results






    def _create_ui_output_from_one_script(self, results: list):
        uiLabHeadingUpdates = QLabel(f"Following variables have been updated ({len(results)}):")
        uiTextEditSummaryUpdates = QPlainTextEdit()
        

        if results:
            for r in results:
                uiTextEditSummaryUpdates.appendHtml(f'<span style="color: #D55">{r[0]}</span> has been replaced by <span style="color: #5D5">{r[1]}</span>\n')
        else:
            uiTextEditSummaryUpdates.appendHtml(f'<span style="color: #5D5">All variables are defined according to VDA recommendations.</span>\n')


        self.uiMainLayout_1.addWidget(uiLabHeadingUpdates)
        self.uiMainLayout_1.addWidget(uiTextEditSummaryUpdates)        







##############################################################################################################################
#                                    MULTIPLE SCRIPTS (FOLDER)
##############################################################################################################################


    def _normalise_multiple_scripts(self):
        self.uiLabHeadingUpdates = QLabel(f"Following files have been updated:")
        self.uiTreeWidgetSummaryUpdates = QTreeWidget()
        self.uiTreeWidgetSummaryUpdates.setHeaderHidden(True) 
        self.uiMainLayout_4.addWidget(self.uiLabHeadingUpdates)
        self.uiMainLayout_4.addWidget(self.uiTreeWidgetSummaryUpdates)   

        self.uiLabProgressStatus = QLabel()
        self.uiMainLayout_1.addWidget(self.uiLabProgressStatus) 

        worker = ScriptNormalizationWorker(self.path)
        worker.signals.current_file.connect(self.update_progress_status)
        worker.signals.replacements.connect(
            self.create_ui_output_from_multiple_scripts
        )
        worker.signals.finished.connect(self.finished)
        self.threadpool.start(worker)





    @pyqtSlot(str)
    def update_progress_status(self, path: str):
        self.uiLabProgressStatus.setText(f"Checking files:   {reduce_path_string(path)}")




    @pyqtSlot()
    def finished(self):
        self.uiBtnStatusBarClose.setEnabled(True)
        self.uiLabProgressStatus.setText("Checking files:   Finished")
        if self.file_count == 0:
            self.uiLabHeadingUpdates.setText(f"Following files have been updated: 0")
            # self.uiTreeWidgetSummaryUpdates.setVisible(False)




    @pyqtSlot(str, list)
    def create_ui_output_from_multiple_scripts(self, path: str, replacements: list):

        

        if replacements:
            self.file_count += 1
            self.uiLabHeadingUpdates.setText(f"Following files have been updated: {self.file_count}")

            item = QTreeWidgetItem(self.uiTreeWidgetSummaryUpdates)
            item.setText(0, f"{reduce_path_string(path)}:  ({len(replacements)}x)")
            for r in replacements:
                temp_item = QTreeWidgetItem(item)
                temp_item.setText(0, f"{r[0]}   -->   {r[1]}")

