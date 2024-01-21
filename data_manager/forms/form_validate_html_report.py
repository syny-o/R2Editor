from PyQt5.QtWidgets import QWidget, QLabel, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QColor

from dialogs.dialog_message import dialog_message
from ui.form_general_ui import Ui_Form


class FormValidatedHTMLReport(QWidget, Ui_Form):

    def __init__(self, data_manager: object, not_covered_requirements: list):
        super().__init__()
        self.setupUi(self)
        # self.setMinimumSize(600, 600)
        self.setWindowIcon(QIcon('R2Editor.ico'))
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setWindowModality(Qt.ApplicationModal)
        self.uiFrameTitleBar.setMaximumHeight(0)
        self.setWindowOpacity(0.95)        
        self.setWindowTitle("HTML Report Validation")
        self.uiLabelTitle.setText("HTML Report Validation")
        self.uiBtnStatusBarClose.clicked.connect(self.close)
        self.uiBtnTitleBarClose.clicked.connect(self.close)
        self.uiBtnOK.setVisible(False)
        self.uiMainLayout_1.setContentsMargins(20, 20, 20, 20)
        self.uiMainLayout_1.setSpacing(20)
        
        uiListWidgetIdentifiers = QListWidget()
        uiListWidgetIdentifiers.itemDoubleClicked.connect(lambda item: data_manager.doubleclicked_on_requirement_in_HTML_report_form(item.text()))
        lw_items = [QListWidgetItem(QIcon(u"ui/icons/cross.png"), item, uiListWidgetIdentifiers) for item in not_covered_requirements]



        self.ui_label_number_covered_requirements = QLabel()
        self.ui_label_number_total_requirements = QLabel()
        self.ui_label_number_not_covered_requirements = QLabel(f"Followng identifiers are missing in report ({len(not_covered_requirements)}):")
        self.uiMainLayout_1.addWidget(self.ui_label_number_not_covered_requirements)
        self.uiMainLayout_1.addWidget(uiListWidgetIdentifiers)
        # self.uiMainLayout_3.addWidget(self.ui_label_number_total_requirements)
        # self.uiMainLayout_3.addWidget(self.ui_label_number_covered_requirements)
        

        self.show()  


        








