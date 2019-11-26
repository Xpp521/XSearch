# -*- coding: utf-8 -*-
# @Time    : 2019/11/26 13:09
# @Author  : Xpp
# @Email   : Xpp233@foxmail.com
from sys import platform
from webbrowser import open
from re import search, split
from urllib.parse import quote
from PyQt5.QtCore import Qt, QSettings
from .SearchDialog_ui import Ui_Dialog
from PyQt5.QtCore import QStringListModel
from .SuggestionGetter import SuggestionGetter
from PyQt5.QtWidgets import QDialog, QCompleter, QItemDelegate


class CompleterItemDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, QPainter, QStyleOptionViewItem, QModelIndex):
        super().paint(QPainter, QStyleOptionViewItem, QModelIndex)

    def sizeHint(self, QStyleOptionViewItem, QModelIndex):
        size = super().sizeHint(QStyleOptionViewItem, QModelIndex)
        # size.setHeight(max(150, size.height()))
        size.setHeight(size.height())
        return size


class SearchDialog(QDialog):
    qss = '''
    QDialog > QFrame {
    background-color: white;
    border: 1px solid #a7acaf;
    }
    QDialog QLineEdit {
    border: 1px white;
    }
    '''
    qss_suggestion = '''
    QListView {
    background-color: grey;
    padding: 1px 5px;
    }
    QListView::item {
    background-color: white;
    line-height: 50 px;
    font-size: 25px;
    }
    '''
    regex_url = r'^(?=^.{3,255}$)(http(s)?:\/\/)?(www\.)?[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,' \
                r'62})+(:\d+)*(\/\w+\.\w+)*'

    def __init__(self):
        super().__init__()
        self.__setting = QSettings()
        self._ui = Ui_Dialog()
        self._ui.setupUi(self)
        self.setStyleSheet(self.qss)
        self.setWindowOpacity(0.9)
        suggestions = QStringListModel()
        suggestion_getter = SuggestionGetter()
        completer = QCompleter()
        completer.setModel(suggestions)
        completer.setFilterMode(Qt.MatchContains)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.PopupCompletion)
        completer.setMaxVisibleItems(10)
        # completer.popup().setStyleSheet(self.qss_suggestion)
        completer.popup().setItemDelegate(CompleterItemDelegate())
        self._ui.lineEdit.setCompleter(completer)
        self._ui.lineEdit.focusOutEvent = self.hide_dialog
        self._ui.lineEdit.textEdited.connect(lambda s: suggestions.setStringList(suggestion_getter.get_suggestions(s)))
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
        pass

    def popup(self, load_setting=False):
        if load_setting:
            self.__load_settings()
        self.show()
        # if self._SetForegroundWindow:
        #     self._SetForegroundWindow(self._hwnd)
        self.raise_()
        self.activateWindow()
        self._ui.lineEdit.setFocus()

    def hide_dialog(self, *args, **kwargs):
        self._ui.lineEdit.clear()
        self.hide()

    def closeEvent(self, QCloseEvent):
        self.hide()
        QCloseEvent.ignore()

    def keyPressEvent(self, QKeyEvent):
        key = QKeyEvent.key()
        if Qt.Key_Escape == key:
            self.hide_dialog()
        elif key in (Qt.Key_Return, Qt.Key_Enter):
            text = self._ui.lineEdit.text()
            if text:
                if search(self.regex_url, text):
                    open(text)
                else:
                    open('https://www.baidu.com/s?wd={}&ie=utf-8'
                         .format('+'.join([quote(w) for w in split(r'\s+', text.strip())])))
                self.hide_dialog()
        QKeyEvent.ignore()
