################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##
################################################################################
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtTest

from progress_bar.ui_modern_progress_bar import Ui_Form

# GLOBALS
counter = 0
jumper = 10

class ModernProgressBar(QWidget, Ui_Form):
    def __init__(self, color, header_text):
        super().__init__()
        self.setupUi(self)

        self.color = color
        self.labelHeader.setText(header_text)
        self.labelHeader.setStyleSheet(f'color: {self.color}; background-color: none;')
        self.labelPercen.setStyleSheet(f'color: {self.color}; background-color: none;')
        # self.labelFooter.setStyleSheet(f'color: {self.color}; background-color: none;')
        # self.labelFooter.setText(f'{actual_number} / {total_number}')

        # self.setValue(int(actual_number/total_number*100))

        self.update_value(0, 0)

    ## ==> SET VALUES TO DEF progressBarValue
    def setValue(self, value):

        # HTML TEXT PERCENTAGE
        htmlText = """<p align="center"><span style=" font-size:20pt;">{VALUE}</span><span style=" font-size:20pt; vertical-align:super;">%</span></p>"""
        self.labelPercen.setText(htmlText.replace("{VALUE}", str(value)))

        # CALL DEF progressBarValue
        self.progressBarValue(value, self.circularProgress_5, self.color)


    ## DEF PROGRESS BAR VALUE
    ########################################################################
    def progressBarValue(self, value, widget, color):
        # PROGRESSBAR STYLESHEET BASE
        styleSheet = """
            QFrame{
            	border-radius: 110px;
            	background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255, 0, 127, 0), stop:{STOP_2} {COLOR});
            }
            """

        # GET PROGRESS BAR VALUE, CONVERT TO FLOAT AND INVERT VALUES
        # stop works of 1.000 to 0.000
        progress = (100 - value) / 100.0

        # GET NEW VALUES
        stop_1 = str(progress - 0.001)
        stop_2 = str(progress)

        # FIX MAX VALUE
        if value == 100:
            stop_1 = "1.000"
            stop_2 = "1.000"

        # SET VALUES TO NEW STYLESHEET
        newStylesheet = styleSheet.replace("{STOP_1}", stop_1).replace("{STOP_2}", stop_2).replace("{COLOR}", color)

        # APPLY STYLESHEET WITH NEW VALUES
        widget.setStyleSheet(newStylesheet)


    def update_value(self, total_number, actual_number, animation=False):
        try:
            percentage = int(actual_number/total_number*100)
        except:
            percentage = 0
        self.labelFooter.setText(f'{actual_number} / {total_number}')
        if animation:
            for i in range(percentage+1):
                self.setValue(i)
                QtTest.QTest.qWait(5)
        else:
            self.setValue(percentage)

