from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon


def create_action(icon_path, text, slot=None, shortcut=None, toolbar=None):
    action = QAction(QIcon(icon_path), text)
    if shortcut:
        action.setShortcut(shortcut)
        action.setToolTip(f"{text} ({shortcut})")
    if slot:
        action.triggered.connect(slot)
    if toolbar:
        toolbar.addAction(action)

    return action