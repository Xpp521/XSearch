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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.\
import webbrowser
from sys import platform
from enum import IntEnum
from pyperclip import copy
from re import search, split
from Resources import resource
from urllib.parse import quote
from Utils.GUI import ListModel
from PyQt5.QtGui import QIcon, QPixmap
from .SearchDialog_ui import Ui_Dialog
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtCore import Qt, QPoint, QSettings, pyqtSignal
from Utils.SuggestionGetter import KeywordGetter, TranslationGetter, CalculationGetter


class Operation(IntEnum):
    OPEN = 1
    SEARCH = 2
    COPY = 3


class SearchDialog(QDialog):
    __keyword_signal = pyqtSignal(str)
    __translation_signal = pyqtSignal(str)
    __calculation_signal = pyqtSignal(str)

    def __init__(self, work_thread=None):
        super().__init__()
        self.__regex_url = r'^(?=^.{3,255}$)(http(s)?:\/\/)?(www\.)?[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][' \
                           r'-a-zA-Z0-9]{0,62})+(:\d+)*(\/\w+\.\w+)*'
        self.__text = ''
        self.__last_text = ''
        self.__max_list_height = 0
        self.__dialog_list_distance = 0
        self.__setting = QSettings()
        self.__ui = Ui_Dialog()
        self.__ui.setupUi(self)
        self.reload_ui()
        self.__engines = []
        self.__keywords = []
        self.__engine_icons = []
        self.__cur_engine = ''
        self.__keyword_getter = KeywordGetter(thread=work_thread)
        self.__keyword_getter.signal.connect(lambda li: self.__show_suggestions(li, Operation.SEARCH))
        self.__keyword_signal.connect(self.__keyword_getter.get)
        self.__translation_getter = TranslationGetter(thread=work_thread)
        self.__translation_getter.signal.connect(lambda li: self.__show_suggestions(li, Operation.COPY))
        self.__translation_signal.connect(self.__translation_getter.get)
        self.__calculation_getter = CalculationGetter(thread=work_thread)
        self.__calculation_getter.signal.connect(lambda li: self.__show_suggestions(li, Operation.COPY))
        self.__calculation_signal.connect(self.__calculation_getter.get)
        self.__cur_plugin = self.__keyword_getter
        self.__model = ListModel(11)
        self.__ui.listView.setModel(self.__model)
        self.__load_settings()
        self.__ui.lineEdit.focusOutEvent = self.__hide_dialog
        self.__ui.lineEdit.textEdited.connect(self.__on_text_edited)
        if 'win' == platform[:3]:
            from ctypes import windll
            from ctypes.wintypes import HWND
            self.__hwnd = HWND(int(self.winId()))
            user32 = windll.user32
            self.__window_id = windll.kernel32.GetCurrentThreadId()
            self.__GetForegroundWindow = user32.GetForegroundWindow
            self.__SetForegroundWindow = user32.SetForegroundWindow
            self.__GetWindowThreadProcessId = user32.GetWindowThreadProcessId
            self.__AttachThreadInput = user32.AttachThreadInput
            # self.__SwitchToThisWindow = user32.SwitchToThisWindow
            # self.__SetFocus = user32.SetFocus

    def __load_settings(self):
        for i in range(int(self.__setting.value('SearchEngine/count'))):
            engine_data = self.__setting.value('SearchEngine/engines/{}'.format(i)).split('||')
            self.__engines.append(engine_data[2])
            self.__keywords.append(engine_data[0])
            self.__engine_icons.append(engine_data[1])
        self.__default_engine_index = int(self.__setting.value('SearchEngine/default_engine_index'))
        self.__keyword_getter_state = int(self.__setting.value('KeywordGetter/state'))
        self.__keyword_getter.provider = int(self.__setting.value('KeywordGetter/provider/data'))
        self.__translation_getter_state = int(self.__setting.value('TranslationGetter/state'))
        self.__translation_getter_keyword = self.__setting.value('TranslationGetter/keyword')
        self.__translation_getter.provider = self.__setting.value('TranslationGetter/provider/data')
        self.__translation_getter.source = self.__setting.value('TranslationGetter/source')
        self.__translation_getter.target = self.__setting.value('TranslationGetter/target')
        self.__calculation_getter_state = int(self.__setting.value('CalculationGetter/state'))
        self.__calculation_getter_keyword = self.__setting.value('CalculationGetter/keyword')
        opacity = float(self.__setting.value('Ui/opacity'))
        self.setWindowOpacity(opacity)
        self.__ui.widget.setWindowOpacity(opacity)
        self.__dialog_list_distance = int(self.__setting.value('Ui/distance'))
        browser_path = self.__setting.value('BrowserPath')
        if browser_path:
            webbrowser.register('CustomBrowser', None, webbrowser.BackgroundBrowser(browser_path))
            try:
                self.__browser = webbrowser.get('CustomBrowser')
            except webbrowser.Error:
                self.__browser = webbrowser.get()
        else:
            self.__browser = webbrowser.get()
        if getattr(self.__browser, 'basename', None) and int(self.__setting.value('PrivateMode')):
            browser_name = self.__browser.basename.lower()
            if 'chrom' in browser_name:
                self.__browser.args.append('--incognito')
            elif 'firefox' in browser_name:
                self.__browser.args.append('-private')
            elif 'safari' in browser_path:
                self.__browser.args.append('')

    def __change_icon(self, filename):
        self.__ui.label.setPixmap(QPixmap(filename).scaled(20, 20))

    def __change_search_engine(self, index):
        self.__change_icon(self.__engine_icons[index])
        self.__cur_engine = self.__engines[index]

    def __on_text_edited_keyword_handler(self, text):
        # match engine keywords
        for i, kw in enumerate(self.__keywords):
            if text == kw:
                self.__change_search_engine(i)
                self.__ui.widget.hide()
                self.__ui.lineEdit.clear()
                self.__clear_selection()
                return
        self.__text = text
        stripped_text = text.strip()
        # check whether the text is the same as last time
        if self.__last_text == stripped_text:
            if self.__model.dataCount() and not self.__ui.widget.isVisible():
                self.__ui.widget.show()
                return
        # check whether the text is a url
        if '.' in stripped_text and ' ' not in stripped_text and search(self.__regex_url, stripped_text):
            self.__model.clearRows()
            self.__model.setRow(0, stripped_text,
                                QPixmap(resource.image.get('web.png')).scaled(25, 25), Operation.OPEN)
            self.__clear_selection()
            self.__ui.listView.setFixedHeight(50)
            self.__ui.widget.setFixedHeight(50)
            if not self.__ui.widget.isVisible():
                self.__ui.widget.show()
        else:
            if Operation.OPEN == self.__model.customData(0):
                self.__model.clearRows()
                self.__clear_selection()
        # query keyword suggestions
        if self.__keyword_getter_state:
            self.__keyword_signal.emit(stripped_text)
            self.__last_text = stripped_text

    def __on_text_edited_handler(self, text, signal):
        self.__text = text
        stripped_text = text.strip()
        if self.__last_text == stripped_text:
            if self.__model.dataCount() and not self.__ui.widget.isVisible():
                self.__ui.widget.show()
                return
        signal.emit(stripped_text)
        self.__last_text = stripped_text

    def __on_text_edited(self, text):
        # match plugin keywords
        if self.__cur_plugin == self.__translation_getter:
            self.__on_text_edited_handler(text, self.__translation_signal)
        elif self.__cur_plugin == self.__calculation_getter:
            self.__on_text_edited_handler(text, self.__calculation_signal)
        else:
            if self.__translation_getter_keyword == text and self.__translation_getter_state:
                self.__change_icon(resource.image.get('translation.png'))
                self.__clear_selection()
                self.__model.clearRows()
                self.__ui.widget.hide()
                self.__ui.lineEdit.clear()
                self.__cur_plugin = self.__translation_getter
            elif self.__calculation_getter_keyword == text and self.__calculation_getter_state:
                self.__clear_selection()
                self.__model.clearRows()
                self.__ui.widget.hide()
                self.__ui.lineEdit.clear()
                self.__change_icon(resource.image.get('calculation.png'))
                self.__cur_plugin = self.__calculation_getter
            else:
                self.__on_text_edited_keyword_handler(text)

    def __show_suggestions(self, suggestions, operation):
        if not self.isVisible():
            return
        if Operation.SEARCH == operation:
            if self.__cur_plugin != self.__keyword_getter:
                return
            if suggestions:
                if Operation.OPEN == self.__model.customData(0):
                    self.__model.setRows(1, suggestions, QPixmap(resource.image.get('search_grey.png')).scaled(25, 25),
                                         Operation.SEARCH)
                else:
                    self.__model.clearRows()
                    self.__model.setRows(0, suggestions, QPixmap(resource.image.get('search_grey.png')).scaled(25, 25),
                                         Operation.SEARCH)
                self.__clear_selection()
                self.__ui.listView.setFixedHeight(min(35 * self.__model.dataCount() + 15, self.__max_list_height))
                self.__ui.widget.setFixedHeight(min(35 * self.__model.dataCount() + 15, self.__max_list_height))
                if not self.__ui.widget.isVisible():
                    self.__ui.widget.show()
            else:
                if Operation.OPEN != self.__model.customData(0):
                    self.__model.clearRows()
                    self.__clear_selection()
                    if self.__ui.widget.isVisible():
                        self.__ui.widget.hide()
        elif Operation.COPY == operation:
            if suggestions:
                self.__model.setRows(0, suggestions, QPixmap(resource.image.get('copy.png')).scaled(25, 25), operation)
                self.__clear_selection()
                self.__ui.listView.setFixedHeight(min(35 * self.__model.dataCount() + 15, self.__max_list_height))
                self.__ui.widget.setFixedHeight(min(35 * self.__model.dataCount() + 15, self.__max_list_height))
                if not self.__ui.widget.isVisible():
                    self.__ui.widget.show()
            else:
                self.__model.clearRows()
                self.__clear_selection()
                if self.__ui.widget.isVisible():
                    self.__ui.widget.hide()

    def popup(self, load_setting=False):
        if load_setting:
            self.__load_settings()
        self.__change_search_engine(self.__default_engine_index)
        if 'win' == platform[:3]:
            top_window_id = self.__GetWindowThreadProcessId(self.__GetForegroundWindow(), None)
            self.__AttachThreadInput(top_window_id, self.__window_id, True)
            self.show()
            self.__SetForegroundWindow(self.__hwnd)
            self.__AttachThreadInput(top_window_id, self.__window_id, False)
        else:
            self.show()
            self.raise_()
            self.activateWindow()
        p = self.mapToGlobal(QPoint(0, self.height()))
        y = p.y()
        self.__max_list_height = QApplication.desktop().screenGeometry().height() - 1 - y - self.__dialog_list_distance
        self.__ui.widget.move(p.x(), y + self.__dialog_list_distance)
        self.__ui.lineEdit.clear()
        self.__cur_plugin = self.__keyword_getter

    def __hide_dialog(self, *args, **kwargs):
        self.__ui.lineEdit.clear()
        # self.__model.clearData()
        # self.clearSelection()
        if self.__ui.widget.isVisible():
            self.__ui.widget.hide()
        self.hide()

    # def showEvent(self, event):
    #     self.setAttribute(Qt.WA_Mapped)
    #     super().showEvent(event)

    def closeEvent(self, event):
        self.__hide_dialog()
        event.ignore()

    def keyPressEvent(self, event):
        key = event.key()
        if Qt.Key_Escape == key:
            if self.__ui.widget.isVisible():
                self.__clear_selection()
                self.__ui.widget.hide()
            else:
                self.__hide_dialog()
        elif Qt.Key_Tab == key:
            current_index = self.__ui.listView.currentIndex()
            if self.__ui.listView.rootIndex() == current_index:
                return
            row = current_index.row()
            operation = self.__model.customData(row)
            text = self.__model.text(row)
            if Operation.OPEN == operation:
                self.__browser.open(text if text.startswith('http') else 'http://{}'.format(text))
                self.__hide_dialog()
            elif Operation.SEARCH == operation:
                self.__ui.lineEdit.setText(text)
                self.__on_text_edited(text)
            elif Operation.COPY == operation:
                copy(text)
                self.__hide_dialog()
        elif key in (Qt.Key_Up, Qt.Key_Down):
            if self.__ui.widget.isVisible():
                count = self.__model.dataCount()
                current_index = self.__ui.listView.currentIndex()
                if Qt.Key_Up == key:
                    if self.__ui.listView.rootIndex() == current_index:
                        index = self.__model.index(count - 1)
                        self.__ui.listView.setCurrentIndex(index)
                        self.__ui.lineEdit.setText(self.__model.text(count - 1))
                        return
                    row = current_index.row() - 1
                    if 0 > row:
                        self.__clear_selection()
                        if self.__cur_plugin == self.__keyword_getter:
                            self.__ui.lineEdit.setText(self.__text)
                            self.__ui.listView.setCurrentIndex(self.__ui.listView.rootIndex())
                        else:
                            self.__ui.listView.setCurrentIndex(self.__model.index(count - 1))
                        return
                else:
                    row = current_index.row() + 1
                    if count <= row:
                        self.__clear_selection()
                        if self.__cur_plugin == self.__keyword_getter:
                            self.__ui.lineEdit.setText(self.__text)
                            self.__ui.listView.setCurrentIndex(self.__model.index(-1))
                        else:
                            self.__ui.listView.setCurrentIndex(self.__model.index(0))
                        return
                index = self.__model.index(row)
                self.__ui.listView.setCurrentIndex(index)
                if self.__cur_plugin == self.__keyword_getter:
                    self.__ui.lineEdit.setText(self.__model.text(row))
        elif key in (Qt.Key_Return, Qt.Key_Enter):
            row = self.__ui.listView.currentIndex().row()
            operation = self.__model.customData(row)
            text = self.__ui.lineEdit.text().strip()
            if Operation.OPEN == operation:
                self.__browser.open(text if text.startswith('http') else 'http://{}'.format(text))
            elif Operation.SEARCH == operation:
                self.__browser.open(self.__cur_engine.replace('%s', '+'.join([quote(w) for w in split(r'\s+', text)])))
            elif Operation.COPY == operation:
                copy(self.__model.text(row))
            self.__hide_dialog()
        event.ignore()

    def reload_ui(self, text=True, qss=True):
        if text:
            self.__ui.retranslateUi(self)
        if qss:
            self.setWindowIcon(QIcon(resource.image.get('app.ico')))
            font_color = self.__setting.value('Ui/font_color')
            border_color = self.__setting.value('Ui/border_color')
            border_radius = self.__setting.value('Ui/border_radius')
            selected_color = self.__setting.value('Ui/selected_color')
            background_color = self.__setting.value('Ui/background_color')
            self.__ui.lineEdit.setStyleSheet('''QLineEdit {{
            font: bold 20px;
            color: {};
            border-radius: {}px;
            border: 1px solid {};
            background-color: {};
            padding:0 11px 0 35px;
            }}'''.format(font_color, border_radius, border_color, background_color))
            self.__ui.listView.setStyleSheet('''QListView {{
            font: 18px;
            color: {};
            padding: 5px;
            border-radius: {}px;
            border: 1px solid {};
            background-color: {};
            }}
            QListView::item {{
            height: 35px;
            border-radius: {}px;
            background-color: transparent;
            }}
            QListView::item:selected {{
            background-color: {}
            }}'''.format(font_color, border_radius, border_color,
                         background_color, border_radius, selected_color))

    def __clear_selection(self):
        self.__ui.listView.clearSelection()
        self.__ui.listView.setCurrentIndex(self.__ui.listView.rootIndex())

    @property
    def keyword_getter(self):
        return self.__keyword_getter

    @property
    def work_thread(self):
        return self.__keyword_getter.thread
