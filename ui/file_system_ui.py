# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\my-py-projects\R4Editor\ui\file_system.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 777)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(0, 0))
        Form.setBaseSize(QtCore.QSize(500, 0))
        Form.setStyleSheet("border: None;\n"
"background-color: rgb(33, 37, 43);\n"
"background-color: rgb(39, 44, 54);\n"
"background-color: rgb(40, 44, 52);\n"
"\n"
"\n"
"\n"
"")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setBaseSize(QtCore.QSize(500, 0))
        self.frame.setStyleSheet("/*border-right: 1px solid rgb(39, 44, 54);*/")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.frame_3.setStyleSheet("QFrame{\n"
"background-color: rgb(39, 44, 54);\n"
"padding: 2px;\n"
"}\n"
"\n"
"QToolButton{\n"
"    border: 1px solid rgb(100, 100, 100);\n"
"    border-radius: 3px;\n"
"     padding: 10;\n"
"    border-color: rgb(40, 44, 52);\n"
"}\n"
"\n"
"QToolButton:hover{\n"
"    border-color: rgb(250, 100, 100);\n"
"}")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.frame_7 = QtWidgets.QFrame(self.frame_3)
        self.frame_7.setMaximumSize(QtCore.QSize(0, 16777215))
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_symbol_3 = QtWidgets.QLabel(self.frame_7)
        self.label_symbol_3.setStyleSheet("")
        self.label_symbol_3.setText("")
        self.label_symbol_3.setPixmap(QtGui.QPixmap(":/16x16/icons/16x16/cil-folder.png"))
        self.label_symbol_3.setObjectName("label_symbol_3")
        self.horizontalLayout_7.addWidget(self.label_symbol_3)
        self.ui_lab_root_path = QtWidgets.QLabel(self.frame_7)
        self.ui_lab_root_path.setStyleSheet("font-weight: bold;")
        self.ui_lab_root_path.setObjectName("ui_lab_root_path")
        self.horizontalLayout_7.addWidget(self.ui_lab_root_path)
        self.horizontalLayout_6.addWidget(self.frame_7)
        self.frame_8 = QtWidgets.QFrame(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy)
        self.frame_8.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.frame_8.setFocusPolicy(QtCore.Qt.NoFocus)
        self.frame_8.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.frame_8.setStyleSheet("QFrame{\n"
"background-color: rgb(39, 44, 54);\n"
"}")
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.ui_btn_disconnect_project_folder = QtWidgets.QToolButton(self.frame_8)
        self.ui_btn_disconnect_project_folder.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ui_btn_disconnect_project_folder.sizePolicy().hasHeightForWidth())
        self.ui_btn_disconnect_project_folder.setSizePolicy(sizePolicy)
        self.ui_btn_disconnect_project_folder.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ui_btn_disconnect_project_folder.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.ui_btn_disconnect_project_folder.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("c:\\my-py-projects\\R4Editor\\ui\\icons/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui_btn_disconnect_project_folder.setIcon(icon)
        self.ui_btn_disconnect_project_folder.setIconSize(QtCore.QSize(16, 16))
        self.ui_btn_disconnect_project_folder.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.ui_btn_disconnect_project_folder.setObjectName("ui_btn_disconnect_project_folder")
        self.horizontalLayout_8.addWidget(self.ui_btn_disconnect_project_folder)
        self.horizontalLayout_6.addWidget(self.frame_8, 0, QtCore.Qt.AlignRight)
        self.verticalLayout.addWidget(self.frame_3, 0, QtCore.Qt.AlignHCenter)
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setStyleSheet("QFrame{\n"
"background-color: rgb(39, 44, 54);\n"
"padding: 2px;\n"
"}")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_6 = QtWidgets.QFrame(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ui_le_filter = QtWidgets.QLineEdit(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ui_le_filter.sizePolicy().hasHeightForWidth())
        self.ui_le_filter.setSizePolicy(sizePolicy)
        self.ui_le_filter.setStyleSheet("margin-right: 5px;\n"
"background-image: url(:/16x16/icons/16x16/cil-find-in-page.png);\n"
"background-position: left center;\n"
"background-repeat: no-repeat;\n"
"padding: 5px;\n"
"padding-left: 30px;\n"
"border-radius: 1px;\n"
"\n"
"background-color: rgb(44, 49, 60);\n"
"")
        self.ui_le_filter.setObjectName("ui_le_filter")
        self.horizontalLayout_2.addWidget(self.ui_le_filter)
        self.horizontalLayout_3.addWidget(self.frame_6)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tree = QtWidgets.QTreeView(self.frame_4)
        self.tree.setMinimumSize(QtCore.QSize(0, 0))
        self.tree.setAnimated(False)
        self.tree.setObjectName("tree")
        self.tree.header().setVisible(False)
        self.verticalLayout_2.addWidget(self.tree)
        self.verticalLayout.addWidget(self.frame_4)
        self.horizontalLayout.addWidget(self.frame)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.frame_3.setToolTip(_translate("Form", "Reset Project Folder"))
        self.ui_lab_root_path.setText(_translate("Form", "No Project"))
        self.ui_btn_disconnect_project_folder.setText(_translate("Form", "J://Projects/Lixiang_X03"))
        self.ui_le_filter.setPlaceholderText(_translate("Form", "Filter"))
import files_rc