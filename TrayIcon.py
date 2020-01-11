# -*- coding: utf-8 -*-
#
# Copyright 2020 Xpp521
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
from os.path import join
from PyQt5.QtCore import Qt
from PyQt5.Qt import QCursor
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QApplication, QAction, QMenu, QSystemTrayIcon


class TrayIcon(QSystemTrayIcon):
    def __init__(self):
        super().__init__()
        menu = QMenu()
        menu.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        menu.setAttribute(Qt.WA_TranslucentBackground)
        action_show = QAction(QIcon(join('Icons', 'search.png')), '', menu)
        action_setting = QAction(QIcon(join('Icons', 'setting.png')), '', menu)
        action_separator = QAction(menu)
        action_separator.setSeparator(True)
        action_exit = QAction(QIcon(join('Icons', 'exit.png')), '', menu, triggered=QApplication.instance().quit)
        self.actions = {'search': action_show, 'setting': action_setting, 'exit': action_exit}
        menu.addActions((action_show, action_setting, action_separator, action_exit))
        self.setContextMenu(menu)
        self.__cursor = QCursor()
        self.activated.connect(lambda: menu.popup(self.__cursor.pos()))
        self.reload_ui()

    def set_action_handler(self, action_name, handler):
        action = self.actions.get(action_name)
        if isinstance(action, QAction) and callable(handler):
            action.triggered.connect(handler)
            return True
        return False

    def reload_ui(self, text=True, qss=True):
        if text:
            self.setIcon(QIcon(join('Icons', 'XSearch.ico')))
            from Strings import Strings
            self.setToolTip(Strings.APP_NAME)
            self.actions.get('search').setText(Strings.TRAY_SEARCH)
            self.actions.get('setting').setText(Strings.TRAY_SETTING)
            self.actions.get('exit').setText(Strings.TRAY_EXIT)
        if qss:
            setting = QSettings()
            font_color = setting.value('Ui/font_color')
            border_color = setting.value('Ui/border_color')
            border_radius = setting.value('Ui/border_radius')
            selected_color = setting.value('Ui/selected_color')
            background_color = setting.value('Ui/background_color')
            self.contextMenu().setStyleSheet('''QMenu {{
            color: {};
            font: 17px;
            padding:3px 3px;
            border: 1px solid {};
            border-radius: {}px;
            background-color: {};
            }}
            QMenu::item {{
            margin:1px 1px;
            border-radius: {}px;
            padding:8px 20px 8px 0;
            background-color: transparent;
            }}
            QMenu::item:selected {{
            background-color: {};
            }}'''.format(font_color, border_color, border_radius, background_color, border_radius, selected_color))
