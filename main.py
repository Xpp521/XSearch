from TrayIcon import TrayIcon
from pynput.keyboard import Key
from SearchDialog import SearchDialog
from SettingDialog import SettingWindow
from HotKeyManager import HotKeyManager, HotKeyType


class XSearch:
    def __init__(self):
        self.search_dialog = SearchDialog()
        self.setting_dialog = SettingWindow()
        self.tray_icon = TrayIcon()
        self.tray_icon.action_show.triggered.connect(self.show_search_dialog)
        self.tray_icon.action_setting.triggered.connect(self.show_setting_dialog)
        self.tray_icon.show_setting = self.show_setting_dialog
        self.tray_icon.show()
        self.manager = HotKeyManager(self.show_search_dialog, [Key.caps_lock], HotKeyType.SINGLE)
        self.manager.start()

    def show_message(self, msg):
        if msg and isinstance(msg, str):
            self.tray_icon.showMessage('XSearch', msg)

    def show_search_dialog(self):
        if not self.search_dialog.isVisible():
            self.search_dialog.show()
            self.search_dialog.setFocus()

    def show_setting_dialog(self):
        if not self.setting_dialog.isVisible():
            self.setting_dialog.show()
            self.manager.stop()
            self.manager.start()
