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
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel


class ListModel(QStandardItemModel):
    """
    ListModel.
    """
    def __init__(self, rows, parent=None):
        super().__init__(rows, 1, parent)
        self.__customData = [0 for _ in range(rows)]
        self.__dataCount = 0

    def index(self, p_int, parent=None, *args, **kwargs):
        return super().index(p_int, 0)

    def isEmptyRow(self, row):
        index = self.index(row)
        return not any((self.data(index), self.data(index, Qt.DecorationRole), self.__customData[row]))

    def setRow(self, row, text='', icon=None, customData=0):
        """
        Set a row data.
        :param int row: row index.
        :param str text: text.
        :param QPixmap, QIcon icon: icon.
        :param int customData: data type.
        :rtype: bool.
        """
        isEmptyBefore = self.isEmptyRow(row)
        isEmptyAfter = not any((text, icon, customData))
        r = self.setItemData(self.index(row), {Qt.DisplayRole: text, Qt.DecorationRole: icon})
        if r:
            self.__customData[row] = customData
            if isEmptyBefore and not isEmptyAfter:
                self.__dataCount += 1
            elif not isEmptyBefore and isEmptyAfter:
                if self.__dataCount > 0:
                    self.__dataCount -= 1
        return r

    def setRows(self, beginRow, stringList, icon=None, customData=None):
        return all([self.setRow(beginRow + i, row, icon, customData) for i, row in enumerate(stringList)])

    def clearRow(self, row):
        """Clear a row data."""
        return self.setRow(row)

    def clearRows(self, beginRow=0, count=None):
        count = count if isinstance(count, int) and 0 < count <= self.rowCount() else self.rowCount()
        return all([self.clearRow(beginRow + i) for i in range(count)])

    def text(self, row):
        """
        Get the text of a row.
        :param int row: row index.
        :rtype: str.
        """
        if 0 <= row < self.rowCount():
            return self.data(self.index(row))
        else:
            return ''

    def customData(self, row):
        """
        Get the type of a row.
        :param int row: row index.
        :rtype: int.
        """
        if 0 <= row < self.rowCount():
            return self.__customData[row]
        else:
            return -1

    def dataCount(self):
        return self.__dataCount

    def setRowCount(self, p_int):
        super().setRowCount(p_int)
        count = len(self.__customData)
        if p_int <= count:
            self.__customData = self.__customData[:p_int]
        else:
            self.__customData = self.__customData.extend([0 for _ in range(p_int - count)])

    def setColumnCount(self, p_int):
        pass

    def appendRow(self, text=None, icon=None, customData=None):
        row = self.rowCount()
        self.setRowCount(row + 1)
        self.setRow(row, text, icon, customData)

    def appendColumn(self, Iterable, QStandardItem=None):
        pass

    def clear(self):
        pass

    def beginInsertColumns(self, *args, **kwargs):
        pass

    def beginInsertRows(self, *args, **kwargs):
        pass

    def beginMoveColumns(self, *args, **kwargs):
        pass

    def beginMoveRows(self, *args, **kwargs):
        pass

    def beginRemoveColumns(self, *args, **kwargs):
        pass

    def beginRemoveRows(self, *args, **kwargs):
        pass

    def beginResetModel(self, *args, **kwargs):
        pass

    def endInsertColumns(self, *args, **kwargs):
        pass

    def endInsertRows(self, *args, **kwargs):
        pass

    def endMoveColumns(self, *args, **kwargs):
        pass

    def endMoveRows(self, *args, **kwargs):
        pass

    def endRemoveColumns(self, *args, **kwargs):
        pass

    def endRemoveRows(self, *args, **kwargs):
        pass

    def endResetModel(self, *args, **kwargs):
        pass

    def insertColumn(self, p_int, *__args):
        pass

    def insertColumns(self, p_int, p_int_1, parent=None, *args, **kwargs):
        pass

    def insertRow(self, p_int, *__args):
        pass

    def insertRows(self, p_int, p_int_1, parent=None, *args, **kwargs):
        pass

    def removeColumns(self, p_int, p_int_1, parent=None, *args, **kwargs):
        pass

    def removeRows(self, p_int, p_int_1, parent=None, *args, **kwargs):
        pass
