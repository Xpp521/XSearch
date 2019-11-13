from .SettingDialog_ui import Ui_Dialog_setting
from PyQt5.QtWidgets import QDialog


class SettingWindow(QDialog):

    def __init__(self):
        super().__init__()
        self._ui = Ui_Dialog_setting()
        self._ui.setupUi(self)
        self._ui.apply.clicked.connect(self.apply)
        self._ui.ok.clicked.connect(self.ok)
        self._ui.cancel.clicked.connect(lambda: self.hide())
        self.reject = lambda: self.hide()

    def apply(self):
        pass

    def ok(self):
        self.apply()
        self.hide()

    def closeEvent(self, QCloseEvent):
        self.hide()
        QCloseEvent.ignore()
