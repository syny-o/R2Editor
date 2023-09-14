from PyQt5.QtWidgets import QMessageBox
def dialog_message(parent, message, title='Information'):
    dlg = QMessageBox(parent)
    dlg.setText(message)
    dlg.setIcon(QMessageBox.Information)
    dlg.setWindowTitle(title)
    dlg.show()