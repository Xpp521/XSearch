from sys import modules
from TrayIcon import TrayIcon
from PyHotKey import manager, Key
from SearchDialog import SearchDialog
from SettingDialog import SettingDialog


class XSearch:
    def __init__(self):
        self.__setting_changed = False
        self.__search_dialog = SearchDialog()
        self.__setting_dialog = SettingDialog()
        self.__setting_dialog.setting_changed.connect(self.__change_settings)
        self.__tray_icon = TrayIcon()
        self.__tray_icon.action_show.triggered.connect(self.__show_search_dialog)
        self.__tray_icon.action_setting.triggered.connect(self.__show_setting_dialog)
        self.__tray_icon.show()
        self.__manager = manager
        self.__hot_key_id = -1
        self.__change_hot_key([Key.caps_lock])

    def __change_settings(self, flag):
        self.__setting_changed = flag
        if flag:
            pass

    def __show_search_dialog(self):
        self.__search_dialog.popup(self.__setting_changed)

    def __show_setting_dialog(self):
        self.__setting_dialog.popup()

    def __change_hot_key(self, keys, count=2, interval=0.5):
        self.__manager.UnregisterHotKey(self.__hot_key_id)
        key_id = self.__manager.RegisterHotKey(self.__tray_icon.action_show.trigger, keys, count, interval)
        if -1 == key_id:
            return False
        self.__hot_key_id = key_id
        return True

    def __show_message(self, msg):
        from Strings import Strings
        if msg and isinstance(msg, str):
            self.__tray_icon.showMessage(Strings.APP_NAME, msg)

    def retranslate_ui(self):
        pass
