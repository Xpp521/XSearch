# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SettingDialog_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_setting(object):
    def setupUi(self, Dialog_setting):
        Dialog_setting.setObjectName("Dialog_setting")
        Dialog_setting.resize(755, 539)
        self.ok = QtWidgets.QPushButton(Dialog_setting)
        self.ok.setGeometry(QtCore.QRect(400, 480, 97, 29))
        self.ok.setObjectName("ok")
        self.cancel = QtWidgets.QPushButton(Dialog_setting)
        self.cancel.setGeometry(QtCore.QRect(510, 480, 97, 29))
        self.cancel.setObjectName("cancel")
        self.apply = QtWidgets.QPushButton(Dialog_setting)
        self.apply.setGeometry(QtCore.QRect(620, 480, 97, 29))
        self.apply.setObjectName("apply")
        self.tabWidget = QtWidgets.QTabWidget(Dialog_setting)
        self.tabWidget.setGeometry(QtCore.QRect(30, 50, 651, 381))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.tabWidget.setFont(font)
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab1 = QtWidgets.QWidget()
        self.tab1.setObjectName("tab1")
        self.tabWidget.addTab(self.tab1, "")
        self.tab2 = QtWidgets.QWidget()
        self.tab2.setObjectName("tab2")
        self.tabWidget.addTab(self.tab2, "")

        self.retranslateUi(Dialog_setting)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog_setting)

    def retranslateUi(self, Dialog_setting):
        _translate = QtCore.QCoreApplication.translate
        Dialog_setting.setWindowTitle(_translate("Dialog_setting", "设置"))
        self.ok.setText(_translate("Dialog_setting", "确定"))
        self.cancel.setText(_translate("Dialog_setting", "取消"))
        self.apply.setText(_translate("Dialog_setting", "应用"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), _translate("Dialog_setting", "常规"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), _translate("Dialog_setting", "其它"))

