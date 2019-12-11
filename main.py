from sys import modules
from TrayIcon import TrayIcon
from NoSleepWorker import Worker
from PyHotKey import manager, Key
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
        self.__hot_key_id = -1
        self.__update_hot_key()
        self.__worker = Worker()
        self.__worker.start()
        if not self.__setting.value('NoSleepStatus', 0):
            self.__worker.suspend()
        tray_icon.show()

    def __change_settings(self, changed_map):
        self.__setting_changed = True
        if changed_map.get('hotkey'):
            self.__update_hot_key()
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

    def __update_hot_key(self):
        keys = []
        for key_text in self.__setting.value('Hotkey/keys', 'caps_lock').split('+'):
            enum = getattr(Key, key_text, None)
            keys.append(enum if enum else key_text[0])
        key_id = self.__hotkey_manager.RegisterHotKey(self.__widgets.get('tray_icon').actions.get('search').trigger,
                                                      keys, self.__setting.value('Hotkey/press_time/data', 2),
                                                      float(self.__setting.value('Hotkey/interval/data', 0.5)))
        if -1 == key_id:
            return False
        if -1 == self.__hot_key_id or self.__hotkey_manager.UnregisterHotKey(self.__hot_key_id):
            self.__hot_key_id = key_id
            return True
        else:
            self.__hotkey_manager.UnregisterHotKey(key_id)
            return False

    def __show_message(self, msg):
        from Strings import Strings
        if isinstance(msg, str):
            self.__widgets.get('tray_icon').showMessage(Strings.APP_NAME, msg)

    def __exec_on_widgets(self, func_name):
        for dialog in self.__widgets.values():
            func = getattr(dialog, func_name, None)
            if callable(func):
                func()
