from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QHBoxLayout, QLabel, QShortcut, QVBoxLayout

from components.my_list_widget import MyListWidget
from components.widgets.widget_baseline import WidgetBaseline
from components.widgets.widget_req_filter_text_edit import RequirementFilterTextEdit
from data_manager.nodes.requirement_module import RequirementModule


class RequirementModuleLayoutGenerator:
    def __init__(self, node: RequirementModule) -> None:
        self.uiMainLayout = QVBoxLayout()
        self.uiMainLayout.setContentsMargins(10, 10, 10, 10)
        self.uiMainLayout.setSpacing(10)
        self.NODE = node

    def _create_layout(self):
        uiLayoutModuleColumns = QHBoxLayout()
        uiLayoutModuleColumns.setContentsMargins(0, 20, 0, 0)
        uiLayoutModuleColumns.addWidget(QLabel("Columns:"))

        self.uiListWidgetModuleAttributes = MyListWidget(context_menu=False)
        self.uiListWidgetModuleAttributes.setAcceptDrops(False)
        uiLayoutModuleColumns.addWidget(self.uiListWidgetModuleAttributes)

        uiLayoutBaseline = QHBoxLayout()
        uiLayoutBaseline.addWidget(QLabel("Baseline:"))
        self.uiWidgetBaselines = WidgetBaseline(view_only=False)
        self.uiWidgetBaselines.setMaximumHeight(160)
        self.uiWidgetBaselines.update(self.NODE)
        uiLayoutBaseline.addWidget(self.uiWidgetBaselines)
        self.uiMainLayout.addLayout(uiLayoutBaseline)

        self.uiListWidgetModuleColumns = MyListWidget()
        self.uiListWidgetModuleColumns.setDefaultDropAction(Qt.MoveAction)
        QShortcut("Del", self.uiListWidgetModuleColumns).activated.connect(
            self.uiListWidgetModuleColumns.remove_item
        )
        uiLayoutModuleColumns.addWidget(self.uiListWidgetModuleColumns)

        self.uiMainLayout.addLayout(uiLayoutModuleColumns)

        self.uiListWidgetModuleColumns.insertItems(0, self.NODE.columns_names)
        self.uiListWidgetModuleAttributes.insertItems(0, self.NODE.attributes)

        self.uiLabelWarning = QLabel()

        uiLayoutCustomIndetifier = QHBoxLayout()
        uiLayoutCustomIndetifier.setContentsMargins(0, 10, 0, 10)
        self.uiComboColumnsAsIdentifier = QComboBox()
        self.uiComboColumnsAsIdentifier.setEditable(False)
        self.uiComboColumnsAsIdentifier.insertItems(
            0, ["<< Default Doors Identifier >>"]
        )
        self.uiComboColumnsAsIdentifier.insertItems(1, self.NODE.columns_names)
        if self.NODE.column_number_as_identifier is None:
            self.uiComboColumnsAsIdentifier.setCurrentIndex(0)
        else:
            self.uiComboColumnsAsIdentifier.setCurrentIndex(
                self.NODE.column_number_as_identifier + 1
            )
        uiLayoutCustomIndetifier.addWidget(QLabel("Identifier:"))
        uiLayoutCustomIndetifier.addWidget(self.uiComboColumnsAsIdentifier)

        self.uiMainLayout.addLayout(uiLayoutCustomIndetifier)

        if self.NODE.coverage_filter:
            self.uiListWidgetModuleColumns.setEnabled(False)
            self.uiWidgetBaselines.setEnabled(False)
            self.uiLabelWarning.setText(
                "Remove coverage filter to edit columns/baseline."
            )
            self.uiLabelWarning.setStyleSheet("color: red;")
            self.uiLabelWarning.setAlignment(Qt.AlignCenter)
            self.uiMainLayout.addWidget(self.uiLabelWarning)

        uiLayoutCoverageFilter = QHBoxLayout()
        uiLayoutCoverageFilter.addWidget(QLabel("Cv. Filter:"))
        self.uiTexEditCoverageFilter = RequirementFilterTextEdit(
            self.NODE.columns_names
        )
        if not self.NODE.columns_names:
            self.uiTexEditCoverageFilter.setEnabled(False)
        self.uiTexEditCoverageFilter.setMaximumHeight(100)
        uiLayoutCoverageFilter.addWidget(self.uiTexEditCoverageFilter)
        if coverage_filter := self.NODE.coverage_filter:
            self.uiTexEditCoverageFilter.setPlainText(str(coverage_filter))
        self.uiLabelNumberOfFilteredRequirements = QLabel()
        self.uiLabelNumberOfFilteredRequirements.setAlignment(Qt.AlignCenter)
        self.uiMainLayout.addLayout(uiLayoutCoverageFilter)
        self.uiMainLayout.addWidget(self.uiLabelNumberOfFilteredRequirements)

    def provide_layout(self) -> QVBoxLayout:
        self._create_layout()
        return self.uiMainLayout

    def update_data(self):
        change = False
        self._save_identifier_changes()
        if self._evaluate_baseline_changes():
            self._save_baseline_changes()
            change = True
        if self._evaluate_columns_changes():
            self._save_columns_changes()
            change = True
        if self._evaluate_filter_changes():
            change = self._save_filter_changes()
        return change

    def _evaluate_baseline_changes(self):
        return self.uiWidgetBaselines.switched_baseline != self.NODE.current_baseline

    def _evaluate_columns_changes(self):
        return self.uiListWidgetModuleColumns.get_all_items() != self.NODE.columns_names

    def _evaluate_filter_changes(self):
        filter_text = self.uiTexEditCoverageFilter.toPlainText().strip()
        if not self.NODE.coverage_filter:
            return bool(filter_text)
        return filter_text != self.NODE.coverage_filter

    def _save_baseline_changes(self):
        self.NODE.current_baseline = self.uiWidgetBaselines.switched_baseline

    def _save_columns_changes(self):
        self.NODE.columns_names = self.uiListWidgetModuleColumns.get_all_items()

    def _save_identifier_changes(self):
        if self.uiComboColumnsAsIdentifier.currentIndex() == 0:
            self.NODE.column_number_as_identifier = None
        else:
            self.NODE.column_number_as_identifier = (
                self.uiComboColumnsAsIdentifier.currentIndex() - 1
            )

    def _save_filter_changes(self):
        if self.NODE.columns_names != self.NODE.columns_names_backup:
            self.uiLabelNumberOfFilteredRequirements.setText(
                "Columns changed - Download data from Doors first."
            )
            self.uiLabelNumberOfFilteredRequirements.setStyleSheet(
                "color: red; font-size: 16px; margin-top: 10px;"
            )
            return False

        filter_string = self.uiTexEditCoverageFilter.toPlainText().strip()
        filter_string = filter_string.replace("\n", " ")
        if filter_string:
            try:
                self._apply_coverage_filter(filter_string)
            except Exception as ex:
                self.uiLabelNumberOfFilteredRequirements.setText(
                    "Wrong Filter: " + str(ex)
                )
                self.uiLabelNumberOfFilteredRequirements.setStyleSheet(
                    "color: red; font-size: 16px; margin-top: 10px;"
                )
                raise
            return True

        self._remove_coverage_filter()
        return True

    def _apply_coverage_filter(self, filter_string):
        self.NODE.apply_coverage_filter(filter_string)
        self.uiLabelNumberOfFilteredRequirements.setText(
            f"Filtered: {self.NODE.number_of_calculated_requirements}"
        )
        self.uiLabelNumberOfFilteredRequirements.setStyleSheet(
            "color: green; font-size: 16px; margin-top: 10px;"
        )
        self.uiListWidgetModuleColumns.setEnabled(False)
        self.uiWidgetBaselines.setEnabled(False)

    def _remove_coverage_filter(self):
        self.NODE.remove_coverage_filter()
        self.uiLabelNumberOfFilteredRequirements.setText("")
        self.uiListWidgetModuleColumns.setEnabled(True)
        self.uiWidgetBaselines.setEnabled(True)
        self.uiLabelWarning.hide()
