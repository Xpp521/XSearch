# -*- coding: utf-8 -*-
#
# Copyright 2020 Xpp521
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
from os.path import join
from requests import get
from json import load, dump
from lxml.etree import HTML
from PyQt5.QtGui import QIcon
from sys import modules, platform
from pynput.keyboard import Listener
from Utils.NoSleepWorker import Worker
from .SettingDialog_ui import Ui_Dialog
from Utils.SuggestionGetter import KeywordGetter
from PyQt5.QtWidgets import QDialog, QFileDialog
from requests.exceptions import RequestException
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, QSettings


class NewVersionChecker(QObject):
    __signal = pyqtSignal(int)

    def __init__(self, thread=None):
        super().__init__()
        self.__thread = thread
        if not isinstance(thread, QThread):
            self.__thread = QThread()
            self.__thread.start()
        self.moveToThread(self.__thread)

    @staticmethod
    def __compare_version(old, new):
        """Compare old version and new version.
        Version text format example: v1.2.3
        :param old: old version text.
        :param new: new version text.
        :return: returns True if new > old, otherwise returns False.
        """
        try:
            old_version = [int(v) for v in old.strip().replace('r', '').split('.')]
            new_version = [int(v) for v in new.strip().replace('r', '').split('.')]
        except ValueError:
            return False
        if 3 != len(old_version) or 3 != len(new_version):
            return False
        if old_version[0] < new_version[0]:
            return True
        else:
            if old_version[1] < new_version[1]:
                return True
            else:
                if old_version[2] < new_version[2]:
                    return True
        return False

    def check(self, *args, **kwargs):
        from Languages import Strings
        self.__signal.emit(self.CHECKING)
        try:
            r = get(Strings.RELEASE_ADDRESS, timeout=11)
        except RequestException:
            self.__signal.emit(self.ERROR)
            return
        if 200 == r.status_code:
            if self.__compare_version(Strings.VERSION,
                                      HTML(r.text).xpath('//div[@class="release-header"]/div/div/a/text()')[0]):
                self.__signal.emit(self.NEW_VERSION)
            else:
                self.__signal.emit(self.NO_NEW_VERSION)
        else:
            self.__signal.emit(self.ERROR)

    @property
    def signal(self):
        return self.__signal

    @property
    def thread(self):
        return self.__thread

    CHECKING = 1
    NEW_VERSION = 2
    NO_NEW_VERSION = 3
    ERROR = 5


class SettingDialog(QDialog):
    __check_new_version_signal = pyqtSignal()
    default_setting = {
        'TipState': '1',
        'StartupState': '1',
        'Language': 'en',
        'SearchEngine/count': '9',
        'SearchEngine/engines/0': 'baidu||{}||https://www.baidu.com/s?ie=utf-8&wd=%s'.format(join('Icons',
                                                                                                  'baidu.png')),
        'SearchEngine/engines/1': 'google||{}||https://www.google.com/search?q=%s'.format(join('Icons', 'google.png')),
        'SearchEngine/engines/2': 'bing||{}||http://www.bing.com/search?q=%s'.format(join('Icons', 'bing.png')),
        'SearchEngine/engines/3': 'cnbing||{}||http://cn.bing.com/search?q=%s'.format(join('Icons', 'bing.png')),
        'SearchEngine/engines/4': '360||{}||https://www.so.com/s?ie=utf-8&q=%s'.format(join('Icons', '360.png')),
        'SearchEngine/engines/5': 'sogou||{}||https://www.sogou.com/web?ie=utf8&query=%s'.format(join('Icons',
                                                                                                      'sogou.png')),
        'SearchEngine/engines/6': 'toutiao||{}||https://m.toutiao.com/search/?&keyword=%s'.format(join('Icons',
                                                                                                       'toutiao.png')),
        'SearchEngine/engines/7': 'yandex||{}||https://yandex.com/search/?text=%s'.format(join('Icons', 'yandex.png')),
        'SearchEngine/engines/8': 'douban||{}||https://search.douban.com/movie/subject_search?search_text=%s'.format(
            join('Icons', 'douban.png')),
        'SearchEngine/default_engine_index': '0',
        'SuggestionState': '1',
        'SuggestionProvider/index': '0',
        'SuggestionProvider/data': str(KeywordGetter.QH360),
        'BrowserPath': '',
        'PrivateMode': '0',
        'Hotkey/keys': 'caps_lock',
        'Hotkey/interval': '0.3',
        'Hotkey/repetitions': '2',
        'Ui/distance': '3',
        'Ui/opacity': '0.9',
        'Ui/theme_index': '0',
        'Ui/border_radius': '0',
        'Ui/font_color': 'black',
        'Ui/theme_color': '#3498db',
        'Ui/border_color': '#a7acaf',
        'Ui/selected_color': '#91c9f7',
        'Ui/background_color': 'white',
        'NoSleepState': '0',
    }

    def __init__(self, work_thread=None):
        super().__init__()
        self.__is_moving = False
        self.__mouse_pos = None
        self.__dialog_pos = None
        self.__selected_row = 0
        self.__pressed_keys = []
        self.__setting_changed_manually = True
        self._setting = QSettings()
        self.__check_settings()
        self._ui = Ui_Dialog()
        self._ui.setupUi(self)
        self.__theme_buttons = [self._ui.pushButton_blue, self._ui.pushButton_green,
                                self._ui.pushButton_yellow, self._ui.pushButton_orange,
                                self._ui.pushButton_red, self._ui.pushButton_purple,
                                self._ui.pushButton_grey, self._ui.pushButton_black]
        self.reload_ui()
        self.__new_version_checker = NewVersionChecker(work_thread)
        self.__connect_event_handlers()
        self.__key_setting_listener.start()
        if int(self._setting.value('StartupState')):
            self._change_startup_state(True)
        self._tip_state = int(self._setting.value('TipState'))
        self.__worker = Worker()
        self.__worker.start()
        if not int(self._setting.value('NoSleepState')):
            self.__worker.suspend()

    def __check_settings(self):
        if not self._setting.value('TipState'):
            for name, setting in self.default_setting.items():
                if not self._setting.value(name):
                    self._setting.setValue(name, setting)

    def _change_startup_state(self, checked):
        if 'win' == platform[:3]:
            from getpass import getuser
            username = getuser()
            if checked:
                from subprocess import Popen
                Popen(('CreateStartup.vbs', username), shell=True)
            else:
                from os import remove
                try:
                    remove(r'C:\Users\{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\XSearch.lnk'.
                           format(username))
                except FileNotFoundError:
                    pass
            self._setting.setValue('StartupState', str(int(checked)))

    def _change_tip_state(self, checked):
        self._tip_state = checked
        self._setting.setValue('TipState', str(int(checked)))

    def _change_language(self, index):
        if self.__setting_changed_manually:
            self._setting.setValue('Language', self._ui.comboBox_language.currentData())
            modules.pop('Languages')
            self.reload_ui(qss=False)

    def _change_engine_data(self, item):
        if self.__setting_changed_manually:
            row = item.index().row()
            engine_data = [self._ui.model.data(self._ui.model.index(row, 0)),
                           self._ui.model.data(self._ui.model.index(row, 1)),
                           self._ui.model.data(self._ui.model.index(row, 2))]
            if int(self._setting.value('SearchEngine/count')) == row:
                if all(engine_data):
                    self._setting.setValue('SearchEngine/count', str(row + 1))
                    self._setting.setValue('SearchEngine/engines/{}'.format(row), '||'.join(engine_data))
                    self._ui.model.setRowCount(row + 2)
            else:
                self._setting.setValue('SearchEngine/engines/{}'.format(row), '||'.join(engine_data))

    def _change_default_engine(self):
        self._setting.setValue('SearchEngine/default_engine_index', str(self.__selected_row))

    def _delete_engine(self):
        self.__setting_changed_manually = False
        last_index = int(self._setting.value('SearchEngine/count')) - 1
        last_engine_data = self._setting.value('SearchEngine/engines/{}'.format(last_index))
        kw, icon, url = last_engine_data.split('||')
        if last_index != self.__selected_row:
            self._setting.setValue('SearchEngine/engines/{}'.format(self.__selected_row), last_engine_data)
            self._ui.model.setData(self._ui.model.index(self.__selected_row, 0), kw)
            self._ui.model.setData(self._ui.model.index(self.__selected_row, 1), icon)
            self._ui.model.setData(self._ui.model.index(self.__selected_row, 1), QIcon(icon), Qt.DecorationRole)
            self._ui.model.setData(self._ui.model.index(self.__selected_row, 2), url)
        self._setting.setValue('SearchEngine/count', str(last_index))
        self._setting.remove('SearchEngine/engines/{}'.format(last_index))
        self._ui.model.setData(self._ui.model.index(last_index, 0), '')
        self._ui.model.setData(self._ui.model.index(last_index, 1), '')
        self._ui.model.setData(self._ui.model.index(last_index, 1), None, Qt.DecorationRole)
        self._ui.model.setData(self._ui.model.index(last_index, 2), '')
        self._ui.model.setRowCount(last_index + 1)
        self.__setting_changed_manually = True

    def _change_suggestion_state(self, checked):
        self._ui.comboBox_suggestion_engine.setEnabled(checked)
        self._setting.setValue('SuggestionState', str(int(checked)))

    def _change_suggestion_provider(self, index):
        current_data = str(self._ui.comboBox_suggestion_engine.currentData())
        if self._setting.value('SuggestionProvider/data') == current_data:
            return
        self._setting.setValue('SuggestionProvider/index', str(index))
        self._setting.setValue('SuggestionProvider/data', str(self._ui.comboBox_suggestion_engine.currentData()))
        self._ui.pushButton_suggestion_clear_cache.click()

    def _clear_suggestion_cache(self):
        pass

    def _change_browser_path(self):
        from Languages import Strings
        filename = QFileDialog.getOpenFileName(parent=self, caption=Strings.SETTING_CHOOSE_BROWSER,
                                               filter='*.exe;*.sh')[0]
        if filename:
            self._ui.lineEdit_browser_path.setText(filename)
            self._setting.setValue('BrowserPath', filename)
            self._ui.lineEdit_browser_path.setFocus(True)

    def _change_private_mode_state(self, checked):
        self._setting.setValue('PrivateMode', str(int(checked)))

    def __change_hotkey_type(self, checked):
        from Languages import Strings
        text = self.sender().text()
        if Strings.SETTING_SINGLE_KEY == text:
            self._ui.comboBox_repetitions.setEnabled(True)
            self._ui.comboBox_interval.setEnabled(True)
        else:
            self._ui.comboBox_repetitions.setEnabled(False)
            self._ui.comboBox_interval.setEnabled(False)
        self._ui.lineEdit_key_setting.clear()

    def _change_hotkey_repetitions(self, index):
        self._setting.setValue('Hotkey/repetitions', self._ui.comboBox_repetitions.currentText())

    def _change_hotkey_interval(self, index):
        self._setting.setValue('Hotkey/interval', self._ui.comboBox_interval.currentText())

    def _change_theme(self, checked):
        cur_button = self.sender()
        button_color = cur_button.palette().button().color()
        theme_color = '#{}'.format(hex(button_color.rgb())[-6:])
        if '#1f1f1f' == theme_color:
            font_color = 'white'
            selected_color = '#71b7e6'
            background_color = '#1f1f1f'
        else:
            font_color = 'black'
            selected_color = theme_color.replace('#', '#B2')
            background_color = 'white'
        self._setting.setValue('Ui/font_color', font_color)
        self._setting.setValue('Ui/theme_color', theme_color)
        self._setting.setValue('Ui/selected_color', selected_color)
        self._setting.setValue('Ui/background_color', background_color)
        for index, button in enumerate(self.__theme_buttons):
            if cur_button == button:
                self._setting.setValue('Ui/theme_index', str(index))
                break
        self.reload_ui(text=False)

    def _custom_theme(self):
        """Custom theme. Waiting to be done."""

    def _change_opacity(self, index):
        self._setting.setValue('Ui/opacity', self._ui.comboBox_opacity.currentText())

    def _change_fillet(self, index):
        self._setting.setValue('Ui/border_radius', str(index))
        self.reload_ui(text=False)

    def _change_distance(self, index):
        self._setting.setValue('Ui/distance', str(index))

    def _change_no_sleep_state(self, checked):
        self.__worker.changeWorkingState()
        self._setting.setValue('NoSleepState', str(int(checked)))

    def __import_settings(self):
        from Languages import Strings
        filename = QFileDialog.getOpenFileName(parent=self, caption=Strings.SETTING_CHOOSE_IMPORT,
                                               filter='*.json')[0]
        if filename:
            setting_map = load(open(filename))
            for name, setting in setting_map.items():
                self._setting.setValue(name, setting)
            self._load_settings()
            self.reload_ui()

    def __export_settings(self):
        from Languages import Strings
        filename = QFileDialog.getSaveFileName(parent=self, caption=Strings.SETTING_CHOOSE_EXPORT,
                                               directory='XSearch_Setting.json', filter='*.json')[0]
        if filename:
            setting_map = {}
            for name in self.default_setting.keys():
                setting_map[name] = self._setting.value(name)
            dump(setting_map, open(filename, 'w'))

    def _check_new_version(self, checked):
        self._ui.pushButton_check_update.setEnabled(False)
        self.__check_new_version_signal.emit()

    def _show_new_version_result(self, state):
        from Languages import Strings
        self._ui.label_update_tip.setText(getattr(Strings, 'SETTING_CHECK_UPDATE_TIP{}'.format(state), ''))
        if state != NewVersionChecker.CHECKING:
            self._ui.pushButton_check_update.setEnabled(True)

    def __connect_event_handlers(self):
        self._ui.widget_up.mousePressEvent = self.__mouse_press_event
        self._ui.widget_up.mouseMoveEvent = self.__mouse_move_event
        self._ui.widget_up.mouseReleaseEventEvent = self.__mouse_release_event
        self._ui.widget_left.mousePressEvent = self.__mouse_press_event
        self._ui.widget_left.mouseMoveEvent = self.__mouse_move_event
        self._ui.widget_left.mouseReleaseEventEvent = self.__mouse_release_event
        self._ui.pushButton_close.clicked.connect(self._hide_dialog)
        self._ui.pushButton_minimize.clicked.connect(self.showMinimized)
        self._ui.treeWidget.itemClicked.connect(self.__tree_item_clicked)

        self._ui.checkBox_start_up.clicked.connect(self._change_startup_state)
        self._ui.checkBox_show_tip.clicked.connect(self._change_tip_state)
        self._ui.comboBox_language.currentIndexChanged.connect(self._change_language)

        self._ui.model.itemChanged.connect(self._change_engine_data)
        self._ui.tableView_search_engine.customContextMenuRequested.connect(self.__popup_menu)
        self._ui.table_menu.setActionHandler('set_default_engine', self._change_default_engine)
        self._ui.table_menu.setActionHandler('delete', self._delete_engine)
        self._ui.checkBox_search_suggestion.clicked.connect(self._change_suggestion_state)
        self._ui.comboBox_suggestion_engine.currentIndexChanged.connect(self._change_suggestion_provider)
        self._ui.pushButton_suggestion_clear_cache.clicked.connect(self._clear_suggestion_cache)
        self._ui.pushButton_browser_path.clicked.connect(self._change_browser_path)
        self._ui.checkBox_private_mode.clicked.connect(self._change_private_mode_state)

        self._ui.radioButton_single_key.clicked.connect(self.__change_hotkey_type)
        self._ui.radioButton_multiple_key.clicked.connect(self.__change_hotkey_type)
        self.__key_setting_listener = Listener(self.__on_key_press, self.__on_key_release)
        self._ui.comboBox_repetitions.currentIndexChanged.connect(self._change_hotkey_repetitions)
        self._ui.comboBox_interval.currentIndexChanged.connect(self._change_hotkey_interval)

        self._ui.comboBox_opacity.currentIndexChanged.connect(self._change_opacity)
        self._ui.comboBox_fillet.currentIndexChanged.connect(self._change_fillet)
        self._ui.comboBox_distance.currentIndexChanged.connect(self._change_distance)
        for button in self.__theme_buttons:
            button.clicked.connect(self._change_theme)
        self._ui.pushButton_custom.clicked.connect(self._custom_theme)

        self._ui.checkBox_no_sleep.clicked.connect(self._change_no_sleep_state)
        self._ui.pushButton_import_settings.clicked.connect(self.__import_settings)
        self._ui.pushButton_export_settings.clicked.connect(self.__export_settings)

        self.__new_version_checker.signal.connect(self._show_new_version_result)
        self.__check_new_version_signal.connect(self.__new_version_checker.check)
        self._ui.pushButton_check_update.clicked.connect(self._check_new_version)

    def __on_key_release(self, key):
        key_name = getattr(key, 'name', None)
        key_name = key_name if key_name else key.char
        if key_name in self.__pressed_keys:
            self.__pressed_keys.remove(key_name)
        if self._ui.lineEdit_key_setting.hasFocus() and self._ui.radioButton_single_key.isChecked():
            self._ui.lineEdit_key_setting.setText(key_name)
            self._setting.setValue('Hotkey/keys', key_name)

    def __on_key_press(self, key):
        if self._ui.lineEdit_key_setting.hasFocus():
            key_name = getattr(key, 'name', None)
            key_name = key_name if key_name else key.char
            if key_name not in self.__pressed_keys:
                self.__pressed_keys.append(key_name)
            if self._ui.radioButton_multiple_key.isChecked() and 1 < len(self.__pressed_keys):
                keys = '+'.join(self.__pressed_keys)
                self._ui.lineEdit_key_setting.setText(keys)
                self._setting.setValue('Hotkey/keys', keys)

    def __tree_item_clicked(self, item, column):
        item.setSelected(True)
        if item.childCount():
            item.setSelected(False)
            if not item.isExpanded():
                item.setExpanded(True)
            self.__tree_item_clicked(item.child(0), column)
        else:
            from Languages import Strings
            data = item.data(0, Qt.DisplayRole)
            if Strings.SETTING_BASICS == data:
                self._ui.frame_basics.raise_()
            if Strings.SETTING_ENGINE_MANAGEMENT == data:
                self._ui.frame_engine_management.raise_()
            elif Strings.SETTING_OTHER == data:
                self._ui.frame_search_other.raise_()
            elif Strings.SETTING_HOTKEY == data:
                self._ui.frame_hotkey.raise_()
            elif Strings.SETTING_APPEARANCE == data:
                self._ui.frame_appearance.raise_()
            elif Strings.SETTING_ADVANCED == data:
                self._ui.frame_advanced.raise_()
            elif Strings.SETTING_ABOUT == data:
                self._ui.frame_about.raise_()
                self._ui.label_update_tip.clear()

    def _load_settings(self):
        self.__setting_changed_manually = False
        self._ui.checkBox_start_up.setChecked(int(self._setting.value('StartupState')))
        self._ui.checkBox_show_tip.setChecked(self._tip_state)
        from Languages import language_map
        self._ui.comboBox_language.setCurrentText(language_map.get(self._setting.value('Language')))
        row = int(self._setting.value('SearchEngine/count'))
        self._ui.model.setRowCount(row + 1)
        for i in range(row):
            kw, icon, url = self._setting.value('SearchEngine/engines/{}'.format(i)).split('||')
            self._ui.model.setData(self._ui.model.index(i, 0), kw)
            self._ui.model.setData(self._ui.model.index(i, 1), icon)
            self._ui.model.setData(self._ui.model.index(i, 1), QIcon(icon), Qt.DecorationRole)
            self._ui.model.setData(self._ui.model.index(i, 2), url)
        suggestion_state = int(self._setting.value('SuggestionState'))
        self._ui.checkBox_search_suggestion.setChecked(suggestion_state)
        self._ui.comboBox_suggestion_engine.setEnabled(suggestion_state)
        self._ui.comboBox_suggestion_engine.setCurrentIndex(int(self._setting.value('SuggestionProvider/index')))
        self._ui.lineEdit_browser_path.setText(self._setting.value('BrowserPath'))
        self._ui.checkBox_private_mode.setChecked(int(self._setting.value('PrivateMode')))
        keys = self._setting.value('Hotkey/keys')
        if 1 == len(keys.split('+')):
            self._ui.radioButton_single_key.setChecked(True)
            self._ui.radioButton_single_key.click()
        else:
            self._ui.radioButton_multiple_key.setChecked(True)
            self._ui.radioButton_multiple_key.click()
        self._ui.lineEdit_key_setting.setText(keys)
        self._ui.comboBox_repetitions.setCurrentText(self._setting.value('Hotkey/repetitions'))
        self._ui.comboBox_interval.setCurrentText(self._setting.value('Hotkey/interval'))
        self._ui.comboBox_opacity.setCurrentText(self._setting.value('Ui/opacity'))
        self._ui.comboBox_fillet.setCurrentText(self._setting.value('Ui/border_radius'))
        self._ui.comboBox_distance.setCurrentText(self._setting.value('Ui/distance'))
        self._ui.checkBox_no_sleep.setChecked(int(self._setting.value('NoSleepState')))
        self.__setting_changed_manually = True

    def reload_ui(self, text=True, qss=True):
        """
        Reload current user interface.
        :param text: whether or not to reload text.
        :param qss: whether or not to reload qss.
        """
        if text:
            self._ui.retranslateUi(self)
        if qss:
            font_color = self._setting.value('Ui/font_color')
            theme_color = self._setting.value('Ui/theme_color')
            border_color = self._setting.value('Ui/border_color')
            border_radius = self._setting.value('Ui/border_radius')
            border_radius_s = str(int(border_radius) * 0.5)
            selected_color = self._setting.value('Ui/selected_color')
            background_color = self._setting.value('Ui/background_color')
            self._ui.widget_up.setStyleSheet('''.QWidget {{
            border-top: 1px solid {};
            background-color: white;
            }}'''.format(theme_color))
            self._ui.widget_left.setStyleSheet('''.QWidget {{
            border: 1px solid {};
            border-right: 0;
            background-color: {};
            border-top-left-radius: {}px;
            border-bottom-left-radius: {}px;
            }}'''.format(border_color, theme_color, border_radius, border_radius))
            right_qss = '''.QWidget {
            border: 1px solid {theme_color};
            border-left: 0;
            background-color: white;
            border-top-right-radius: {border_radius}px;
            border-bottom-right-radius: {border_radius}px;
            }
            .QWidget > QFrame {border-right: 1px solid {theme_color}; background-color: white;}
            .QWidget QLabel[width="600"] {
            font: 900 21px;
            border: 7px;
            border-left-style: solid;
            border-left-color: {theme_color};
            }
            .QWidget QLineEdit {border: 2px solid; border-color: {border_color}; border-radius: {border_radius_s}px;}
            .QWidget QLineEdit:focus {border-color: {theme_color};}
            .QWidget QPushButton {
            font-weight: 900;
            color: {theme_color};
            outline: none;
            background-color: {button_color1};
            border-radius: {border_radius};
            }
            .QWidget QPushButton:hover {background-color: {button_color2};}
            .QWidget QPushButton:pressed {background-color: {button_color3};}
            .QWidget QPushButton:!enabled {color: {border_color};}
            .QWidget QComboBox {border: 1px solid {theme_color}; border-radius: {border_radius_s}px;}
            .QWidget QComboBox QAbstractItemView {border: 1px solid {theme_color};}
            .QWidget QComboBox:!enabled {border: 1px solid {border_color}; background-color: #e1e1e1;}
            .QWidget QCheckBox::indicator, .QWidget QRadioButton::indicator {
            width: 16px;
            height: 16px;
            border: 1px solid {theme_color};
            border-radius: {border_radius_s}px;
            }
            .QWidget QCheckBox::indicator:pressed, .QWidget QRadioButton::indicator:pressed {
            background-color: {theme_color};
            }
            .QWidget QCheckBox::indicator:checked, .QWidget QRadioButton::indicator:checked {
            background-color: {theme_color};
            image: url(Icons/check.png);
            image-position: center;
            }'''
            right_qss = right_qss.replace('{theme_color}', theme_color).replace('{border_color}', border_color)
            right_qss = right_qss.replace('{border_radius}', border_radius).replace('{border_radius_s}',
                                                                                    border_radius_s)
            right_qss = right_qss.replace('{button_color1}', theme_color.replace('#', '#26'))
            right_qss = right_qss.replace('{button_color2}', theme_color.replace('#', '#3F'))
            right_qss = right_qss.replace('{button_color3}', theme_color.replace('#', '#59'))
            self._ui.widget_right.setStyleSheet(right_qss)
            self._ui.label_logo.setStyleSheet('.QLabel {font: 54px; color: white;}')
            self._ui.treeWidget.setStyleSheet('''.QTreeWidget {{
            font: 500 20px;
            color: white;
            border: 0;
            border-left: 1px solid {};
            outline: 0;
            background-color: {};
            }}
            .QTreeWidget::item {{
            height: 50px;
            margin: 3px 0;
            border-top-left-radius: {}px;
            border-bottom-left-radius: {}px;
            }}
            .QTreeWidget::item:selected {{
            image: url(Icons/triangle.png);
            image-position: right;
            background-color: rgba(0, 0, 0, 0.2);
            }}
            .QTreeWidget::item:selected:!active {{color: white;}}
            .QTreeWidget::item:hover {{
            background-color: rgba(255, 255, 255, 0.2);
            }}'''.format(border_color, theme_color, border_radius, border_radius))
            self._ui.pushButton_minimize.setStyleSheet('''.QPushButton {{
            font: 24px;
            outline: none;
            color: #85c43b;
            border-radius: {}px;
            background-color: #85c43b;
            }}
            .QPushButton:hover {{color: white;}}
            .QPushButton:pressed {{font: 18px;}}'''.format(border_radius))
            self._ui.pushButton_close.setStyleSheet('''.QPushButton {{
            font: 18px;
            outline: none;
            color: #ea6e4d;
            border-radius: {}px;
            background-color: #ea6e4d;
            }}
            .QPushButton:hover {{color: white;}}
            .QPushButton:pressed {{font: 16px;}}'''.format(border_radius))
            self._ui.tableView_search_engine.setStyleSheet('''.QTableView {{
            outline: none;
            border: 1px solid {};
            }}
            .QTableView::item {{min-height: 30px; border-radius: {}px;}}
            .QTableView::item:selected {{
            background-color: {};
            }}'''.format(theme_color, border_radius_s, selected_color))
            self._ui.table_menu.setStyleSheet('''QMenu {{
            color: {};
            font: 17px;
            padding:3px 3px;
            border: 1px solid {};
            background-color: {};
            }}
            QMenu::item {{
            margin:1px 1px;
            border-radius: {}px;
            padding:8px 20px 8px 0;
            background-color: transparent;
            }}
            QMenu::item:selected {{
            background-color: {};
            }}'''.format(font_color, border_color, background_color, border_radius, selected_color))
            self._ui.frame_appearance.setStyleSheet('''#groupBox_custom {{border: none;}}
            QPushButton {{outline: none; border-radius: {}px;}}
            #pushButton_blue {{background-color: #3498db;}}
            #pushButton_green {{background-color: #4daf7c;}}
            #pushButton_yellow {{background-color: #e9d460;}}
            #pushButton_orange {{background-color: #f5ab35;}}
            #pushButton_red {{background-color: #d64541;}}
            #pushButton_purple {{background-color: #9b59b6;}}
            #pushButton_grey {{background-color: #6c7a89;}}
            #pushButton_black {{background-color: #1f1f1f;}}
            #pushButton_custom {{background-color: rgba(0, 0, 0, 0.3);}}'''.format(border_radius))
            theme_index = int(self._setting.value('Ui/theme_index'))
            for index, button in enumerate(self.__theme_buttons):
                if theme_index == index:
                    button.parent().setStyleSheet('''.QGroupBox {{
                    color: {};
                    border: 3px solid {};
                    border-radius: {}px;
                    }}'''.format(theme_color, theme_color, border_radius))
                else:
                    button.parent().setStyleSheet('.QGroupBox {border: none;}')

    def popup(self):
        self._load_settings()
        self.show()

    def _hide_dialog(self):
        row = self._ui.model.rowCount() - 1
        self._ui.model.clearItemData(self._ui.model.index(row, 0))
        self._ui.model.clearItemData(self._ui.model.index(row, 1))
        self._ui.model.clearItemData(self._ui.model.index(row, 2))
        self._ui.tableView_search_engine.clearSelection()
        self.hide()

    def __popup_menu(self, point):
        selected_row = self._ui.tableView_search_engine.indexAt(point).row()
        if selected_row in (-1, self._ui.model.rowCount() - 1):
            return
        self.__selected_row = selected_row
        point.setY(point.y() + 35)
        self._ui.table_menu.popup(self._ui.tableView_search_engine.mapToGlobal(point))

    def __mouse_press_event(self, event):
        if Qt.LeftButton == event.button():
            self.__is_moving = True
            self.__dialog_pos = self.frameGeometry().topLeft()
            self.__mouse_pos = event.globalPos()

    def __mouse_move_event(self, event):
        if event.buttons() & Qt.LeftButton:
            relative_pos = event.globalPos() - self.__mouse_pos
            self.move(self.__dialog_pos + relative_pos)

    def __mouse_release_event(self, event):
        if Qt.LeftButton == event.button():
            self.__is_moving = False

    def closeEvent(self, event):
        self._hide_dialog()
        event.ignore()

    def keyPressEvent(self, event):
        key = event.key()
        if Qt.Key_Escape == key:
            self._hide_dialog()
        event.ignore()

    @property
    def work_thread(self):
        return self.__new_version_checker.thread
