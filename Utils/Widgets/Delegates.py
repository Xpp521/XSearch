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
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QIcon, QRegExpValidator
from PyQt5.QtWidgets import QLineEdit, QComboBox, QItemDelegate, QFileDialog


class ReadOnlyDelegate(QItemDelegate):
    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        return None


class RegexDelegate(QItemDelegate):
    def __init__(self, regex='', parent=None):
        super().__init__(parent)
        self.__regex = QRegExp(regex)

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        lineEdit = QLineEdit(QWidget)
        lineEdit.setValidator(QRegExpValidator(self.__regex, QWidget))
        return lineEdit

    def setEditorData(self, QWidget, QModelIndex):
        QWidget.setText(QModelIndex.model().data(QModelIndex))

    def setModelData(self, QWidget, QAbstractItemModel, QModelIndex):
        QAbstractItemModel.setData(QModelIndex, QWidget.text())

    def updateEditorGeometry(self, QWidget, QStyleOptionViewItem, QModelIndex):
        QWidget.setGeometry(QStyleOptionViewItem.rect)


class ComboBoxDelegate(QItemDelegate):
    def __init__(self, options, parent=None):
        super().__init__(parent)
        if isinstance(options, list):
            self.__options = options
        else:
            raise TypeError('"options" must be a list')

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        comboBox = QComboBox(QWidget)
        comboBox.addItems(self.__options)
        return comboBox

    def setEditorData(self, QWidget, QModelIndex):
        QWidget.setCurrentIndex(QWidget.findText(QModelIndex.model().data(QModelIndex)))

    def setModelData(self, QWidget, QAbstractItemModel, QModelIndex):
        QAbstractItemModel.setData(QModelIndex, QWidget.currentText())

    def updateEditorGeometry(self, QWidget, QStyleOptionViewItem, QModelIndex):
        QWidget.setGeometry(QStyleOptionViewItem.rect)


class IconDelegate(QItemDelegate):
    def __init__(self, caption='', directory='', filter='', parent=None):
        super().__init__(parent)
        self.__filter = filter
        self.__caption = caption
        self.__directory = directory

    def createEditor(self, QWidget, QStyleOptionViewItem, QModelIndex):
        path = QFileDialog.getOpenFileName(caption=self.__caption, directory=self.__directory, filter=self.__filter)[0]
        if path:
            QModelIndex.model().setData(QModelIndex, path)
            QModelIndex.model().setData(QModelIndex, QIcon(path), Qt.DecorationRole)
        return None
