from PyQt5.QtCore import Qt

from config import constants
from data_manager.nodes.requirement_node import RequirementNode
from data_manager.view import filter


class ViewFilterController:
    def __init__(self, view):
        self.view = view

    def trigger(self, reset_filter):
        view = self.view
        text = view.uiLineEditTextFilter.text()
        coverage = view.uiComboCoverageFilter.currentText()

        current_index = view.uiDataTreeView.currentIndex()
        if not current_index.isValid():
            return

        item = view.MODEL.itemFromIndex(current_index)
        if isinstance(item, RequirementNode):
            return

        item.view_filter = constants.ViewCoverageFilter(coverage)
        item.setData(text, Qt.UserRole)
        filter.filter(
            view.uiDataTreeView,
            item,
            text,
            coverage,
            reset_filter=reset_filter,
        )

    def stop(self):
        view = self.view
        coverage = view.uiComboCoverageFilter.currentText()
        current_index = view.uiDataTreeView.currentIndex()
        if not current_index.isValid():
            return

        view.uiLineEditTextFilter.clear()
        item = view.MODEL.itemFromIndex(current_index)
        filter.stop_filtering(
            view.uiDataTreeView,
            item,
            coverage,
        )
