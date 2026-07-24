from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, QTimer

from config.icon_manager import IconManager


class WindowController:
    def __init__(self, main_window):
        self.main_window = main_window
        self.menu_animation = None

    def configure_icons(self, icons):
        window = self.main_window
        icon_bindings = (
            (window.ui_btn_home, icons.ICON_DASHBOARD),
            (window.ui_btn_data_manager, icons.ICON_DATA_MANAGER),
            (window.ui_btn_text_editor, icons.ICON_CODE_EDITOR),
            (window.btn_app_settings, icons.ICON_SETTINGS),
            (window.btn_app_exit, icons.ICON_APP_EXIT),
            (window.btn_project_open, icons.ICON_PROJECT_OPEN),
            (window.btn_project_new, icons.ICON_PROJECT_NEW),
            (window.btn_project_save, icons.ICON_PROJECT_SAVE),
            (window.btn_project_save_as, icons.ICON_PROJECT_SAVE_AS),
            (window.btn_toggle_menu, icons.ICON_MENU),
            (window.btn_script_new, icons.ICON_NEW_SCRIPT),
            (window.btn_script_open, icons.ICON_OPEN_SCRIPT),
            (window.btn_script_save, icons.ICON_SAVE_SCRIPT),
            (window.btn_script_save_as, icons.ICON_SAVE_SCRIPT_AS),
            (window.btn_insert_chapter, icons.ICON_INSERT_CHAPTER),
            (window.btn_insert_testcase, icons.ICON_INSERT_TESTCASE),
            (window.btn_insert_command, icons.ICON_INSERT_COMMAND),
            (
                window.btn_comment_uncomment,
                icons.ICON_COMMENT_UNCOMMENT,
            ),
            (window.btn_format_code, icons.ICON_FORMAT_CODE),
            (window.btn_zoom_in, icons.ICON_ZOOM_IN),
            (window.btn_zoom_out, icons.ICON_ZOOM_OUT),
            (window.btn_zoom_default, icons.ICON_ZOOM_RESET),
        )
        for button, icon in icon_bindings:
            button.setIcon(icon)

    def connect_window_actions(self):
        window = self.main_window
        window.btn_app_exit.clicked.connect(window.close)
        window.btn_close.clicked.connect(window.close)
        window.btn_toggle_menu.clicked.connect(
            lambda: self.toggle_menu(window.uiFrameLeftMenu, 70, 210)
        )

    def connect_navigation(self):
        window = self.main_window
        navigation = (
            (window.ui_btn_text_editor, window.tabs_splitter),
            (window.ui_btn_data_manager, window.data_manager),
            (window.ui_btn_home, window.dashboard),
            (window.btn_app_settings, window.app_settings),
        )
        for button, page in navigation:
            button.clicked.connect(
                lambda checked=False, page=page, button=button:
                window.manage_right_menu(page, button)
            )

    def show_page(self, widget, button):
        window = self.main_window
        for navigation_button in (
            window.ui_btn_home,
            window.ui_btn_text_editor,
            window.ui_btn_data_manager,
            window.btn_app_settings,
        ):
            navigation_button.setChecked(False)

        window.stackedWidget.setCurrentWidget(widget)
        button.setChecked(True)
        editor_is_visible = button is window.ui_btn_text_editor
        window.uiFrameFileManager.setVisible(editor_is_visible)
        window.frame_2.setVisible(editor_is_visible)
        if editor_is_visible and window.actual_text_edit:
            window.actual_text_edit.setFocus()

    def toggle_menu(self, toggled_frame, min_width, max_width):
        window = self.main_window
        width = toggled_frame.width()
        extended_width = max_width if width == min_width else min_width
        self.menu_animation = QPropertyAnimation(
            toggled_frame,
            b'minimumWidth',
        )
        self.menu_animation.setDuration(300)
        self.menu_animation.setStartValue(width)
        self.menu_animation.setEndValue(extended_width)
        self.menu_animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.menu_animation.start()

        icon = (
            IconManager().ICON_MENU_CLOSE
            if window.btn_toggle_menu.isChecked()
            else IconManager().ICON_MENU
        )
        window.btn_toggle_menu.setIcon(icon)

    def update_project_title(self, project_params):
        path = project_params.get('json_project_path')
        is_saved = project_params.get('is_project_saved')
        modified_status = '' if is_saved else '[*Modified]'
        project_path = str(path) if path else 'No Project Loaded'

        label = self.main_window.label_opened_project
        label.setText(f'{project_path} {modified_status}')
        color = 'rgb(200, 200, 200)' if is_saved else 'rgb(250, 50, 50)'
        label.setStyleSheet(f'color: {color};')

    def update_editor_state(self):
        window = self.main_window
        if window.left_tabs.count() == 0 and window.right_tabs.count() == 0:
            window.actual_text_edit = None

        self._update_lock_button()
        self._update_tabs_color()
        self._update_window_title()
        window.outline_controller.update_selected_item()

    def show_notification(self, notification_text):
        window = self.main_window
        label = window.uiLabelProgressStatus
        label.setText(notification_text)
        label.setStyleSheet('color: rgb(50, 250, 50);')
        if window.actual_text_edit:
            window.actual_text_edit.setFocus()

        QTimer.singleShot(4000, lambda: label.setText('Ready'))
        QTimer.singleShot(
            4000,
            lambda: label.setStyleSheet('color: rgb(200, 200, 200);'),
        )
        if window.actual_text_edit:
            QTimer.singleShot(4100, window.actual_text_edit.setFocus)

    def _update_lock_button(self):
        window = self.main_window
        if window.actual_text_edit is None:
            window.btn_lock_unlock.setVisible(False)
            return

        window.btn_lock_unlock.setVisible(True)
        icon = (
            IconManager().ICON_FILE_LOCKED
            if window.actual_text_edit.isReadOnly()
            else IconManager().ICON_FILE_UNLOCKED
        )
        window.btn_lock_unlock.setIcon(icon)

    def _update_tabs_color(self):
        window = self.main_window
        if not window.actual_tabs:
            return

        inactive_style = (
            'QTabBar::tab {border-bottom: 3px solid #31363b}'
        )
        window.left_tabs.setStyleSheet(inactive_style)
        window.right_tabs.setStyleSheet(inactive_style)
        window.actual_tabs.setStyleSheet(
            'QTabBar::tab:selected {'
            'border-bottom: 3px solid rgb(0, 128, 255)'
            '}'
        )

    def _update_window_title(self):
        text_edit = self.main_window.actual_text_edit
        title = f'Editor - {text_edit.file_path}' if text_edit else 'Editor'
        self.main_window.setWindowTitle(title)
