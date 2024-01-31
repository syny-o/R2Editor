import os, re, stat

from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QCheckBox, QTextEdit, QPlainTextEdit
from PyQt5.QtCore import Qt, pyqtSignal

from dialogs.dialog_message import dialog_message
from ui.form_general_ui import Ui_Form
from components.reduce_path_string import reduce_path_string





class A2lNormReport(QWidget, Ui_Form):
    """
    This "window" will appear after successfull A2L normalisation is finished
    """


    def __init__(self, data_4_report: dict, missing_signals: list, duplicated_signals: list):
        super().__init__()
        self.setupUi(self)
        self.uiMainLayout_1.setContentsMargins(0,0,0,0)
        self.uiMainLayout_2.setContentsMargins(0,0,0,0)
        self.uiMainLayout_3.setContentsMargins(0,0,0,0)
        self.uiMainLayout_4.setContentsMargins(0,0,0,0)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(1024, 768)
        self.setWindowOpacity(0.95)  
        self.uiBtnOK.setVisible(False)         
        self.uiLabelTitle.setText(f"A2L Normalisation Finished")
        self.uiBtnTitleBarClose.clicked.connect(self.close)
        self.uiBtnStatusBarClose.clicked.connect(self.close)
        self.uiBtnStatusBarClose.setText("Close")
        # self.uiBtnOK.clicked.connect(self.close)        
        uiLabHeadingUpdates = QLabel(f"Following variables have been updated ({len(data_4_report)}):")
        uiTextEditSummaryUpdates = QPlainTextEdit()

        if data_4_report:
            for k, v in data_4_report.items():
                uiTextEditSummaryUpdates.appendHtml(f'<span style="color: #D55">{k}</span> has been replaced by <span style="color: #5D5">{v}</span>\n')
        else:
            uiTextEditSummaryUpdates.appendHtml(f'<span style="color: #5D5">All variables are defined according to VDA recommendations.</span>\n')


        self.uiMainLayout_1.addWidget(uiLabHeadingUpdates)
        self.uiMainLayout_1.addWidget(uiTextEditSummaryUpdates)



        
        uiTextEditSummaryMissingSignals = QPlainTextEdit()
        uiTextEditSummaryMissingSignals.setMaximumHeight(80)
        missing_signals_count = 0
        if missing_signals:
            for s in missing_signals:                
                uiTextEditSummaryMissingSignals.appendHtml(f'<span style="color: #D55">{s}</span>\n')
        else:
            uiTextEditSummaryMissingSignals.appendHtml(f'<span style="color: #5D5">All mandatory variables are present.</span>\n')

        uiLabHeadingMissingSignals = QLabel(f"Following variables are missing ({missing_signals_count}):")


        self.uiMainLayout_1.addWidget(uiLabHeadingMissingSignals)
        self.uiMainLayout_1.addWidget(uiTextEditSummaryMissingSignals)    



        uiTextEditSummaryDuplicatedSignals = QPlainTextEdit()
        uiTextEditSummaryDuplicatedSignals.setMaximumHeight(80)
        if duplicated_signals:
            for s in duplicated_signals:
                uiTextEditSummaryDuplicatedSignals.appendHtml(f'<span style="color: #D55">{s}</span>\n')
        else:
            uiTextEditSummaryDuplicatedSignals.appendHtml(f'<span style="color: #5D5">All variables are defined just once.</span>\n')


        uiLabHeadingDuplicatedSignals = QLabel(f"Following variables are defined more than once ({len(duplicated_signals)}):")

            

        self.uiMainLayout_1.addWidget(uiLabHeadingDuplicatedSignals)
        self.uiMainLayout_1.addWidget(uiTextEditSummaryDuplicatedSignals)         
     







