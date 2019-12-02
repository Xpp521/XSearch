# -*- coding: utf-8 -*-
# @Time    : 2019/11/26 13:09
# @Author  : Xpp
# @Email   : Xpp233@foxmail.com
import webbrowser
from sys import platform
from os.path import join
from re import search, split
from urllib.parse import quote
from PyQt5.QtGui import QPixmap
from .SearchDialog_ui import Ui_Dialog
from PyQt5.QtWidgets import QDialog, QApplication
from .SuggestionGetter import keyword_suggestion_getter
from PyQt5.QtCore import Qt, QPoint, QSettings, QStringListModel


class SearchDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.__regex_url = r'^(?=^.{3,255}$)(http(s)?:\/\/)?(www\.)?[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][' \
                           r'-a-zA-Z0-9]{0,62})+(:\d+)*(\/\w+\.\w+)*'
        self.__text = ''
        self.__last_text = ''
        self.__first_popup = True
        self.__max_list_height = 0
        self.__setting = QSettings()
        self._ui = Ui_Dialog()
        self._ui.setupUi(self)
        self.__suggestion_getter = keyword_suggestion_getter
        self.__suggestion_getter.signal.connect(self.__show_suggestions)
        self.__suggestion_model = QStringListModel()
        self.__load_settings()
        self._ui.lineEdit.focusOutEvent = self.__hide_dialog
        self._ui.lineEdit.textEdited.connect(self.__on_text_edited)
        if 'win32' == platform:
            from ctypes import windll
            from ctypes.wintypes import HWND
            # print(dir(windll.kernel32))
            # print(dir(windll.user32))
            # self.hwnd = QApplication.instance()
            self._AllowSetForegroundWindow = windll.user32.AllowSetForegroundWindow
            # t = windll.user32.ASFW_ANY
            # self._AllowSetForegroundWindow()
            self._SetForegroundWindow = windll.user32.SetForegroundWindow
            # self._FindWindow = windll.user32.FindWindow
            self._hwnd = HWND(int(self.winId()))
            # print(type(self._hwnd))
            # print(self._hwnd)
        else:
            self._SetForegroundWindow = None

    def __load_settings(self):
        self.setStyleSheet(self.__setting.value('SearchDialogQss',
                                                '''QDialog QLineEdit {
                                                border: 1px solid #a7acaf;
                                                padding:0 11px 0 35px;
                                                font: bold 20px;
                                                }
                                                QDialog QListView {
                                                border: 1px solid #a7acaf;
                                                background-color: white;
                                                padding: 5px;
                                                font: 18px;
                                                }
                                                QDialog QListView::item {height: 35px;}
                                                QDialog QListView::item:selected {background-color: #E5F3FF;}'''))
        opacity = self.__setting.value('SearchDialogOpacity', 0.9)
        self.setWindowOpacity(opacity)
        self._ui.listView.setWindowOpacity(opacity)
        self.__dialog_list_distance = self.__setting.value('DialogListDistance', 3)
        self.__search_engine = self.__setting.value('SearchEngine', 'https://www.baidu.com/s?wd={}&ie=utf-8')
        self._ui.label.setPixmap(QPixmap(self.__setting.value('SearchEngineIcon',
                                                              join('Icons', 'baidu.png'))).scaled(20, 20))
        self.__suggestion_getter.api = self.__setting.value('SuggestEngine', 'https://sug.so.360.cn/suggest/word?')
        browser_path = self.__setting.value('BrowserPath')
        if browser_path:
            webbrowser.register('CustomBrowser', None, webbrowser.BackgroundBrowser(browser_path))
            try:
                self.__browser = webbrowser.get('CustomBrowser')
            except webbrowser.Error:
                self.__browser = webbrowser.get()
        else:
            self.__browser = webbrowser.get()

    def __on_text_edited(self, text):
        self.__text = text
        text = text.strip()
        if not text:
            self._ui.listView.hide()
            return
        if self.__last_text == text:
            if self.__suggestion_model.stringList() and not self._ui.listView.isVisible():
                self._ui.listView.show()
        else:
            self.__suggestion_getter.get(text)
            self.__last_text = text

    def __show_suggestions(self, suggestions):
        if self.__suggestion_model.stringList() == suggestions:
            return
        self.__suggestion_model.setStringList(suggestions)
        self._ui.listView.setModel(self.__suggestion_model)
        if suggestions:
            self._ui.listView.setFixedHeight(min(35 * len(suggestions) + 15, self.__max_list_height))
            if not self._ui.listView.isVisible():
                self._ui.listView.show()
        else:
            self._ui.listView.hide()
            if self._ui.listView.isVisible():
                self._ui.listView.hide()

    def popup(self, load_setting=False):
        if load_setting:
            self.__load_settings()
        self.show()
        if self._SetForegroundWindow:
            self._SetForegroundWindow(self._hwnd)
        self.raise_()
        self.activateWindow()
        self._ui.lineEdit.setFocus()
        if self.__first_popup:
            p = self.mapToGlobal(QPoint(0, self.height()))
            self._ui.listView.move(p.x(), p.y() + self.__dialog_list_distance)
            self.__first_popup = False
            self.__max_list_height = QApplication.desktop().screenGeometry().height() - 1 - self.mapToGlobal(QPoint(0, self.height())).y() - self.__dialog_list_distance

    def __hide_dialog(self, *args, **kwargs):
        if self._ui.listView.isVisible():
            self._ui.listView.hide()
        self._ui.lineEdit.clear()
        self.hide()

    def closeEvent(self, event):
        self.hide()
        event.ignore()

    def keyPressEvent(self, event):
        key = event.key()
        if Qt.Key_Escape == key:
            if self._ui.listView.isVisible():
                self._ui.listView.hide()
            else:
                self.__hide_dialog()
        elif key in (Qt.Key_Up, Qt.Key_Down):
            if self._ui.listView.isVisible():
                count = self.__suggestion_model.rowCount()
                current_index = self._ui.listView.currentIndex()
                if Qt.Key_Up == key:
                    if self._ui.listView.rootIndex() == current_index:
                        index = self.__suggestion_model.index(count - 1)
                        self._ui.listView.setCurrentIndex(index)
                        self._ui.lineEdit.setText(self.__suggestion_model.data(index, Qt.DisplayRole))
                        return
                    row = current_index.row() - 1
                    if 0 > row:
                        self._ui.listView.clearSelection()
                        self._ui.lineEdit.setText(self.__text)
                        self._ui.listView.setCurrentIndex(self._ui.listView.rootIndex())
                        return
                else:
                    row = current_index.row() + 1
                    if count <= row:
                        self._ui.listView.clearSelection()
                        self._ui.lineEdit.setText(self.__text)
                        self._ui.listView.setCurrentIndex(self.__suggestion_model.index(-1))
                        return
                index = self.__suggestion_model.index(row)
                self._ui.listView.setCurrentIndex(index)
                self._ui.lineEdit.setText(self.__suggestion_model.data(index, Qt.DisplayRole))
        elif key in (Qt.Key_Return, Qt.Key_Enter):
            text = self._ui.lineEdit.text()
            if text:
                if search(self.__regex_url, text):
                    self.__browser.open(text if text.startswith('http') else 'http://{}'.format(text))
                else:
                    self.__browser.open(self.__search_engine.format(
                        '+'.join([quote(w) for w in split(r'\s+', text.strip())])))
                self.__hide_dialog()
        event.ignore()

    def retranslate_ui(self):
        self._ui.retranslateUi(self)
