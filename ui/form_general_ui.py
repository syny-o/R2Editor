# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\my-py-projects\R4Editor\ui\form_general.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(941, 886)
        Form.setStyleSheet("")
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.uiFrameGlobal = QtWidgets.QFrame(Form)
        self.uiFrameGlobal.setStyleSheet("QWidget{\n"
"font-size: 16px;\n"
"background-color: rgb(58, 89, 245);\n"
"background-color: rgb(20, 20, 30);\n"
"}\n"
"\n"
"QFrame, QPushButton, QLineEdit, QComboBox, QCheckBox{\n"
"    color: rgb(200, 200, 200);\n"
"\n"
"}\n"
"\n"
"QPushButton {    \n"
"    border: none;\n"
"    padding: 5;\n"
"    width: 65px;\n"
"    background-color: rgb(39, 44, 54);\n"
"    background-color: rgb(58, 89, 245);\n"
"\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(33, 37, 43);\n"
"\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"\n"
"}\n"
"\n"
"QPushButton:checked {    \n"
"    background-color: rgb(255, 100, 105);\n"
"\n"
"}\n"
"\n"
"QLineEdit, QListWidget, QComboBox{\n"
"    padding: 5;\n"
"    border: 1px solid rgb(100, 100, 100);\n"
"\n"
"}\n"
" QCheckBox{\n"
"    padding: 5;\n"
"\n"
"}\n"
"\n"
"QCheckBox::indicator {\n"
"border: 1px solid rgb(200, 200, 200);\n"
"} \n"
"\n"
"QCheckBox::indicator:checked {background-color: rgb(50,50,250);}\n"
"\n"
"\n"
"")
        self.uiFrameGlobal.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.uiFrameGlobal.setFrameShadow(QtWidgets.QFrame.Raised)
        self.uiFrameGlobal.setObjectName("uiFrameGlobal")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.uiFrameGlobal)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.uiFrameTitleBar = QtWidgets.QFrame(self.uiFrameGlobal)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiFrameTitleBar.sizePolicy().hasHeightForWidth())
        self.uiFrameTitleBar.setSizePolicy(sizePolicy)
        self.uiFrameTitleBar.setStyleSheet("background-color: rgb(58, 89, 245);")
        self.uiFrameTitleBar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.uiFrameTitleBar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.uiFrameTitleBar.setLineWidth(0)
        self.uiFrameTitleBar.setObjectName("uiFrameTitleBar")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.uiFrameTitleBar)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_top = QtWidgets.QFrame(self.uiFrameTitleBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_top.sizePolicy().hasHeightForWidth())
        self.frame_top.setSizePolicy(sizePolicy)
        self.frame_top.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_top.setStyleSheet("QPushButton {    \n"
"    border: none;\n"
"    background-color: transparent;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(44, 49, 60)\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.frame_top.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_top.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top.setLineWidth(0)
        self.frame_top.setObjectName("frame_top")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_top)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_logo = QtWidgets.QFrame(self.frame_top)
        self.frame_logo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_logo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_logo.setObjectName("frame_logo")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_logo)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.logo = QtWidgets.QLabel(self.frame_logo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy)
        self.logo.setMinimumSize(QtCore.QSize(0, 0))
        self.logo.setMaximumSize(QtCore.QSize(0, 16777215))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.logo.setFont(font)
        self.logo.setStyleSheet("color: rgb(58, 89, 245);")
        self.logo.setObjectName("logo")
        self.horizontalLayout_6.addWidget(self.logo)
        self.horizontalLayout_3.addWidget(self.frame_logo)
        self.frame_caption = QtWidgets.QFrame(self.frame_top)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_caption.sizePolicy().hasHeightForWidth())
        self.frame_caption.setSizePolicy(sizePolicy)
        self.frame_caption.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_caption.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_caption.setObjectName("frame_caption")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_caption)
        self.horizontalLayout_4.setContentsMargins(12, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.uiLabelTitle = QtWidgets.QLabel(self.frame_caption)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiLabelTitle.sizePolicy().hasHeightForWidth())
        self.uiLabelTitle.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.uiLabelTitle.setFont(font)
        self.uiLabelTitle.setObjectName("uiLabelTitle")
        self.horizontalLayout_4.addWidget(self.uiLabelTitle)
        self.horizontalLayout_3.addWidget(self.frame_caption)
        self.frame_close = QtWidgets.QFrame(self.frame_top)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_close.sizePolicy().hasHeightForWidth())
        self.frame_close.setSizePolicy(sizePolicy)
        self.frame_close.setMaximumSize(QtCore.QSize(45, 16777215))
        self.frame_close.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_close.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_close.setLineWidth(0)
        self.frame_close.setObjectName("frame_close")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_close)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.uiBtnTitleBarClose = QtWidgets.QPushButton(self.frame_close)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiBtnTitleBarClose.sizePolicy().hasHeightForWidth())
        self.uiBtnTitleBarClose.setSizePolicy(sizePolicy)
        self.uiBtnTitleBarClose.setMinimumSize(QtCore.QSize(45, 45))
        self.uiBtnTitleBarClose.setStyleSheet("")
        self.uiBtnTitleBarClose.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/20x20/icons/20x20/cil-x.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.uiBtnTitleBarClose.setIcon(icon)
        self.uiBtnTitleBarClose.setIconSize(QtCore.QSize(20, 20))
        self.uiBtnTitleBarClose.setObjectName("uiBtnTitleBarClose")
        self.horizontalLayout_5.addWidget(self.uiBtnTitleBarClose)
        self.horizontalLayout_3.addWidget(self.frame_close, 0, QtCore.Qt.AlignRight)
        self.verticalLayout_2.addWidget(self.frame_top)
        self.verticalLayout_5.addWidget(self.uiFrameTitleBar)
        self.uiFrameContent = QtWidgets.QFrame(self.uiFrameGlobal)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiFrameContent.sizePolicy().hasHeightForWidth())
        self.uiFrameContent.setSizePolicy(sizePolicy)
        self.uiFrameContent.setStyleSheet("QLabel {min-width: 100px; }")
        self.uiFrameContent.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.uiFrameContent.setFrameShadow(QtWidgets.QFrame.Raised)
        self.uiFrameContent.setObjectName("uiFrameContent")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.uiFrameContent)
        self.verticalLayout_3.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.uiMainLayout_1 = QtWidgets.QVBoxLayout()
        self.uiMainLayout_1.setContentsMargins(12, 12, 12, 12)
        self.uiMainLayout_1.setSpacing(8)
        self.uiMainLayout_1.setObjectName("uiMainLayout_1")
        self.verticalLayout_3.addLayout(self.uiMainLayout_1)
        self.uiMainLayout_2 = QtWidgets.QVBoxLayout()
        self.uiMainLayout_2.setContentsMargins(12, 12, 12, 12)
        self.uiMainLayout_2.setSpacing(8)
        self.uiMainLayout_2.setObjectName("uiMainLayout_2")
        self.verticalLayout_3.addLayout(self.uiMainLayout_2)
        self.uiMainLayout_3 = QtWidgets.QVBoxLayout()
        self.uiMainLayout_3.setContentsMargins(12, 12, 12, 12)
        self.uiMainLayout_3.setSpacing(8)
        self.uiMainLayout_3.setObjectName("uiMainLayout_3")
        self.verticalLayout_3.addLayout(self.uiMainLayout_3)
        self.uiMainLayout_4 = QtWidgets.QVBoxLayout()
        self.uiMainLayout_4.setContentsMargins(12, 12, 12, 12)
        self.uiMainLayout_4.setSpacing(8)
        self.uiMainLayout_4.setObjectName("uiMainLayout_4")
        self.verticalLayout_3.addLayout(self.uiMainLayout_4)
        self.uiMainLayout_5 = QtWidgets.QVBoxLayout()
        self.uiMainLayout_5.setContentsMargins(12, 12, 12, 12)
        self.uiMainLayout_5.setSpacing(8)
        self.uiMainLayout_5.setObjectName("uiMainLayout_5")
        self.verticalLayout_3.addLayout(self.uiMainLayout_5)
        self.verticalLayout_5.addWidget(self.uiFrameContent)
        self.uiFrameStatusBar = QtWidgets.QFrame(self.uiFrameGlobal)
        self.uiFrameStatusBar.setMinimumSize(QtCore.QSize(0, 40))
        self.uiFrameStatusBar.setMaximumSize(QtCore.QSize(16777215, 55))
        self.uiFrameStatusBar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.uiFrameStatusBar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.uiFrameStatusBar.setObjectName("uiFrameStatusBar")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.uiFrameStatusBar)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.uiBtnOK = QtWidgets.QPushButton(self.uiFrameStatusBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiBtnOK.sizePolicy().hasHeightForWidth())
        self.uiBtnOK.setSizePolicy(sizePolicy)
        self.uiBtnOK.setObjectName("uiBtnOK")
        self.horizontalLayout_12.addWidget(self.uiBtnOK)
        self.uiBtnStatusBarClose = QtWidgets.QPushButton(self.uiFrameStatusBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiBtnStatusBarClose.sizePolicy().hasHeightForWidth())
        self.uiBtnStatusBarClose.setSizePolicy(sizePolicy)
        self.uiBtnStatusBarClose.setObjectName("uiBtnStatusBarClose")
        self.horizontalLayout_12.addWidget(self.uiBtnStatusBarClose)
        self.verticalLayout_5.addWidget(self.uiFrameStatusBar, 0, QtCore.Qt.AlignRight)
        self.verticalLayout.addWidget(self.uiFrameGlobal)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Create Project"))
        self.logo.setText(_translate("Form", "R2"))
        self.uiLabelTitle.setText(_translate("Form", "Title"))
        self.uiBtnTitleBarClose.setToolTip(_translate("Form", "Close"))
        self.uiBtnOK.setText(_translate("Form", "OK"))
        self.uiBtnStatusBarClose.setText(_translate("Form", "Close"))
import files_rc
