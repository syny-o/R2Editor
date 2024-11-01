from PyQt5.QtGui import QStandardItem, QIcon, QTextCursor, QTextCharFormat, QColor, QCursor
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QLayout, QFrame, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QApplication
from PyQt5.QtCore import Qt


def layout_generate_one_row(label_text: str, main_layout: QVBoxLayout, extend_label_width: bool = True) -> QLineEdit:
    
    MINIMUM_LABEL_WIDTH = 70

    uiOneRowLayout = QHBoxLayout()
    line_edit = QLineEdit()
    label = QLabel(label_text)
    if extend_label_width:
        label.setMinimumWidth(MINIMUM_LABEL_WIDTH)
    uiOneRowLayout.addWidget(label)
    uiOneRowLayout.addWidget(line_edit)             
    main_layout.addLayout(uiOneRowLayout)
    main_layout.setAlignment(Qt.AlignCenter)
    line_edit.setReadOnly(True)  # disable editing data in right panel --> only for displaying data:
    return line_edit





def validate_line_edits(*line_edits: QLineEdit, 
                        invalid_chars = ('\\', '?', '!', '<', '>', '&', '#', '@', '^', '*', '$')) -> bool:

    success = True
  
    for line_edit in line_edits:
        if any(ch in line_edit.text() for ch in invalid_chars) or line_edit.text().strip() == "":
            line_edit.setStyleSheet("border-color: red")
            success = False
        else:
            line_edit.setStyleSheet("border-color: rgb(60, 60, 60)")
    return success    