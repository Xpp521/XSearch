# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Xpp521
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Form implementation generated from reading ui file 'SearchDialog_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
from os.path import join
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(690, 50)
        Dialog.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Dialog.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(0, 0, 690, 50))
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(11, 15, 20, 20))
        self.label.setObjectName("label")
        self.widget = QtWidgets.QWidget(Dialog, QtCore.Qt.ToolTip | QtCore.Qt.FramelessWindowHint)
        self.widget.setGeometry(QtCore.QRect(0, 0, 690, 0))
        self.widget.setObjectName("widget")
        self.widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.widget.setVisible(False)
        self.listView = QtWidgets.QListView(self.widget)
        self.listView.setGeometry(QtCore.QRect(0, 0, 690, 0))
        self.listView.setObjectName("listView")
        self.listView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowIcon(QIcon(join('Icons', 'XSearch.ico')))
        from Languages import Strings
        Dialog.setWindowTitle(Strings.APP_NAME)
