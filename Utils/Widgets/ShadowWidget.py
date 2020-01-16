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
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QBrush, QColor, QPainter, QPainterPath


class ShadowWidget(QWidget):
    """
    Window with shadow. Waiting to be done.
    """
    def __init__(self, parent=None, shadowPos=None):
        """
        :param QWidget parent: the parent widget.
        :param list shadowPos: shadow position list.
        The four elements represent top, right, bottom and left respectively.
        """
        super().__init__(parent)
        self.__shadowPos = [False, False, False, False]
        if shadowPos:
            if not self.setShadowPos(shadowPos):
                raise TypeError('shadowPos must be a list, and its length must be 4')

    def setShadowPos(self, shadow_pos):
        """
        :param list shadow_pos: shadow position list.
        The four elements represent top, right, bottom and left respectively.
        :rtype: bool.
        """
        if isinstance(shadow_pos, list) and 4 == len(shadow_pos):
            self.__shadowPos = [True if p else False for p in shadow_pos]
            return True
        return False

    def paintEvent(self, event):
        if any(self.__shadowPos):
            path = QPainterPath()
            path.setFillRule(Qt.WindingFill)
            path.addRect(10, 10, self.width()-20, self.height()-20)
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            painter.fillPath(path, QBrush(Qt.white))
            color = QColor(0, 0, 0, 50)
            for i in range(10):
                path = QPainterPath()
                path.setFillRule(Qt.WindingFill)
                path.addRect(10-i, 10-i, self.width()-(10-i)*2, self.height()-(10-i)*2)
                color.setAlpha(150-i**0.5*50)
                painter.setPen(color)
                painter.drawPath(path)
