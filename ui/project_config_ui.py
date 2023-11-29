# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\my-py-projects\R4Editor\ui\project_config.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(669, 467)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_global = QtWidgets.QFrame(Form)
        self.frame_global.setStyleSheet("QFrame, QPushButton, QLineEdit{\n"
"    background-color: rgb(27, 29, 35);\n"
"    color: rgb(200, 200, 200);\n"
"}\n"
"\n"
"QPushButton {    \n"
"    border: none;\n"
"    padding: 5;\n"
"    width: 50px;\n"
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
"QLineEdit, QListWidget{\n"
"    padding: 5;\n"
"    background-color: rgb(39, 44, 54);\n"
"    border: 1px solid rgb(100, 100, 100);\n"
"}\n"
"\n"
"\n"
"")
        self.frame_global.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_global.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_global.setObjectName("frame_global")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_global)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_top = QtWidgets.QFrame(self.frame_global)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_top.sizePolicy().hasHeightForWidth())
        self.frame_top.setSizePolicy(sizePolicy)
        self.frame_top.setMaximumSize(QtCore.QSize(16777215, 20))
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
        self.logo.setMinimumSize(QtCore.QSize(30, 0))
        font = QtGui.QFont()
        font.setFamily("ZF Serif")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        font.setStrikeOut(False)
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
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_window_name = QtWidgets.QLabel(self.frame_caption)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_window_name.sizePolicy().hasHeightForWidth())
        self.label_window_name.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_window_name.setFont(font)
        self.label_window_name.setObjectName("label_window_name")
        self.horizontalLayout_4.addWidget(self.label_window_name)
        self.horizontalLayout_3.addWidget(self.frame_caption)
        self.frame_close = QtWidgets.QFrame(self.frame_top)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_close.sizePolicy().hasHeightForWidth())
        self.frame_close.setSizePolicy(sizePolicy)
        self.frame_close.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_close.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_close.setObjectName("frame_close")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_close)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.btn_close = QtWidgets.QPushButton(self.frame_close)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_close.sizePolicy().hasHeightForWidth())
        self.btn_close.setSizePolicy(sizePolicy)
        self.btn_close.setMinimumSize(QtCore.QSize(0, 0))
        self.btn_close.setMaximumSize(QtCore.QSize(20, 16777215))
        self.btn_close.setStyleSheet("")
        self.btn_close.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/16x16/icons/16x16/cil-x.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_close.setIcon(icon)
        self.btn_close.setObjectName("btn_close")
        self.horizontalLayout_5.addWidget(self.btn_close)
        self.horizontalLayout_3.addWidget(self.frame_close, 0, QtCore.Qt.AlignRight)
        self.verticalLayout_2.addWidget(self.frame_top)
        self.stackedWidget = QtWidgets.QStackedWidget(self.frame_global)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setObjectName("page_1")
        self.frame_content = QtWidgets.QFrame(self.page_1)
        self.frame_content.setGeometry(QtCore.QRect(0, 0, 651, 371))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_content.sizePolicy().hasHeightForWidth())
        self.frame_content.setSizePolicy(sizePolicy)
        self.frame_content.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_content.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_content.setObjectName("frame_content")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_content)
        self.verticalLayout_3.setContentsMargins(-1, 20, -1, -1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame = QtWidgets.QFrame(self.frame_content)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setMinimumSize(QtCore.QSize(80, 0))
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.le_project = QtWidgets.QLineEdit(self.frame)
        self.le_project.setObjectName("le_project")
        self.horizontalLayout_2.addWidget(self.le_project)
        self.btn_project = QtWidgets.QPushButton(self.frame)
        self.btn_project.setMaximumSize(QtCore.QSize(25, 16777215))
        self.btn_project.setStyleSheet("background-color: None;")
        self.btn_project.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/16x16/icons/16x16/cil-folder-open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_project.setIcon(icon1)
        self.btn_project.setObjectName("btn_project")
        self.horizontalLayout_2.addWidget(self.btn_project)
        self.verticalLayout_3.addWidget(self.frame)
        self.frame_bottom_buttons = QtWidgets.QFrame(self.page_1)
        self.frame_bottom_buttons.setGeometry(QtCore.QRect(440, 370, 212, 43))
        self.frame_bottom_buttons.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_bottom_buttons.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_bottom_buttons.setObjectName("frame_bottom_buttons")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_bottom_buttons)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_next = QtWidgets.QPushButton(self.frame_bottom_buttons)
        self.btn_next.setObjectName("btn_next")
        self.horizontalLayout.addWidget(self.btn_next)
        self.btn_cancel = QtWidgets.QPushButton(self.frame_bottom_buttons)
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout.addWidget(self.btn_cancel)
        self.stackedWidget.addWidget(self.page_1)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setMaximumSize(QtCore.QSize(649, 413))
        self.page_2.setObjectName("page_2")
        self.frame_content_2 = QtWidgets.QFrame(self.page_2)
        self.frame_content_2.setGeometry(QtCore.QRect(0, -6, 651, 391))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_content_2.sizePolicy().hasHeightForWidth())
        self.frame_content_2.setSizePolicy(sizePolicy)
        self.frame_content_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_content_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_content_2.setObjectName("frame_content_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_content_2)
        self.verticalLayout_5.setContentsMargins(-1, 20, -1, -1)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.frame_7 = QtWidgets.QFrame(self.frame_content_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_7 = QtWidgets.QLabel(self.frame_7)
        self.label_7.setMinimumSize(QtCore.QSize(120, 0))
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_7.addWidget(self.label_7)
        self.lw_cond_file = QtWidgets.QListWidget(self.frame_7)
        self.lw_cond_file.setMaximumSize(QtCore.QSize(16777215, 100))
        self.lw_cond_file.setObjectName("lw_cond_file")
        self.horizontalLayout_7.addWidget(self.lw_cond_file)
        self.btn_cond_file = QtWidgets.QPushButton(self.frame_7)
        self.btn_cond_file.setMaximumSize(QtCore.QSize(25, 16777215))
        self.btn_cond_file.setStyleSheet("background-color: None;")
        self.btn_cond_file.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/16x16/icons/16x16/cil-library-add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_cond_file.setIcon(icon2)
        self.btn_cond_file.setObjectName("btn_cond_file")
        self.horizontalLayout_7.addWidget(self.btn_cond_file)
        self.verticalLayout_5.addWidget(self.frame_7)
        self.frame_8 = QtWidgets.QFrame(self.frame_content_2)
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_8 = QtWidgets.QLabel(self.frame_8)
        self.label_8.setMinimumSize(QtCore.QSize(120, 0))
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_9.addWidget(self.label_8)
        self.le_dspace_file = QtWidgets.QLineEdit(self.frame_8)
        self.le_dspace_file.setObjectName("le_dspace_file")
        self.horizontalLayout_9.addWidget(self.le_dspace_file)
        self.btn_dspace_file = QtWidgets.QPushButton(self.frame_8)
        self.btn_dspace_file.setMaximumSize(QtCore.QSize(25, 16777215))
        self.btn_dspace_file.setStyleSheet("background-color: None;")
        self.btn_dspace_file.setText("")
        self.btn_dspace_file.setIcon(icon1)
        self.btn_dspace_file.setObjectName("btn_dspace_file")
        self.horizontalLayout_9.addWidget(self.btn_dspace_file)
        self.verticalLayout_5.addWidget(self.frame_8)
        self.frame_9 = QtWidgets.QFrame(self.frame_content_2)
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_9)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_9 = QtWidgets.QLabel(self.frame_9)
        self.label_9.setMinimumSize(QtCore.QSize(120, 0))
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_8.addWidget(self.label_9)
        self.lw_a2l_file = QtWidgets.QListWidget(self.frame_9)
        self.lw_a2l_file.setMaximumSize(QtCore.QSize(16777215, 100))
        self.lw_a2l_file.setObjectName("lw_a2l_file")
        self.horizontalLayout_8.addWidget(self.lw_a2l_file)
        self.btn_a2l_file = QtWidgets.QPushButton(self.frame_9)
        self.btn_a2l_file.setMaximumSize(QtCore.QSize(25, 16777215))
        self.btn_a2l_file.setStyleSheet("background-color: None;")
        self.btn_a2l_file.setText("")
        self.btn_a2l_file.setIcon(icon2)
        self.btn_a2l_file.setObjectName("btn_a2l_file")
        self.horizontalLayout_8.addWidget(self.btn_a2l_file)
        self.verticalLayout_5.addWidget(self.frame_9)
        self.frame_10 = QtWidgets.QFrame(self.frame_content_2)
        self.frame_10.setMaximumSize(QtCore.QSize(16777215, 0))
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame_10)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_10 = QtWidgets.QLabel(self.frame_10)
        self.label_10.setMinimumSize(QtCore.QSize(120, 0))
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_10.addWidget(self.label_10)
        self.lw_req_file = QtWidgets.QListWidget(self.frame_10)
        self.lw_req_file.setMaximumSize(QtCore.QSize(16777215, 100))
        self.lw_req_file.setObjectName("lw_req_file")
        self.horizontalLayout_10.addWidget(self.lw_req_file)
        self.btn_req_file = QtWidgets.QPushButton(self.frame_10)
        self.btn_req_file.setMaximumSize(QtCore.QSize(25, 16777215))
        self.btn_req_file.setStyleSheet("background-color: None;")
        self.btn_req_file.setText("")
        self.btn_req_file.setIcon(icon2)
        self.btn_req_file.setObjectName("btn_req_file")
        self.horizontalLayout_10.addWidget(self.btn_req_file)
        self.verticalLayout_5.addWidget(self.frame_10)
        self.frame_bottom_buttons_2 = QtWidgets.QFrame(self.page_2)
        self.frame_bottom_buttons_2.setGeometry(QtCore.QRect(440, 380, 212, 43))
        self.frame_bottom_buttons_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_bottom_buttons_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_bottom_buttons_2.setObjectName("frame_bottom_buttons_2")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.frame_bottom_buttons_2)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.btn_back = QtWidgets.QPushButton(self.frame_bottom_buttons_2)
        self.btn_back.setObjectName("btn_back")
        self.horizontalLayout_12.addWidget(self.btn_back)
        self.btn_ok = QtWidgets.QPushButton(self.frame_bottom_buttons_2)
        self.btn_ok.setObjectName("btn_ok")
        self.horizontalLayout_12.addWidget(self.btn_ok)
        self.stackedWidget.addWidget(self.page_2)
        self.verticalLayout_2.addWidget(self.stackedWidget)
        self.verticalLayout.addWidget(self.frame_global)

        self.retranslateUi(Form)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Create Project"))
        self.logo.setText(_translate("Form", "R2"))
        self.label_window_name.setText(_translate("Form", "Create Project"))
        self.btn_close.setToolTip(_translate("Form", "Close"))
        self.label.setText(_translate("Form", "Location:"))
        self.btn_next.setText(_translate("Form", "Next"))
        self.btn_cancel.setText(_translate("Form", "Cancel"))
        self.label_7.setText(_translate("Form", "Condition Files:"))
        self.label_8.setText(_translate("Form", "DSpace Mapping File:"))
        self.label_9.setText(_translate("Form", "A2L Files:"))
        self.label_10.setText(_translate("Form", "Doors Project Paths:"))
        self.btn_back.setText(_translate("Form", "Back"))
        self.btn_ok.setText(_translate("Form", "OK"))
import files_rc