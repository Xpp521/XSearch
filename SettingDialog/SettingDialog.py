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
from json import load, dump
from PyQt5.QtGui import QPixmap, QIcon
from sys import modules, platform
from pynput.keyboard import Listener
from PyQt5.QtCore import Qt, QSettings
from Utils.NoSleepWorker import Worker
from .SettingDialog_ui import Ui_Dialog
from Utils.SuggestionGetter import WebGetter
from PyQt5.QtWidgets import QDialog, QFileDialog, QTableWidgetItem


class SettingDialog(QDialog):
    default_setting = {
        'StartupState': '1',
        'TipState': '1',
        'Language/index': '0',
        'Language/data': 'cn',
        'SearchEngine/count': '8',
        'SearchEngine/engines/0': 'baidu||baidu.png||https://www.baidu.com/s?ie=utf-8&wd=%s',
        'SearchEngine/engines/1': 'google||google.png||https://www.google.com/search?q=%s',
        'SearchEngine/engines/2': 'bing||bing.png||http://www.bing.com/search?q=%s',
        'SearchEngine/engines/3': 'bingcn||bing.png||http://cn.bing.com/search?q=%s',
        'SearchEngine/engines/4': '360||360.png||https://www.so.com/s?ie=utf-8&q=%s',
        'SearchEngine/engines/5': 'sogou||sogou.png||https://www.sogou.com/web?ie=utf8&query=%s',
        'SearchEngine/engines/6': 'toutiao||toutiao.png||https://m.toutiao.com/search/?&keyword=%s',
        'SearchEngine/engines/7': 'yandex||yandex.png||https://yandex.com/search/?text=%s',
        'SearchEngine/default_engine_index': '0',
        'SuggestionState': '1',
        'SuggestionProvider/index': '0',
        'SuggestionProvider/data': str(WebGetter.QH360),
        'BrowserPath': '',
        'PrivateMode': '0',
        'Hotkey/keys': 'caps_lock',
        'Hotkey/repetitions': '2',
        'Hotkey/interval': '0.5',
        'Ui/opacity': '0.9',
        'Ui/distance': '3',
        'Ui/theme_index': '0',
        'Ui/border_radius': '0',
        'Ui/font_color': 'black',
        'Ui/theme_color': '#3498db',
        'Ui/border_color': '#a7acaf',
        'Ui/selected_color': '#91c9f7',
        'Ui/background_color': 'white',
        'NoSleepState': '0',
    }

    def __init__(self):
        super().__init__()
        self.__setting_changed = False
        self.__is_moving = False
        self.__dialog_pos = None
        self.__mouse_pos = None
        self.__pressed_keys = []
        self._setting = QSettings()
        self.__check_settings()
        self._ui = Ui_Dialog()
        self._ui.setupUi(self)
        self.__theme_buttons = [self._ui.pushButton_blue, self._ui.pushButton_green,
                                self._ui.pushButton_yellow, self._ui.pushButton_orange,
                                self._ui.pushButton_red, self._ui.pushButton_purple,
                                self._ui.pushButton_grey, self._ui.pushButton_black]
        self.reload_ui()
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
        self._setting.setValue('Language/index', str(index))
        self._setting.setValue('Language/data', self._ui.comboBox_language.currentData())
        modules.pop('Strings')
        self.reload_ui(qss=False)

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
        from Strings import Strings
        filename = QFileDialog.getOpenFileName(parent=self, caption=Strings.SETTING_CHOOSE_BROWSER,
                                               filter='*.exe;*.sh')[0]
        if filename:
            self._ui.lineEdit_browser_path.setText(filename)
            self._setting.setValue('BrowserPath', filename)
            self._ui.lineEdit_browser_path.setFocus(True)

    def _change_private_mode_state(self, checked):
        self._setting.setValue('PrivateMode', str(int(checked)))

    def __change_hotkey_type(self, checked):
        from Strings import Strings
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
            selected_color = '#91c9f7'
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
        pass

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
        from Strings import Strings
        filename = QFileDialog.getOpenFileName(parent=self, caption=Strings.SETTING_CHOOSE_IMPORT,
                                               filter='*.json')[0]
        if filename:
            setting_map = load(open(filename))
            for name, setting in setting_map.items():
                self._setting.setValue(name, setting)
            self._load_settings()
            self.reload_ui()

    def __export_settings(self):
        from Strings import Strings
        filename = QFileDialog.getSaveFileName(parent=self, caption=Strings.SETTING_CHOOSE_EXPORT,
                                               directory='XSearch_Setting.json', filter='*.json')[0]
        if filename:
            setting_map = {}
            for name in self.default_setting.keys():
                setting_map[name] = self._setting.value(name)
            dump(setting_map, open(filename, 'w'))

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
            from Strings import Strings
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

    def _load_settings(self):
        self._ui.checkBox_start_up.setChecked(int(self._setting.value('StartupState')))
        self._ui.checkBox_show_tip.setChecked(self._tip_state)
        self._ui.comboBox_language.setCurrentIndex(int(self._setting.value('Language/index')))
        row = int(self._setting.value('SearchEngine/count'))
        self._ui.tableWidget_search_engine.setRowCount(row)
        for i in range(row):
            kw, icon, url = self._setting.value('SearchEngine/engines/{}'.format(i)).split('||')
            self._ui.tableWidget_search_engine.setItem(i, 0, QTableWidgetItem(kw))
            self._ui.tableWidget_search_engine.setItem(i, 1, QTableWidgetItem(QIcon(join('Icons', icon)), ''))
            self._ui.tableWidget_search_engine.setItem(i, 2, QTableWidgetItem(url))
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

    def reload_ui(self, text=True, qss=True):
        """
        Reload current user interface.
        :param text: whether or not to reload text.
        :param qss: whether or not to reload qss.
        """
        if text:
            self._ui.retranslateUi(self)
        if qss:
            theme_color = self._setting.value('Ui/theme_color')
            border_color = self._setting.value('Ui/border_color')
            border_radius = self._setting.value('Ui/border_radius')
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
            color: {theme_color};
            outline: none;
            background-color: {button_color1};
            border-radius: {border_radius};
            }
            .QWidget QPushButton:hover {background-color: {button_color2};}
            .QWidget QPushButton:pressed {background-color: {button_color3};}
            .QWidget QPushButton:!enabled {font-weight: 900; color: {border_color};}
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
                                                                                    str(int(border_radius) * 0.5))
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
        self.hide()

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
