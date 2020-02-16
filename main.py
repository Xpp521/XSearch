# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Xpp521
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from TrayIcon import TrayIcon
from PyQt5.QtCore import QThread
from PyHotKey import manager, Key
from SearchDialog import SearchDialog
from SettingDialog import SettingDialog
from PyQt5.QtWidgets import QApplication


class Application(SettingDialog):
    def __init__(self):
        self.__work_thread = QThread()
        self.__work_thread.start()
        super().__init__(self.__work_thread)
        self.__setting_changed = False
        search_dialog = SearchDialog(self.__work_thread)
        tray_icon = TrayIcon()
        if not all((tray_icon.setActionHandler('search', self.__show_search_dialog),
                    tray_icon.setActionHandler('setting', self.__show_setting_dialog),
                    tray_icon.setActionHandler('exit', QApplication.instance().quit))):
            raise ConnectionError("Tray icon's handler connection failed.")
        self.__widgets = {'tray_icon': tray_icon, 'search': search_dialog}
        self.__hotkey_manager = manager
        self.__hot_key_id = -1
        self.__update_hot_key()
        tray_icon.show()
        from Languages import Strings
        self.__show_tip(Strings.TIP_WELCOME)

    def __update_hot_key(self):
        keys = []
        for key_text in self._setting.value('Hotkey/keys').split('+'):
            enum = getattr(Key, key_text, None)
            keys.append(enum if enum else key_text[0])
        key_id = self.__hotkey_manager.RegisterHotKey(self.__widgets.get('tray_icon').actions.get('search').trigger,
                                                      keys, self._setting.value('Hotkey/press_time/data', 2),
                                                      float(self._setting.value('Hotkey/interval/data', 0.5)))
        if -1 == key_id:
            return False
        if -1 == self.__hot_key_id or self.__hotkey_manager.UnregisterHotKey(self.__hot_key_id):
            self.__hot_key_id = key_id
            return True
        else:
            self.__hotkey_manager.UnregisterHotKey(key_id)
            return False

    def __show_search_dialog(self):
        if not any((self.__widgets.get('search').isVisible(), self.isVisible())):
            setting_changed = self.__setting_changed
            self.__setting_changed = False
            self.__widgets.get('search').popup(setting_changed)

    def __show_setting_dialog(self):
        if not self.isVisible():
            self.popup()

    def __show_tip(self, msg):
        if self._tip_state:
            from Languages import Strings
            if isinstance(msg, str):
                self.__widgets.get('tray_icon').showMessage(Strings.APP_NAME, msg)

    def __exec_on_widgets(self, func_name, *args, **kwargs):
        for dialog in self.__widgets.values():
            func = getattr(dialog, func_name, None)
            if callable(func):
                func(*args, **kwargs)

    def _load_settings(self):
        super()._load_settings()
        cache_count = self.__widgets.get('search').keyword_getter.cache_count
        self._ui.label_suggestion_cache_count2.setText(str(cache_count))
        self._ui.pushButton_suggestion_clear_cache.setEnabled(cache_count)

    def _change_tip_state(self, checked):
        from Languages import Strings
        super()._change_tip_state(checked)
        if checked:
            self.__show_tip(Strings.TIP_TURN_ON_TIP)

    def _clear_suggestion_cache(self):
        self.__widgets.get('search').keyword_getter.clear_cache()
        self._ui.label_suggestion_cache_count2.setText('0')
        self._ui.pushButton_suggestion_clear_cache.setEnabled(False)

    def _change_no_sleep_state(self, checked):
        super()._change_no_sleep_state(checked)
        from Languages import Strings
        if checked:
            self.__show_tip(Strings.TIP_PREVENT_SLEEP)
        else:
            self.__show_tip(Strings.TIP_ALLOW_SLEEP)

    def reload_ui(self, text=True, qss=True):
        super().reload_ui(text, qss)
        try:
            self.__exec_on_widgets('reload_ui', text, qss)
        except AttributeError:
            pass

    def _hide_dialog(self):
        super()._hide_dialog()
        self.__update_hot_key()
        self.__setting_changed = True

    @property
    def work_thread(self):
        return self.__work_thread
