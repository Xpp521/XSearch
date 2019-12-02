from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog
from .SettingDialog_ui import Ui_Dialog_setting


class SettingDialog(QDialog):
    setting_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self._ui = Ui_Dialog_setting()
        self._ui.setupUi(self)
        self._ui.ok.clicked.connect(self.__ok)
        self._ui.apply.clicked.connect(self.__apply)
        self._ui.cancel.clicked.connect(self.__cancel)

    def __load_settings(self):
        pass

    def popup(self):
        self.show()

    def __apply(self):
        # save settings
        self.setting_changed.emit(True)

    def __ok(self):
        self.__apply()
        self.hide()

    def __cancel(self):
        self.setting_changed.emit(False)
        self.hide()

    def closeEvent(self, QCloseEvent):
        self.__cancel()
        QCloseEvent.ignore()
