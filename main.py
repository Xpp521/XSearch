from sys import modules
from TrayIcon import TrayIcon
from PyHotKey import manager, Key
from NoSleepWorkers import Worker
from PyQt5.QtCore import QSettings
from SearchDialog import SearchDialog
from SettingDialog import SettingDialog


class XSearch:
    def __init__(self):
        self.__setting = QSettings()
        self.__setting_changed = False
        search_dialog = SearchDialog()
        setting_dialog = SettingDialog()
        setting_dialog.setting_changed.connect(self.__change_settings)
        tray_icon = TrayIcon()
        if not all((tray_icon.set_action_handler('search', self.__show_search_dialog),
                    tray_icon.set_action_handler('setting', self.__show_setting_dialog))):
            raise ConnectionError("Tray icon's handler connection failed.")
        self.__widgets = {'tray_icon': tray_icon, 'search': search_dialog, 'setting': setting_dialog}
        self.__hotkey_manager = manager
        # self.__hotkey_manager.logger = True
        self.__hot_key_id = -1
        self.__change_hot_key([Key.caps_lock])
        self.__worker = Worker()
        self.__worker.start()
        if not self.__setting.value('NoSleepStatus', 0):
            self.__worker.suspend()
        tray_icon.show()

    def __change_settings(self, changed_map):
        self.__setting_changed = True
        if changed_map.get('hotkey'):
            # hotkey = self.__setting.value('Hotkey')
            # self.__change_hot_key(hotkey)
            pass
        if changed_map.get('language'):
            modules.pop('Strings')
            self.__exec_on_widgets('retranslate_ui')
        if changed_map.get('appearance'):
            # change appearance
            pass
        if changed_map.get('sleep_status'):
            if self.__worker.isWorking:
                self.__worker.suspend()
            else:
                self.__worker.resume()

    def __show_search_dialog(self):
        if not any((self.__widgets.get('search').isVisible(), self.__widgets.get('setting').isVisible())):
            self.__widgets.get('search').popup(self.__setting_changed)
            self.__setting_changed = False

    def __show_setting_dialog(self):
        if not self.__widgets.get('setting').isVisible():
            self.__widgets.get('setting').popup()

    def __change_hot_key(self, keys, count=2, interval=0.5):
        self.__hotkey_manager.UnregisterHotKey(self.__hot_key_id)
        key_id = self.__hotkey_manager.RegisterHotKey(self.__widgets.get('tray_icon').actions.get('search').trigger,
                                                      keys, count, interval)
        if -1 == key_id:
            return False
        self.__hot_key_id = key_id
        return True

    def __show_message(self, msg):
        from Strings import Strings
        if isinstance(msg, str):
            self.__widgets.get('tray_icon').showMessage(Strings.APP_NAME, msg)

    def __exec_on_widgets(self, func_name):
        for dialog in self.__widgets.values():
            func = getattr(dialog, func_name, None)
            if callable(func):
                func()
