# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\my-py-projects\R4Editor\ui\form_find_replace.ui'
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
        self.frame_global = QtWidgets.QFrame(Form)
        self.frame_global.setStyleSheet("QWidget{\n"
"font-size: 16px;\n"
"background-color: rgb(58, 89, 245);\n"
"border-color: rgb(200, 200, 200);\n"
"}\n"
"\n"
"QFrame, QPushButton, QLineEdit, QComboBox, QCheckBox{\n"
"    background-color: rgb(58, 89, 245);\n"
"    color: rgb(200, 200, 200);\n"
"\n"
"}\n"
"\n"
"QPushButton {    \n"
"    border: none;\n"
"    padding: 5;\n"
"    width: 60px;\n"
"    background-color: rgb(39, 44, 54);\n"
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
"    background-color: rgb(85, 170, 255);\n"
"\n"
"}\n"
"\n"
"QLineEdit, QListWidget, QComboBox{\n"
"    padding: 5;\n"
"\n"
"}\n"
" QCheckBox{\n"
"    padding: 5;\n"
"\n"
"}\n"
"\n"
"\n"
"")
        self.frame_global.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_global.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_global.setObjectName("frame_global")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_global)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.uiFrameTitleBar = QtWidgets.QFrame(self.frame_global)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiFrameTitleBar.sizePolicy().hasHeightForWidth())
        self.uiFrameTitleBar.setSizePolicy(sizePolicy)
        self.uiFrameTitleBar.setStyleSheet("")
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
        self.horizontalLayout_4.setContentsMargins(15, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_window_name = QtWidgets.QLabel(self.frame_caption)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_window_name.sizePolicy().hasHeightForWidth())
        self.label_window_name.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.label_window_name.setFont(font)
        self.label_window_name.setObjectName("label_window_name")
        self.horizontalLayout_4.addWidget(self.label_window_name)
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
        self.ui_btn_close_x = QtWidgets.QPushButton(self.frame_close)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ui_btn_close_x.sizePolicy().hasHeightForWidth())
        self.ui_btn_close_x.setSizePolicy(sizePolicy)
        self.ui_btn_close_x.setMinimumSize(QtCore.QSize(45, 45))
        self.ui_btn_close_x.setStyleSheet("")
        self.ui_btn_close_x.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/20x20/icons/20x20/cil-x.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui_btn_close_x.setIcon(icon)
        self.ui_btn_close_x.setIconSize(QtCore.QSize(20, 20))
        self.ui_btn_close_x.setObjectName("ui_btn_close_x")
        self.horizontalLayout_5.addWidget(self.ui_btn_close_x)
        self.horizontalLayout_3.addWidget(self.frame_close, 0, QtCore.Qt.AlignRight)
        self.verticalLayout_2.addWidget(self.frame_top)
        self.verticalLayout_5.addWidget(self.uiFrameTitleBar)
        self.frame_content = QtWidgets.QFrame(self.frame_global)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_content.sizePolicy().hasHeightForWidth())
        self.frame_content.setSizePolicy(sizePolicy)
        self.frame_content.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_content.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_content.setObjectName("frame_content")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_content)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_subcontent = QtWidgets.QFrame(self.frame_content)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_subcontent.sizePolicy().hasHeightForWidth())
        self.frame_subcontent.setSizePolicy(sizePolicy)
        self.frame_subcontent.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_subcontent.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_subcontent.setObjectName("frame_subcontent")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_subcontent)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_16 = QtWidgets.QFrame(self.frame_subcontent)
        self.frame_16.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_16.setObjectName("frame_16")
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout(self.frame_16)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.label_16 = QtWidgets.QLabel(self.frame_16)
        self.label_16.setMinimumSize(QtCore.QSize(100, 0))
        self.label_16.setText("")
        self.label_16.setPixmap(QtGui.QPixmap(":/16x16/icons/16x16/cil-magnifying-glass.png"))
        self.label_16.setScaledContents(False)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_18.addWidget(self.label_16)
        self.ui_le_original_string = QtWidgets.QLineEdit(self.frame_16)
        self.ui_le_original_string.setStyleSheet("")
        self.ui_le_original_string.setObjectName("ui_le_original_string")
        self.horizontalLayout_18.addWidget(self.ui_le_original_string)
        self.verticalLayout_3.addWidget(self.frame_16)
        self.frame_17 = QtWidgets.QFrame(self.frame_subcontent)
        self.frame_17.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_17.setObjectName("frame_17")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout(self.frame_17)
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.label_17 = QtWidgets.QLabel(self.frame_17)
        self.label_17.setMinimumSize(QtCore.QSize(100, 0))
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_19.addWidget(self.label_17)
        self.ui_le_new_string = QtWidgets.QLineEdit(self.frame_17)
        self.ui_le_new_string.setStyleSheet("")
        self.ui_le_new_string.setObjectName("ui_le_new_string")
        self.horizontalLayout_19.addWidget(self.ui_le_new_string)
        self.verticalLayout_3.addWidget(self.frame_17)
        self.frame_20 = QtWidgets.QFrame(self.frame_subcontent)
        self.frame_20.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_20.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_20.setObjectName("frame_20")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_20)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ui_cb_case_sensitive = QtWidgets.QCheckBox(self.frame_20)
        self.ui_cb_case_sensitive.setObjectName("ui_cb_case_sensitive")
        self.horizontalLayout_2.addWidget(self.ui_cb_case_sensitive)
        self.ui_cb_whole_word = QtWidgets.QCheckBox(self.frame_20)
        self.ui_cb_whole_word.setChecked(True)
        self.ui_cb_whole_word.setObjectName("ui_cb_whole_word")
        self.horizontalLayout_2.addWidget(self.ui_cb_whole_word)
        self.verticalLayout_3.addWidget(self.frame_20, 0, QtCore.Qt.AlignHCenter)
        self.frame = QtWidgets.QFrame(self.frame_subcontent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(0, 300))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.ui_te_summary = QtWidgets.QTextEdit(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ui_te_summary.sizePolicy().hasHeightForWidth())
        self.ui_te_summary.setSizePolicy(sizePolicy)
        self.ui_te_summary.setBaseSize(QtCore.QSize(0, 0))
        self.ui_te_summary.setObjectName("ui_te_summary")
        self.horizontalLayout_7.addWidget(self.ui_te_summary)
        self.verticalLayout_3.addWidget(self.frame)
        self.horizontalLayout.addWidget(self.frame_subcontent, 0, QtCore.Qt.AlignTop)
        self.verticalLayout_5.addWidget(self.frame_content)
        self.uiFrameStatusBar = QtWidgets.QFrame(self.frame_global)
        self.uiFrameStatusBar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.uiFrameStatusBar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.uiFrameStatusBar.setObjectName("uiFrameStatusBar")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.uiFrameStatusBar)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.uiBtnOK = QtWidgets.QPushButton(self.uiFrameStatusBar)
        self.uiBtnOK.setObjectName("uiBtnOK")
        self.horizontalLayout_12.addWidget(self.uiBtnOK)
        self.uiBtnClose = QtWidgets.QPushButton(self.uiFrameStatusBar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiBtnClose.sizePolicy().hasHeightForWidth())
        self.uiBtnClose.setSizePolicy(sizePolicy)
        self.uiBtnClose.setObjectName("uiBtnClose")
        self.horizontalLayout_12.addWidget(self.uiBtnClose)
        self.verticalLayout_5.addWidget(self.uiFrameStatusBar, 0, QtCore.Qt.AlignRight)
        self.verticalLayout.addWidget(self.frame_global)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Create Project"))
        self.logo.setText(_translate("Form", "R2"))
        self.label_window_name.setText(_translate("Form", "Find and Replace"))
        self.ui_btn_close_x.setToolTip(_translate("Form", "Close"))
        self.label_17.setText(_translate("Form", "Replace:"))
        self.ui_cb_case_sensitive.setText(_translate("Form", "Case Sensitive"))
        self.ui_cb_whole_word.setText(_translate("Form", "Whole Words"))
        self.ui_te_summary.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:16px; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8.25pt;\"><br /></p></body></html>"))
        self.uiBtnOK.setText(_translate("Form", "Run"))
        self.uiBtnClose.setText(_translate("Form", "Close"))
import files_rc