# -*- coding: utf-8 -*-
#
# Copyright 2019 Xpp521
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
#
# Form implementation generated from reading ui file 'SettingDialog_ui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
from os.path import join
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName('Dialog')
        Dialog.resize(1025, 675)
        Dialog.setWindowIcon(QIcon(join('Icons', 'XSearch.ico')))
        self.treeWidget = QtWidgets.QTreeWidget(Dialog)
        self.treeWidget.setGeometry(QtCore.QRect(30, 38, 200, 600))
        self.treeWidget.setObjectName('treeWidget')
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        self.frame_search = QtWidgets.QFrame(Dialog)
        self.frame_search.setGeometry(QtCore.QRect(260, 38, 735, 600))
        self.frame_search.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_search.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_search.setObjectName('frame_search')
        self.checkBox_private_mode = QtWidgets.QCheckBox(self.frame_search)
        self.checkBox_private_mode.setGeometry(QtCore.QRect(40, 340, 91, 20))
        self.checkBox_private_mode.setObjectName('checkBox_private_mode')
        self.label_search_engine = QtWidgets.QLabel(self.frame_search)
        self.label_search_engine.setGeometry(QtCore.QRect(40, 20, 72, 16))
        self.label_search_engine.setObjectName('label_search_engine')
        self.label_private_mode = QtWidgets.QLabel(self.frame_search)
        self.label_private_mode.setGeometry(QtCore.QRect(40, 290, 72, 16))
        self.label_private_mode.setObjectName('label_private_mode')
        self.label_private_mode_tip = QtWidgets.QLabel(self.frame_search)
        self.label_private_mode_tip.setGeometry(QtCore.QRect(40, 310, 431, 16))
        self.label_private_mode_tip.setObjectName('label_private_mode_tip')
        self.label_browser_path = QtWidgets.QLabel(self.frame_search)
        self.label_browser_path.setGeometry(QtCore.QRect(40, 220, 81, 16))
        self.label_browser_path.setObjectName('label_browser_path')
        self.pushButton_browser_path = QtWidgets.QPushButton(self.frame_search)
        self.pushButton_browser_path.setGeometry(QtCore.QRect(260, 220, 51, 29))
        self.pushButton_browser_path.setObjectName('pushButton_browser_path')
        self.comboBox_search_engine = QtWidgets.QComboBox(self.frame_search)
        self.comboBox_search_engine.setGeometry(QtCore.QRect(140, 20, 88, 22))
        self.comboBox_search_engine.setObjectName('comboBox_search_engine')
        self.comboBox_search_engine.addItem('')
        self.comboBox_search_engine.addItem('')
        self.comboBox_search_engine.addItem('')
        self.comboBox_search_engine.addItem('')
        self.comboBox_search_engine.addItem('')
        self.comboBox_search_engine.addItem('')
        self.comboBox_search_engine.addItem('')
        self.comboBox_search_engine.addItem('')
        self.lineEdit_browser_path = QtWidgets.QLineEdit(self.frame_search)
        self.lineEdit_browser_path.setGeometry(QtCore.QRect(140, 220, 113, 22))
        self.lineEdit_browser_path.setReadOnly(True)
        self.lineEdit_browser_path.setObjectName('lineEdit_browser_path')
        self.label_suggestion_engine = QtWidgets.QLabel(self.frame_search)
        self.label_suggestion_engine.setGeometry(QtCore.QRect(40, 150, 101, 16))
        self.label_suggestion_engine.setObjectName('label_suggestion_engine')
        self.comboBox_suggest_engine = QtWidgets.QComboBox(self.frame_search)
        self.comboBox_suggest_engine.setGeometry(QtCore.QRect(150, 140, 88, 22))
        self.comboBox_suggest_engine.setObjectName('comboBox_suggest_engine')
        self.comboBox_suggest_engine.addItem('')
        self.comboBox_suggest_engine.addItem('')
        self.comboBox_suggest_engine.addItem('')
        self.label_search_suggestion = QtWidgets.QLabel(self.frame_search)
        self.label_search_suggestion.setGeometry(QtCore.QRect(40, 90, 72, 16))
        self.label_search_suggestion.setObjectName('label_search_suggestion')
        self.checkBox_search_suggestion = QtWidgets.QCheckBox(self.frame_search)
        self.checkBox_search_suggestion.setGeometry(QtCore.QRect(40, 120, 91, 20))
        self.checkBox_search_suggestion.setObjectName('checkBox_search_suggestion')
        self.frame_appearance = QtWidgets.QFrame(Dialog)
        self.frame_appearance.setGeometry(QtCore.QRect(260, 38, 735, 600))
        self.frame_appearance.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_appearance.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_appearance.setObjectName('frame_appearance')
        self.label_language = QtWidgets.QLabel(self.frame_appearance)
        self.label_language.setGeometry(QtCore.QRect(110, 380, 72, 16))
        self.label_language.setObjectName('label_language')
        self.comboBox_language = QtWidgets.QComboBox(self.frame_appearance)
        self.comboBox_language.setGeometry(QtCore.QRect(170, 380, 88, 22))
        self.comboBox_language.setObjectName('comboBox_language')
        self.comboBox_language.addItem('')
        self.comboBox_language.addItem('')
        self.label_opacity = QtWidgets.QLabel(self.frame_appearance)
        self.label_opacity.setGeometry(QtCore.QRect(100, 430, 72, 16))
        self.label_opacity.setObjectName('label_opacity')
        self.comboBox_opacity = QtWidgets.QComboBox(self.frame_appearance)
        self.comboBox_opacity.setGeometry(QtCore.QRect(170, 430, 88, 22))
        self.comboBox_opacity.setObjectName('comboBox_opacity')
        self.comboBox_opacity.addItem('')
        self.comboBox_opacity.addItem('')
        self.comboBox_opacity.addItem('')
        self.comboBox_opacity.addItem('')
        self.comboBox_opacity.addItem('')
        self.comboBox_opacity.addItem('')
        self.frame_other = QtWidgets.QFrame(Dialog)
        self.frame_other.setGeometry(QtCore.QRect(260, 38, 735, 600))
        self.frame_other.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_other.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_other.setObjectName('frame_other')
        self.label_no_sleep = QtWidgets.QLabel(self.frame_other)
        self.label_no_sleep.setGeometry(QtCore.QRect(420, 410, 72, 16))
        self.label_no_sleep.setObjectName('label_no_sleep')
        self.checkBox_no_sleep = QtWidgets.QCheckBox(self.frame_other)
        self.checkBox_no_sleep.setGeometry(QtCore.QRect(420, 440, 91, 20))
        self.checkBox_no_sleep.setObjectName('checkBox_no_sleep')
        self.frame_hotkey = QtWidgets.QFrame(Dialog)
        self.frame_hotkey.setGeometry(QtCore.QRect(260, 38, 735, 600))
        self.frame_hotkey.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_hotkey.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_hotkey.setObjectName('frame_hotkey')
        self.label_key_type = QtWidgets.QLabel(self.frame_hotkey)
        self.label_key_type.setGeometry(QtCore.QRect(370, 20, 91, 16))
        self.label_key_type.setObjectName('label_key_type')
        self.radioButton_single_key = QtWidgets.QRadioButton(self.frame_hotkey)
        self.radioButton_single_key.setGeometry(QtCore.QRect(370, 60, 115, 20))
        self.radioButton_single_key.setObjectName('radioButton_single_key')
        self.radioButton_multiple_key = QtWidgets.QRadioButton(self.frame_hotkey)
        self.radioButton_multiple_key.setGeometry(QtCore.QRect(370, 90, 115, 20))
        self.radioButton_multiple_key.setObjectName('radioButton_multiple_key')
        self.lineEdit_key_setting = QtWidgets.QLineEdit(self.frame_hotkey)
        self.lineEdit_key_setting.setGeometry(QtCore.QRect(380, 190, 100, 22))
        self.lineEdit_key_setting.setObjectName('lineEdit_key_setting')
        self.lineEdit_key_setting.setReadOnly(True)
        self.label_key_setting_tip = QtWidgets.QLabel(self.frame_hotkey)
        self.label_key_setting_tip.setGeometry(QtCore.QRect(380, 160, 201, 16))
        self.label_key_setting_tip.setObjectName('label_key_setting_tip')
        self.label_key_setting = QtWidgets.QLabel(self.frame_hotkey)
        self.label_key_setting.setGeometry(QtCore.QRect(370, 130, 81, 16))
        self.label_key_setting.setObjectName('label_key_setting')
        self.groupBox_extra_setting = QtWidgets.QGroupBox(self.frame_hotkey)
        self.groupBox_extra_setting.setGeometry(QtCore.QRect(360, 230, 221, 121))
        self.groupBox_extra_setting.setObjectName('groupBox_extra_setting')
        self.comboBox_press_times = QtWidgets.QComboBox(self.groupBox_extra_setting)
        self.comboBox_press_times.setGeometry(QtCore.QRect(100, 60, 100, 22))
        self.comboBox_press_times.setObjectName('comboBox_press_times')
        self.comboBox_press_times.addItem('')
        self.comboBox_press_times.addItem('')
        self.comboBox_press_times.addItem('')
        self.comboBox_press_times.addItem('')
        self.comboBox_press_times.addItem('')
        self.label_extra_key_setting_tip = QtWidgets.QLabel(self.groupBox_extra_setting)
        self.label_extra_key_setting_tip.setGeometry(QtCore.QRect(10, 30, 191, 16))
        self.label_extra_key_setting_tip.setObjectName('label_extra_key_setting_tip')
        self.label_interval = QtWidgets.QLabel(self.groupBox_extra_setting)
        self.label_interval.setGeometry(QtCore.QRect(10, 90, 72, 16))
        self.label_interval.setObjectName('label_interval')
        self.label_press_times = QtWidgets.QLabel(self.groupBox_extra_setting)
        self.label_press_times.setGeometry(QtCore.QRect(10, 60, 72, 16))
        self.label_press_times.setObjectName('label_press_times')
        self.comboBox_interval = QtWidgets.QComboBox(self.groupBox_extra_setting)
        self.comboBox_interval.setGeometry(QtCore.QRect(100, 90, 100, 22))
        self.comboBox_interval.setObjectName('comboBox_interval')
        self.comboBox_interval.addItem('')
        self.comboBox_interval.addItem('')
        self.comboBox_interval.addItem('')
        self.comboBox_interval.addItem('')
        self.comboBox_interval.addItem('')
        self.comboBox_interval.addItem('')
        self.comboBox_interval.addItem('')
        self.comboBox_interval.addItem('')
        self.comboBox_interval.addItem('')
        self.comboBox_interval.addItem('')
        self.treeWidget.raise_()
        self.frame_other.raise_()
        self.frame_appearance.raise_()
        self.frame_hotkey.raise_()
        self.frame_search.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        from Strings import Strings
        Dialog.setWindowTitle(Strings.SETTING_DIALOG_TITLE)
        self.treeWidget.headerItem().setText(0, '')
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, Strings.SETTING_SEARCH)
        self.treeWidget.topLevelItem(1).setText(0, Strings.SETTING_HOTKEY)
        self.treeWidget.topLevelItem(2).setText(0, Strings.SETTING_APPEARANCE)
        self.treeWidget.topLevelItem(3).setText(0, Strings.SETTING_OTHER)
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.checkBox_private_mode.setText('{}{}'.format(Strings.SETTING_TURN_ON, Strings.SETTING_PRIVATE_MODE))
        self.label_search_engine.setText(Strings.SETTING_SEARCH_ENGINE)
        self.label_private_mode.setText(Strings.SETTING_PRIVATE_MODE)
        self.label_private_mode_tip.setText(Strings.SETTING_PRIVATE_MODE_TIP)
        self.label_browser_path.setText(Strings.SETTING_BROWSER_PATH)
        self.pushButton_browser_path.setText('...')
        self.comboBox_search_engine.setItemText(0, Strings.SETTING_BAIDU)
        self.comboBox_search_engine.setItemText(1, Strings.SETTING_GOOGLE)
        self.comboBox_search_engine.setItemText(2, Strings.SETTING_BING)
        self.comboBox_search_engine.setItemText(3, Strings.SETTING_BING_CN)
        self.comboBox_search_engine.setItemText(4, Strings.SETTING_360)
        self.comboBox_search_engine.setItemText(5, Strings.SETTING_SOGOU)
        self.comboBox_search_engine.setItemText(6, Strings.SETTING_TOUTIAO)
        self.comboBox_search_engine.setItemText(7, Strings.SETTING_YANDEX)
        self.label_suggestion_engine.setText(Strings.SETTING_SUGGEST_ENGINE)
        self.comboBox_suggest_engine.setItemText(0, Strings.SETTING_360)
        self.comboBox_suggest_engine.setItemText(1, Strings.SETTING_BAIDU)
        self.comboBox_suggest_engine.setItemText(2, Strings.SETTING_SOGOU)
        self.label_search_suggestion.setText(Strings.SETTING_SUGGEST)
        self.checkBox_search_suggestion.setText('{}{}'.format(Strings.SETTING_TURN_ON, Strings.SETTING_SUGGEST))
        self.label_language.setText(Strings.SETTING_LANGUAGE)
        self.comboBox_language.setItemText(0, Strings.SETTING_SIMPLIFIED_CHINESE)
        self.comboBox_language.setItemText(1, Strings.SETTING_ENGLISH)
        self.label_opacity.setText(Strings.SETTING_OPACITY)
        self.comboBox_opacity.setItemText(0, '0.9')
        self.comboBox_opacity.setItemText(1, '0.8')
        self.comboBox_opacity.setItemText(2, '0.7')
        self.comboBox_opacity.setItemText(3, '0.6')
        self.comboBox_opacity.setItemText(4, '0.5')
        self.comboBox_opacity.setItemText(5, '1')
        self.label_no_sleep.setText(Strings.SETTING_NO_SLEEP)
        self.checkBox_no_sleep.setText(Strings.SETTING_TURN_ON)
        self.label_key_type.setText(Strings.SETTING_HOTKEY_TYPE)
        self.radioButton_single_key.setText(Strings.SETTING_SINGLE_KEY)
        self.radioButton_multiple_key.setText(Strings.SETTING_MULTIPLE_KEY)
        self.comboBox_interval.setItemText(0, '0.5')
        self.comboBox_interval.setItemText(1, '0.1')
        self.comboBox_interval.setItemText(2, '0.2')
        self.comboBox_interval.setItemText(3, '0.3')
        self.comboBox_interval.setItemText(4, '0.4')
        self.comboBox_interval.setItemText(5, '0.6')
        self.comboBox_interval.setItemText(6, '0.7')
        self.comboBox_interval.setItemText(7, '0.8')
        self.comboBox_interval.setItemText(8, '0.9')
        self.comboBox_interval.setItemText(9, '1')
        self.comboBox_press_times.setItemText(0, '2')
        self.comboBox_press_times.setItemText(1, '3')
        self.comboBox_press_times.setItemText(2, '4')
        self.comboBox_press_times.setItemText(3, '5')
        self.comboBox_press_times.setItemText(4, '1')
        self.label_key_setting_tip.setText(Strings.SETTING_KEY_SETTING_TIP)
        self.label_interval.setText(Strings.SETTING_INTERVAL)
        self.label_press_times.setText(Strings.SETTING_PRESS_TIMES)
        self.label_key_setting.setText(Strings.SETTING_KEY_SETTING)
        self.groupBox_extra_setting.setTitle(Strings.SETTING_EXTRA_SETTING)
        self.label_extra_key_setting_tip.setText(Strings.SETTING_EXTRA_SETTING_TIP)
        self.comboBox_search_engine.setItemData(0, '{}||https://www.baidu.com/s?ie=utf-8&wd=%s'.format(
            join('Icons', 'baidu.png')))
        self.comboBox_search_engine.setItemData(1, '{}||https://www.google.com/search?q=%s'.format(
            join('Icons', 'google.png')))
        self.comboBox_search_engine.setItemData(2, '{}||http://www.bing.com/search?q=%s'.format(join('Icons',
                                                                                                     'bing.png')))
        self.comboBox_search_engine.setItemData(3, '{}||http://cn.bing.com/search?q=%s'.format(join('Icons',
                                                                                                    'bing.png')))
        self.comboBox_search_engine.setItemData(4, '{}||https://www.so.com/s?ie=utf-8&q=%s'.format(join('Icons',
                                                                                                        '360.png')))
        self.comboBox_search_engine.setItemData(5, '{}||https://www.sogou.com/web?ie=utf8&query=%s'.format(
            join('Icons', 'sogou.png')))
        self.comboBox_search_engine.setItemData(6, '{}||https://m.toutiao.com/search/?&keyword=%s'.format(
            join('Icons', 'toutiao.png')))
        self.comboBox_search_engine.setItemData(7, '{}||https://yandex.com/search/?text=%s'.format(join('Icons',
                                                                                                        'yandex.png')))
        self.comboBox_suggest_engine.setItemData(0, '360')
        self.comboBox_suggest_engine.setItemData(1, 'baidu')
        self.comboBox_suggest_engine.setItemData(2, 'sogou')
        self.comboBox_language.setItemData(0, 'cn')
        self.comboBox_language.setItemData(1, 'en')
