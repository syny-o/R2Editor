import os, re, stat
from pathlib import Path

from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QCheckBox, QTextEdit, QPlainTextEdit, QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot, QSettings, QRunnable, QThreadPool

from ui.form_general_ui import Ui_Form
from components.reduce_path_string import reduce_path_string

from file_browser.pbc_patterns_scripts import patterns
from dialogs.dialog_message import dialog_message





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

        # THREAD CONFIGURATION
        self.threadpool = QThreadPool()
        self.threadpool.setMaxThreadCount(1)



        self.path = path

        if Path(self.path).is_file():
            results = self._normalise_one_script()
            self._create_ui_output_from_one_script(results)

        else:
            self.file_count = 0
            self._normalise_multiple_scripts()




##############################################################################################################################
#                                    ONE SCRIPT (FILE):
##############################################################################################################################


  
    def _normalise_one_script(self):

        results = []

        try:
            with open(self.path, 'r') as file:
                text = file.read()
        except Exception as e:
            dialog_message(self, f"Error while opening {self.path}: {e}")
            return

        for key, value in patterns.items():
            # find all matches for each variable
            pattern = key
            iterations = pattern.finditer(text)

            for i in iterations:

                string_to_replace = i.group()
                # print(string_to_replace)

                if string_to_replace != value:
                    text = text.replace(string_to_replace, value)

                    results.append( (string_to_replace, value) )
            
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
        self.uiMainLayout_5.addWidget(self.uiLabHeadingUpdates)
        self.uiMainLayout_5.addWidget(self.uiTreeWidgetSummaryUpdates)   

        self.uiLabProgressStatus = QLabel()
        self.uiMainLayout_1.addWidget(self.uiLabProgressStatus) 

        worker = Worker(self)
        self.threadpool.start(worker)





    @pyqtSlot(str)
    def update_progress_status(self, path: str):
        self.uiLabProgressStatus.setText(f"Checking files:   {reduce_path_string(path)}")




    @pyqtSlot()
    def finished(self):
        self.uiBtnStatusBarClose.setEnabled(True)
        self.uiLabProgressStatus.setText("Checking files:   Finished")




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

            







class Worker(QRunnable):

    def __init__(self, form):
        super().__init__()
        self.form = form
        self.signals = WorkerSignals()
        self.signals.current_file.connect(form.update_progress_status)
        self.signals.replacements.connect(form.create_ui_output_from_multiple_scripts)
        self.signals.finished.connect(form.finished) 



    @pyqtSlot()
    def run(self):

        for root, dirs, files in os.walk(self.form.path):
            for filename in files:
                if filename.endswith((".par", ".txt")):

                    full_path = (root + '\\' + filename)

                    self.signals.current_file.emit(full_path)
                    
                    # Check if the file ReadOnly and if so, unlock it:
                    is_read_only = not(os.access(full_path, os.W_OK))
                    if is_read_only:
                        os.chmod(full_path, stat.S_IWRITE)

                    with open(full_path, 'r') as f:
                        text = f.read()

                    
                    l = []

                    for key, value in patterns.items():
                        # find all matches for each variable
                        pattern = key
                        iterations = pattern.finditer(text)

                        for i in iterations:

                            string_to_replace = i.group()
                            # print(string_to_replace)

                            if string_to_replace != value:
                                text = text.replace(string_to_replace, value)

                                l.append( (string_to_replace, value) )

                        
                        
                    if l:
                        # results[full_path] = l
                        self.signals.replacements.emit(full_path, l) 



                    # with open(full_path, 'w') as f:
                    #     f.write(text)

                    # lock the file to be ReadOnly back again
                    if is_read_only:
                        os.chmod(full_path, stat.S_IREAD)



                    
                    

        self.signals.finished.emit()
        
        # text = re.sub(r"""_?PbcOut(Debug)?\.?_?FaultStatus.?[_\[]?(?P<number>\d\d)\]?_?""", r"""PbcOutFaultStatus_\g<number>""", text)

        # text = re.sub(r"""_?PbcOut(Debug)?\.?_?FaultStatus.?[_\[]?(?P<number>\d)(?!\d)\]?_?""", r"""PbcOutFaultStatus_0\g<number>""", text)






class WorkerSignals(QObject):
    replacements = pyqtSignal(str, list)
    current_file = pyqtSignal(str)  
    finished = pyqtSignal()      


