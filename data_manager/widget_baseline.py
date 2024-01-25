from PyQt5.QtWidgets import QTextEdit, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QListWidgetItem
from PyQt5.QtGui import QIcon


class WidgetBaseline(QWidget):
    def __init__(self, view_only=True):
        super().__init__()

        self.setStyleSheet("""
        QPushButton{background-color: rgb(58, 89, 245);
        color: rgb(200, 200, 200);
        font-size: 14px;
        padding: 5px;
        }

        QPushButton:hover{
        background-color: rgb(95, 180, 255);
        }
        """)

        self.view_only = view_only # if True, then the user can't switch the baseline

        uiMainLayout = QHBoxLayout()
        uiVLayout = QVBoxLayout()

        self.uiTextEditBaseLineDetails = QTextEdit()
        self.uiListWidgetBaselines = QListWidget()
        self.uiListWidgetBaselines.setMaximumWidth(200)
        self.uiBtnSwitchBaseLine = QPushButton("Switch")
        self.uiBtnSwitchBaseLine.setVisible(not self.view_only)


        uiVLayout.addWidget(self.uiListWidgetBaselines)
        uiVLayout.addWidget(self.uiBtnSwitchBaseLine)

        
        uiMainLayout.addLayout(uiVLayout)
        uiMainLayout.addWidget(self.uiTextEditBaseLineDetails)
        

        self.setLayout(uiMainLayout)

        self.uiListWidgetBaselines.currentItemChanged.connect(self._update_text)
        self.uiBtnSwitchBaseLine.clicked.connect(self._switch_baseline)

        self.switched_baseline = None


    # INTERFACE FROM DATA MANAGER
    def update(self, module):
        self.module = module
        self._update_list()
        self._update_text()
        self._update_icon()

    
    def _update_list(self):
        baselines = self.module.baseline
        self.uiListWidgetBaselines.clear()
        for b in reversed(baselines.keys()):
            baseline_item = QListWidgetItem(b, self.uiListWidgetBaselines)

        self.uiListWidgetBaselines.setCurrentRow(0)

    
    def _update_text(self):
        self.uiTextEditBaseLineDetails.clear()
        item = self.uiListWidgetBaselines.currentItem()
        if item:
            baselines = self.module.baseline
            selected_baseline_key = item.text()
            baseline = baselines.get(selected_baseline_key)
            value_names = ["User", "Date", "Note"]

            try:
                for i in range(len(baseline)):            
                    self.uiTextEditBaseLineDetails.insertHtml(f'<span style="color: rgb(150, 150, 150);">{value_names[i].capitalize()}:</span>  <span> {baseline[i]}</span><br>')
                    self.uiBtnSwitchBaseLine.setEnabled(True)
            except IndexError:    
                # FOR OLDER VERSION OF R2: #TODO: DELETE THIS AFTER SOME TIME
                self.uiTextEditBaseLineDetails.clear()        
                self.uiTextEditBaseLineDetails.insertHtml(baseline)
                self.uiBtnSwitchBaseLine.setEnabled(False)
                

    
    def _update_icon(self):
        for row in range(self.uiListWidgetBaselines.count()):
            temp_list_widget_item = self.uiListWidgetBaselines.item(row)
            if self.module.current_baseline == temp_list_widget_item.text():
                temp_list_widget_item.setIcon(QIcon(u"ui/icons/check.png"))
                self._update_selection(temp_list_widget_item)
            else:    
                temp_list_widget_item.setIcon(QIcon())

        if not self.module.current_baseline:
            first_item = self.uiListWidgetBaselines.item(0)
            if first_item:
                first_item.setIcon(QIcon(u"ui/icons/check.png"))
                self._update_selection(first_item)


    def _update_selection(self, item):
        self.uiListWidgetBaselines.setCurrentItem(item)


    def _switch_baseline(self):
        item = self.uiListWidgetBaselines.currentItem()
        if item:
            self._remove_all_icons()
            item.setIcon(QIcon(u"ui/icons/check.png"))
            self.switched_baseline = item.text()


    def _remove_all_icons(self):
        for row in range(self.uiListWidgetBaselines.count()):
            temp_list_widget_item = self.uiListWidgetBaselines.item(row)
            temp_list_widget_item.setIcon(QIcon())



        
            
