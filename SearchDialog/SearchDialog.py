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
from PyQt5.QtCore import Qt, QPoint, QSettings, pyqtSignal, QStringListModel


class SearchDialog(QDialog):
    __get_suggestions = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.__regex_url = r'^(?=^.{3,255}$)(http(s)?:\/\/)?(www\.)?[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][' \
                           r'-a-zA-Z0-9]{0,62})+(:\d+)*(\/\w+\.\w+)*'
        self.__text = ''
        self.__last_text = ''
        self.__first_popup = True
        self.__max_list_height = 0
        self.__setting = QSettings()
        self.__ui = Ui_Dialog()
        self.__ui.setupUi(self)
        self.__suggestion_getter = keyword_suggestion_getter
        self.__suggestion_getter.signal.connect(self.__show_suggestions)
        self.__get_suggestions.connect(self.__suggestion_getter.get)
        self.__suggestion_model = QStringListModel()
        self.__load_settings()
        self.__ui.lineEdit.textEdited.connect(self.__on_text_edited)
        self.__ui.lineEdit.focusOutEvent = self.__hide_dialog
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
        self.__suggestion_status = self.__setting.value('SuggestionStatus', True)
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
        # #5858fc
        opacity = float(self.__setting.value('Opacity/data', 0.9))
        self.setWindowOpacity(opacity)
        self.__ui.listView.setWindowOpacity(opacity)
        self.__dialog_list_distance = self.__setting.value('DialogListDistance', 3)
        self.__search_engine = self.__setting.value('SearchEngine/data', 'https://www.baidu.com/s?wd={}&ie=utf-8')
        self.__ui.label.setPixmap(QPixmap(self.__setting.value('SearchEngineIcon',
                                                               join('Icons', 'baidu.png'))).scaled(20, 20))
        self.__suggestion_getter.api = self.__setting.value('SuggestEngine/data', 'https://sug.so.360.cn/suggest/word?')
        browser_path = self.__setting.value('BrowserPath')
        if browser_path:
            webbrowser.register('CustomBrowser', None, webbrowser.BackgroundBrowser(browser_path))
            try:
                self.__browser = webbrowser.get('CustomBrowser')
            except webbrowser.Error:
                self.__browser = webbrowser.get()
        else:
            self.__browser = webbrowser.get()
        if getattr(self.__browser, 'basename', None) and self.__setting.value('PrivateMode', True):
            browser_name = self.__browser.basename.lower()
            if 'chrom' in browser_name:
                self.__browser.args.append('--incognito')
            elif 'firefox' in browser_name:
                self.__browser.args.append('-private')
            elif 'safari' in browser_path:
                self.__browser.args.append('')

    def __on_text_edited(self, text):
        if self.__suggestion_status:
            self.__text = text
            text = text.strip()
            if not text:
                self.__ui.listView.hide()
                return
            if self.__last_text == text:
                if self.__suggestion_model.rowCount() and not self.__ui.listView.isVisible():
                    self.__ui.listView.show()
            else:
                self.__get_suggestions.emit(text)
                self.__last_text = text

    def __show_suggestions(self, suggestions):
        if self.__suggestion_model.stringList() == suggestions:
            return
        self.__suggestion_model.setStringList(suggestions)
        self.__ui.listView.setModel(self.__suggestion_model)
        if suggestions:
            self.__ui.listView.setFixedHeight(min(35 * len(suggestions) + 15, self.__max_list_height))
            if not self.__ui.listView.isVisible():
                self.__ui.listView.show()
        else:
            self.__ui.listView.hide()
            if self.__ui.listView.isVisible():
                self.__ui.listView.hide()

    def popup(self, load_setting=False):
        if load_setting:
            self.__load_settings()
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
        # self._ui.lineEdit.setFocus()
        if self.__first_popup:
            p = self.mapToGlobal(QPoint(0, self.height()))
            self.__ui.listView.move(p.x(), p.y() + self.__dialog_list_distance)
            self.__first_popup = False
            self.__max_list_height = QApplication.desktop().screenGeometry().height() - 1 - self.mapToGlobal(QPoint(0, self.height())).y() - self.__dialog_list_distance

    def __hide_dialog(self, *args, **kwargs):
        if self.__ui.listView.isVisible():
            self.__ui.listView.hide()
        self.__ui.lineEdit.clear()
        self.hide()

    def closeEvent(self, event):
        self.__hide_dialog()
        event.ignore()

    def keyPressEvent(self, event):
        key = event.key()
        if Qt.Key_Escape == key:
            if self.__ui.listView.isVisible():
                self.__ui.listView.hide()
            else:
                self.__hide_dialog()
        elif Qt.Key_Tab == key:
            if self.__suggestion_status:
                current_index = self.__ui.listView.currentIndex()
                if self.__ui.listView.rootIndex() == current_index:
                    return
                text = self.__suggestion_model.data(current_index, Qt.DisplayRole)
                self.__ui.lineEdit.setText(text)
                self.__text = text
                self.__last_text = text
                self.__get_suggestions.emit(text)
        elif key in (Qt.Key_Up, Qt.Key_Down):
            if self.__suggestion_status:
                if self.__ui.listView.isVisible():
                    count = self.__suggestion_model.rowCount()
                    current_index = self.__ui.listView.currentIndex()
                    if Qt.Key_Up == key:
                        if self.__ui.listView.rootIndex() == current_index:
                            index = self.__suggestion_model.index(count - 1)
                            self.__ui.listView.setCurrentIndex(index)
                            self.__ui.lineEdit.setText(self.__suggestion_model.data(index, Qt.DisplayRole))
                            return
                        row = current_index.row() - 1
                        if 0 > row:
                            self.__ui.listView.clearSelection()
                            self.__ui.lineEdit.setText(self.__text)
                            self.__ui.listView.setCurrentIndex(self.__ui.listView.rootIndex())
                            return
                    else:
                        row = current_index.row() + 1
                        if count <= row:
                            self.__ui.listView.clearSelection()
                            self.__ui.lineEdit.setText(self.__text)
                            self.__ui.listView.setCurrentIndex(self.__suggestion_model.index(-1))
                            return
                    index = self.__suggestion_model.index(row)
                    self.__ui.listView.setCurrentIndex(index)
                    self.__ui.lineEdit.setText(self.__suggestion_model.data(index, Qt.DisplayRole))
        elif key in (Qt.Key_Return, Qt.Key_Enter):
            text = self.__ui.lineEdit.text()
            if text:
                if search(self.__regex_url, text):
                    self.__browser.open(text if text.startswith('http') else 'http://{}'.format(text))
                else:
                    self.__browser.open(self.__search_engine.format(
                        '+'.join([quote(w) for w in split(r'\s+', text.strip())])))
                self.__hide_dialog()
        event.ignore()

    def retranslate_ui(self):
        self.__ui.retranslateUi(self)
