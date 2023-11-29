# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\my-py-projects\R4Editor\ui\dashboard.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1314, 834)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setStyleSheet("QWidget, QFrame, QPushButton, QLineEdit{\n"
"    background-color: rgb(27, 29, 35);\n"
"    color: rgb(200, 200, 200);\n"
"    border: none;\n"
"}\n"
"\n"
"\n"
"\n"
"QListWidget{\n"
"    padding: 10px 20px;\n"
"}\n"
"\n"
"QListWidget::item{\n"
"    color: rgb(180,180,180);\n"
"    padding: 5px;\n"
"    text-align: right;\n"
"}\n"
"\n"
"QListWidget::item:selected{\n"
"    font-style: bold;\n"
"}\n"
"\n"
"\n"
"QPushButton {    \n"
"    border: none;\n"
"    padding: 7 17;\n"
"    width: 50px;\n"
"    background-color: rgb(39, 44, 54);\n"
"}\n"
"QPushButton:hover {\n"
"    color: rgb(200, 200, 200);\n"
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
"QPushButton:disabled {    \n"
"    color: rgb(100, 100, 100);\n"
"\n"
"}\n"
"\n"
"QLabel{\n"
"    padding: 7 17;\n"
"}")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setMaximumSize(QtCore.QSize(800, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_logo_2 = QtWidgets.QFrame(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_logo_2.sizePolicy().hasHeightForWidth())
        self.frame_logo_2.setSizePolicy(sizePolicy)
        self.frame_logo_2.setMinimumSize(QtCore.QSize(0, 300))
        self.frame_logo_2.setStyleSheet("/*background: transparent;\n"
"background-image: url(:/16x16/icons/16x16/cil-terminal.png);\n"
"background-position: center;\n"
"background-repeat: no-repeat;*/")
        self.frame_logo_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_logo_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_logo_2.setObjectName("frame_logo_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_logo_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_6 = QtWidgets.QLabel(self.frame_logo_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("ZF Serif")
        font.setPointSize(72)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(58, 89, 245);")
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_3.addWidget(self.label_6, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addWidget(self.frame_logo_2, 0, QtCore.Qt.AlignHCenter)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setStyleSheet("")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_2 = QtWidgets.QLabel(self.frame_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(150, 150, 150);")
        self.label_2.setObjectName("label_2")
        self.verticalLayout_6.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter)
        self.ui_lw_projects = QtWidgets.QListWidget(self.frame_4)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.ui_lw_projects.setFont(font)
        self.ui_lw_projects.setStyleSheet("")
        self.ui_lw_projects.setViewMode(QtWidgets.QListView.ListMode)
        self.ui_lw_projects.setObjectName("ui_lw_projects")
        self.verticalLayout_6.addWidget(self.ui_lw_projects)
        self.verticalLayout_2.addWidget(self.frame_4)
        self.frame_top = QtWidgets.QFrame(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_top.sizePolicy().hasHeightForWidth())
        self.frame_top.setSizePolicy(sizePolicy)
        self.frame_top.setMaximumSize(QtCore.QSize(16777215, 0))
        self.frame_top.setStyleSheet("QPushButton {    \n"
"    border: none;\n"
"    background-color: transparent;\n"
"\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(44, 49, 60)\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}\n"
"\n"
"QFrame:{\n"
"padding: 5px;\n"
"}")
        self.frame_top.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_top.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top.setObjectName("frame_top")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_top)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
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
        self.horizontalLayout_4.addWidget(self.frame_logo)
        self.frame_caption = QtWidgets.QFrame(self.frame_top)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_caption.sizePolicy().hasHeightForWidth())
        self.frame_caption.setSizePolicy(sizePolicy)
        self.frame_caption.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_caption.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_caption.setObjectName("frame_caption")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_caption)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
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
        self.label_window_name.setText("")
        self.label_window_name.setObjectName("label_window_name")
        self.horizontalLayout_5.addWidget(self.label_window_name)
        self.horizontalLayout_4.addWidget(self.frame_caption)
        self.frame_close = QtWidgets.QFrame(self.frame_top)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_close.sizePolicy().hasHeightForWidth())
        self.frame_close.setSizePolicy(sizePolicy)
        self.frame_close.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_close.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_close.setObjectName("frame_close")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_close)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
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
        self.horizontalLayout_7.addWidget(self.btn_close)
        self.horizontalLayout_4.addWidget(self.frame_close, 0, QtCore.Qt.AlignRight)
        self.verticalLayout_2.addWidget(self.frame_top)
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 0))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_24.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_24.setSpacing(0)
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.frame_17 = QtWidgets.QFrame(self.frame_2)
        self.frame_17.setStyleSheet("")
        self.frame_17.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_17.setObjectName("frame_17")
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout(self.frame_17)
        self.horizontalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_20.setSpacing(0)
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.frame_21 = QtWidgets.QFrame(self.frame_17)
        self.frame_21.setStyleSheet("")
        self.frame_21.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_21.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_21.setObjectName("frame_21")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_21)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_bottom_buttons = QtWidgets.QFrame(self.frame_21)
        self.frame_bottom_buttons.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_bottom_buttons.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_bottom_buttons.setObjectName("frame_bottom_buttons")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_bottom_buttons)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ui_btn_ok = QtWidgets.QPushButton(self.frame_bottom_buttons)
        self.ui_btn_ok.setEnabled(False)
        self.ui_btn_ok.setObjectName("ui_btn_ok")
        self.horizontalLayout.addWidget(self.ui_btn_ok)
        self.ui_btn_open = QtWidgets.QPushButton(self.frame_bottom_buttons)
        self.ui_btn_open.setObjectName("ui_btn_open")
        self.horizontalLayout.addWidget(self.ui_btn_open)
        self.ui_btn_remove = QtWidgets.QPushButton(self.frame_bottom_buttons)
        self.ui_btn_remove.setEnabled(False)
        self.ui_btn_remove.setObjectName("ui_btn_remove")
        self.horizontalLayout.addWidget(self.ui_btn_remove)
        self.horizontalLayout_2.addWidget(self.frame_bottom_buttons)
        self.horizontalLayout_20.addWidget(self.frame_21, 0, QtCore.Qt.AlignLeft)
        self.frame_23 = QtWidgets.QFrame(self.frame_17)
        self.frame_23.setEnabled(True)
        self.frame_23.setStyleSheet("")
        self.frame_23.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_23.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_23.setObjectName("frame_23")
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout(self.frame_23)
        self.horizontalLayout_23.setContentsMargins(0, 0, 9, 0)
        self.horizontalLayout_23.setSpacing(0)
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.ui_btn_close = QtWidgets.QPushButton(self.frame_23)
        self.ui_btn_close.setObjectName("ui_btn_close")
        self.horizontalLayout_23.addWidget(self.ui_btn_close)
        self.horizontalLayout_20.addWidget(self.frame_23, 0, QtCore.Qt.AlignRight)
        self.horizontalLayout_24.addWidget(self.frame_17)
        self.verticalLayout_2.addWidget(self.frame_2)
        self.horizontalLayout_8.addWidget(self.frame)
        self.frame_3 = QtWidgets.QFrame(Form)
        self.frame_3.setStyleSheet("QWidget, QFrame, QPushButton, QLineEdit{\n"
"    background-color: rgb(33, 37, 43);\n"
"    color: rgb(200, 200, 200);\n"
"    border: none;\n"
"}\n"
"\n"
"QToolButton{\n"
"    color: rgb(58, 89, 245);\n"
"}\n"
"\n"
"QToolButton:hover{\n"
"    color: rgb(200, 200, 200);\n"
"}")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_10 = QtWidgets.QFrame(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_10.sizePolicy().hasHeightForWidth())
        self.frame_10.setSizePolicy(sizePolicy)
        self.frame_10.setMaximumSize(QtCore.QSize(16777215, 0))
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_10)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_11 = QtWidgets.QFrame(self.frame_10)
        self.frame_11.setMinimumSize(QtCore.QSize(0, 130))
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame_11)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_5 = QtWidgets.QLabel(self.frame_11)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("ZF Serif")
        font.setPointSize(72)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(58, 89, 245);")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_10.addWidget(self.label_5)
        self.verticalLayout_4.addWidget(self.frame_11, 0, QtCore.Qt.AlignHCenter)
        self.frame_12 = QtWidgets.QFrame(self.frame_10)
        self.frame_12.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setObjectName("frame_12")
        self.verticalLayout_4.addWidget(self.frame_12)
        self.verticalLayout.addWidget(self.frame_10)
        self.frame_5 = QtWidgets.QFrame(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy)
        self.frame_5.setStyleSheet("")
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_9 = QtWidgets.QFrame(self.frame_5)
        self.frame_9.setStyleSheet("")
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_9)
        self.verticalLayout_5.setSpacing(10)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_3 = QtWidgets.QLabel(self.frame_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(150, 150, 150);")
        self.label_3.setObjectName("label_3")
        self.verticalLayout_5.addWidget(self.label_3)
        self.ui_btn_new_project = QtWidgets.QToolButton(self.frame_9)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ui_btn_new_project.setFont(font)
        self.ui_btn_new_project.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ui_btn_new_project.setFocusPolicy(QtCore.Qt.NoFocus)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/20x20/icons/20x20/cil-folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui_btn_new_project.setIcon(icon1)
        self.ui_btn_new_project.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.ui_btn_new_project.setObjectName("ui_btn_new_project")
        self.verticalLayout_5.addWidget(self.ui_btn_new_project)
        self.ui_btn_open_project = QtWidgets.QToolButton(self.frame_9)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ui_btn_open_project.setFont(font)
        self.ui_btn_open_project.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/20x20/icons/20x20/cil-folder-open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui_btn_open_project.setIcon(icon2)
        self.ui_btn_open_project.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.ui_btn_open_project.setObjectName("ui_btn_open_project")
        self.verticalLayout_5.addWidget(self.ui_btn_open_project)
        self.ui_btn_editor = QtWidgets.QToolButton(self.frame_9)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ui_btn_editor.setFont(font)
        self.ui_btn_editor.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/20x20/icons/20x20/cil-file.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui_btn_editor.setIcon(icon3)
        self.ui_btn_editor.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.ui_btn_editor.setObjectName("ui_btn_editor")
        self.verticalLayout_5.addWidget(self.ui_btn_editor)
        self.ui_btn_configuration = QtWidgets.QToolButton(self.frame_9)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ui_btn_configuration.setFont(font)
        self.ui_btn_configuration.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/20x20/icons/20x20/cil-settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui_btn_configuration.setIcon(icon4)
        self.ui_btn_configuration.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.ui_btn_configuration.setObjectName("ui_btn_configuration")
        self.verticalLayout_5.addWidget(self.ui_btn_configuration)
        self.verticalLayout_3.addWidget(self.frame_9, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.frame_8 = QtWidgets.QFrame(self.frame_5)
        self.frame_8.setMaximumSize(QtCore.QSize(16777215, 0))
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.verticalLayout_3.addWidget(self.frame_8)
        self.verticalLayout.addWidget(self.frame_5)
        self.frame_7 = QtWidgets.QFrame(self.frame_3)
        self.frame_7.setMinimumSize(QtCore.QSize(0, 100))
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.verticalLayout.addWidget(self.frame_7)
        self.frame_6 = QtWidgets.QFrame(self.frame_3)
        self.frame_6.setMaximumSize(QtCore.QSize(16777215, 0))
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout.addWidget(self.frame_6)
        self.horizontalLayout_8.addWidget(self.frame_3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_6.setText(_translate("Form", "R2"))
        self.label_2.setText(_translate("Form", "Recent Projects"))
        self.logo.setText(_translate("Form", "R2"))
        self.btn_close.setToolTip(_translate("Form", "Close"))
        self.ui_btn_ok.setText(_translate("Form", "OK"))
        self.ui_btn_open.setText(_translate("Form", "Open..."))
        self.ui_btn_remove.setText(_translate("Form", "Remove"))
        self.ui_btn_close.setText(_translate("Form", "Cancel"))
        self.label_5.setText(_translate("Form", "R2"))
        self.label_3.setText(_translate("Form", "Start"))
        self.ui_btn_new_project.setText(_translate("Form", "New Project..."))
        self.ui_btn_open_project.setText(_translate("Form", "Open Project..."))
        self.ui_btn_editor.setText(_translate("Form", "Script Editor..."))
        self.ui_btn_configuration.setText(_translate("Form", "Configuration..."))
import files_rc