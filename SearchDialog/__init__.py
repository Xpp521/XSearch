from webbrowser import open
from re import search, split
from PyQt5.QtCore import Qt
from urllib.parse import quote
from PyQt5.QtWidgets import QDialog
from .SearchDialog_ui import Ui_Dialog


class SearchDialog(QDialog):
    regex_url = r'^(?=^.{3,255}$)(http(s)?:\/\/)?(www\.)?[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,' \
                r'62})+(:\d+)*(\/\w+\.\w+)*'

    def __init__(self):
        super().__init__()
        self._ui = Ui_Dialog()
        self._ui.setupUi(self)

    def closeEvent(self, QCloseEvent):
        self.hide()
        QCloseEvent.ignore()

    def keyPressEvent(self, QKeyEvent):
        key = QKeyEvent.key()
        if Qt.Key_Escape == key:
            self.hide()
        elif key in (Qt.Key_Return, Qt.Key_Enter):
            text = self._ui.lineEdit.text()
            if text:
                if search(self.regex_url, text):
                    open(text)
                else:
                    open('https://www.baidu.com/s?wd={}&ie=utf-8'
                         .format('+'.join([quote(w) for w in split(r'\s+', text.strip())])))
                self._ui.lineEdit.setText('')
                self.hide()
        else:
            pass
