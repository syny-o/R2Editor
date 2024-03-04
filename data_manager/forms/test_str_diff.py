from PyQt5.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtGui import QTextCharFormat, QColor, QTextCursor
import difflib

class DiffTextEdit(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 800)

        self.text_edit = QTextEdit(self)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        self.setLayout(layout)


        strings = []
        self.string1 = "04 Approved"
        self.string2 = "Rejected"
        strings.append((self.string1, self.string2), )

        self.string1 = 'Hello World Again'
        self.string2 = 'Hello Python World!'
        strings.append((self.string1, self.string2), )

        self.string1 = 'Play football\nPlay cricket\nPlay basketball'
        self.string2 = 'Buy football\nPlay cricket\nPlay basketball and tennis'
        strings.append((self.string1, self.string2), )

        self.string1 = """
Due to the harmonisation of the EPB-Development (EPBi) and the derivation from the preliminary architecture, the system shall consist of the following components:

- ECU (Electronic Control Unit)
- ESS (EPBi System Services)
- SSM_PB (Stand Still Manager - Park Brake) 
- PBC (Park Brake Control)
- HSB (Host Safety Barrier)
- CFA (Clamp Force Actuator)"""

        self.string2 = """
Due to the harmonisation of the EPB-Development (EPBi) and the derivation from the preliminary architecture, the system shall consist of the following components:

- EHCU (Electronic Control Unit with HCU)
- ESS (EPBi System Services)
- SSM_PB (Stand Still Manager - Park Brake) 
- PBC (Park Brake Control)
- HSB (Host Safety Barrier)
- CFA (Clamp Force Actuator)"""


        strings.append((self.string1, self.string2))

        for string1, string2 in strings:
            self.string1 = string1
            self.string2 = string2
            

            self.displayDifferences()

    def displayDifferences(self):
        
        diff = difflib.ndiff(self.string1, self.string2)

        format = QTextCharFormat()
        # format.setUnderlineColor(QColor("red"))
        # format.setUnderlineStyle(QTextCharFormat.SingleUnderline)
        format.setBackground(QColor("red"))

        cursor = self.text_edit.textCursor()
        cursor.setCharFormat(QTextCharFormat())

        cursor.insertText("\n\nString 1:\n\n")
        for i, s in enumerate(diff):
            if s[0] == ' ':
                cursor.insertText(s[2:])
            elif s[0] == '-':
                cursor.setCharFormat(format)
                cursor.insertText(s[2:])
                cursor.setCharFormat(QTextCharFormat())

        diff = difflib.ndiff(self.string1, self.string2)

        cursor.setCharFormat(QTextCharFormat())
        cursor.insertText("\n\nString 2:\n\n")
        for i, s in enumerate(diff):
            if s[0] == ' ':
                cursor.insertText(s[2:])
            elif s[0] == '+':
                cursor.setCharFormat(format)
                cursor.insertText(s[2:])
                cursor.setCharFormat(QTextCharFormat())
        
        # cursor.setCharFormat(QTextCharFormat())

if __name__ == "__main__":
    app = QApplication([])
    window = DiffTextEdit()
    window.show()
    app.exec_()
