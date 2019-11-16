from sys import platform
from webbrowser import open
from PyQt5.QtCore import Qt
from re import search, split
from urllib.parse import quote
from .SearchDialog_ui import Ui_Dialog
from PyQt5.QtWidgets import QDialog, QApplication


class SearchDialog(QDialog):
    regex_url = r'^(?=^.{3,255}$)(http(s)?:\/\/)?(www\.)?[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,' \
                r'62})+(:\d+)*(\/\w+\.\w+)*'

    def __init__(self):
        super().__init__()
        self._ui = Ui_Dialog()
        self._ui.setupUi(self)
        self._ui.lineEdit.focusOutEvent = self.hide_dialog
        if 'win32' == platform:
            from ctypes import windll
            from ctypes.wintypes import HWND
            from pprint import pprint
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

    def popup(self):
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
        else:
            pass
