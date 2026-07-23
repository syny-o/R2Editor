from importlib import reload

from PyQt5.QtWidgets import QApplication

import config.app_styles


class SettingsController:
    def __init__(self, main_window):
        self.main_window = main_window

    def apply(self):
        settings = self.main_window.app_settings
        self.update_theme(settings.theme)
        self.update_autosave_interval(settings.autosave)

    def update_autosave_interval(self, autosave_interval):
        timer = self.main_window.timer_project_autosave
        timer.stop()
        if autosave_interval != 'Off':
            interval = int(autosave_interval) * 60 * 1000
            timer.start(interval)

    def update_theme(self, theme):
        reload(config.app_styles)
        styles = config.app_styles.switch_theme(theme.upper())
        QApplication.instance().setStyleSheet(styles)
