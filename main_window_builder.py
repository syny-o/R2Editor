from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QFrame, QLabel, QSplitter, QVBoxLayout

from components.widgets.widgets_pointing_hand import TreeWidgetPointingHand
from dashboard.dashboard import Dashboard
from data_manager.data_manager import DataManager
from file_browser.tree_file_browser import FileSystemView
from text_editor.outline.controller import OutlineController
from text_editor.tab_manager import EditorTabManager
from text_editor.tabs import Tabs


class MainWindowBuilder:
    def __init__(self, main_window, project_manager):
        self.main_window = main_window
        self.project_manager = project_manager

    def build(self):
        self._build_file_and_outline_panel()
        self._build_application_pages()
        self._build_editor_tabs()
        self._build_page_stack()

    def _build_file_and_outline_panel(self):
        window = self.main_window
        panel_splitter = QSplitter(Qt.Vertical)
        window.uiLayoutFileManager.addWidget(panel_splitter)

        window.tree_file_browser = FileSystemView(
            window,
            self.project_manager,
        )
        panel_splitter.addWidget(window.tree_file_browser)

        outline_layout = QVBoxLayout()
        outline_layout.setContentsMargins(0, 0, 0, 0)
        outline_layout.addWidget(QLabel('Outline'), alignment=Qt.AlignCenter)

        window.uiTreeOutline = TreeWidgetPointingHand()
        window.uiTreeOutline.setHeaderHidden(True)
        outline_layout.addWidget(window.uiTreeOutline)

        window.outline_controller = OutlineController(
            window,
            window.uiTreeOutline,
        )
        window.uiTreeOutline.itemClicked.connect(
            window.outline_controller.click_item
        )
        window.timer_4_updating_outline = QTimer()
        window.timer_4_updating_outline.timeout.connect(
            window.outline_controller.update
        )
        window.timer_4_updating_outline.start(500)

        outline_frame = QFrame()
        outline_frame.setObjectName('objNameFrameOutline')
        outline_frame.setLayout(outline_layout)
        panel_splitter.addWidget(outline_frame)

    def _build_application_pages(self):
        window = self.main_window
        window.data_manager = DataManager(window, self.project_manager)
        window.script_requirement_reference_changed.connect(
            window.data_manager.script_requirement_reference_changed
        )
        window.dashboard = Dashboard(window, self.project_manager)
        self.project_manager.set_listeners(
            window,
            window.dashboard,
            window.data_manager,
            window.tree_file_browser,
        )

    def _build_editor_tabs(self):
        window = self.main_window
        window.left_tabs = Tabs(window, True, 'LEFT_TABS')
        window.left_tabs.currentChanged.connect(
            window.editor_controller.update_find_replace
        )
        window.right_tabs = Tabs(window, False, 'RIGHT_TABS')
        window.right_tabs.currentChanged.connect(
            window.editor_controller.update_find_replace
        )

        window.tab_manager = EditorTabManager(
            window,
            window.left_tabs,
            window.right_tabs,
        )
        window.tab_manager.connect_signals()

        window.tabs_splitter = QSplitter()
        window.tabs_splitter.addWidget(window.left_tabs)
        window.tabs_splitter.addWidget(window.right_tabs)
        window.tabs_splitter.setStretchFactor(2, 1)

    def _build_page_stack(self):
        window = self.main_window
        for page in (
            window.tabs_splitter,
            window.data_manager,
            window.app_settings,
            window.dashboard,
        ):
            window.stackedWidget.addWidget(page)
        window.stackedWidget.setCurrentWidget(window.dashboard)
        window.window_controller.connect_navigation()
