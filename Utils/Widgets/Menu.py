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
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMenu


class SingleLevelMenu(QMenu):
    """An untitled translucent single level menu.
    SingleLevelMenu(actionLabels: list, icons: list=None, parent: QWidget = None)
    """
    def __init__(self, actionLabels, icons=None, parent=None):
        super().__init__(parent)
        if isinstance(actionLabels, list):
            if icons is None:
                icons = [None for _ in actionLabels]
            if isinstance(icons, list) and len(actionLabels) == len(icons):
                self.actions = {}
                for label, icon in zip(actionLabels, icons):
                    # None presents a separator
                    if label is None:
                        self.addSeparator()
                    else:
                        action = QAction(QIcon(icon), label, self) if icon else QAction(label, self)
                        self.addAction(action)
                        self.actions[label] = action
                self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
                self.setAttribute(Qt.WA_TranslucentBackground)
            else:
                raise TypeError('icons must be a list and equal in length to actionLabels')
        else:
            raise TypeError('actionLabels must be a list')

    def setActionHandler(self, actionName, handler, *args, **kwargs):
        """
        Set handler for each action.
        :rtype: bool.
        """
        action = self.actions.get(actionName)
        if isinstance(action, QAction) and callable(handler):
            action.triggered.connect(lambda: handler(*args, **kwargs))
            return True
        return False
