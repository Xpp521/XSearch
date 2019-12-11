from pynput.keyboard import Listener
from .SettingDialog_ui import Ui_Dialog
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal, QSettings


class SettingDialog(QDialog):
    setting_changed = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.__cur_hotkey = ''
        self.__cur_language = ''
        self.__pressed_keys = []
        self.__cur_no_sleep_status = 0
        self.__setting = QSettings()
        self.__ui = Ui_Dialog()
        self.__ui.setupUi(self)
        self.__ui.radioButton_single_key.clicked.connect(self.__change_hotkey_type)
        self.__ui.radioButton_multiple_key.clicked.connect(self.__change_hotkey_type)
        self.__ui.pushButton_browser_path.clicked.connect(self.__select_file)
        self.__ui.treeWidget.itemClicked.connect(self.__tree_item_clicked)
        self.__ui.treeWidget.itemDoubleClicked.connect(lambda item, column: None)
        self.__key_setting_listener = Listener(self.__on_key_press, self.__on_key_release)
        self.__key_setting_listener.start()

    def __on_key_release(self, key):
        key_name = getattr(key, 'name', None)
        key_name = key_name if key_name else key.char
        if key_name in self.__pressed_keys:
            self.__pressed_keys.remove(key_name)
        if self.__ui.lineEdit_key_setting.hasFocus() and self.__ui.radioButton_single_key.isChecked():
            self.__ui.lineEdit_key_setting.setText(key_name)

    def __on_key_press(self, key):
        if self.__ui.lineEdit_key_setting.hasFocus():
            key_name = getattr(key, 'name', None)
            key_name = key_name if key_name else key.char
            if key_name not in self.__pressed_keys:
                self.__pressed_keys.append(key_name)
            if self.__ui.radioButton_multiple_key.isChecked() and 1 < len(self.__pressed_keys):
                self.__ui.lineEdit_key_setting.setText('+'.join(self.__pressed_keys))

    def __change_hotkey_type(self, checked):
        from Strings import Strings
        text = self.sender().text()
        if Strings.SETTING_SINGLE_KEY == text:
            self.__ui.groupBox_extra_setting.setEnabled(True)
        else:
            self.__ui.groupBox_extra_setting.setEnabled(False)
        self.__ui.lineEdit_key_setting.clear()

    def __tree_item_clicked(self, item, column):
        if item.childCount() and not item.isExpanded():
            item.setExpanded(True)
            return
        from Strings import Strings
        data = item.data(0, Qt.DisplayRole)
        if Strings.SETTING_SEARCH == data:
            self.__ui.frame_search.raise_()
        elif Strings.SETTING_HOTKEY == data:
            self.__ui.frame_hotkey.raise_()
        elif Strings.SETTING_APPEARANCE == data:
            self.__ui.frame_appearance.raise_()
        elif Strings.SETTING_OTHER == data:
            self.__ui.frame_other.raise_()

    def __load_settings(self):
        self.__ui.comboBox_search_engine.setCurrentIndex(self.__setting.value('SearchEngine/index', 0))
        self.__ui.checkBox_search_suggestion.setChecked(self.__setting.value('SuggestionStatus', 1))
        self.__ui.comboBox_suggest_engine.setCurrentIndex(self.__setting.value('SuggestionEngine/index', 0))
        self.__ui.lineEdit_browser_path.setText(self.__setting.value('BrowserPath'))
        self.__ui.checkBox_private_mode.setChecked(self.__setting.value('PrivateMode', 0))
        if 1 == len(self.__setting.value('Hotkey/keys', 'caps_lock').split('+')):
            self.__ui.radioButton_single_key.setChecked(True)
            self.__ui.radioButton_single_key.click()
        else:
            self.__ui.radioButton_multiple_key.setChecked(True)
            self.__ui.radioButton_multiple_key.click()
        keys = self.__setting.value('Hotkey/keys', 'caps_lock')
        self.__ui.lineEdit_key_setting.setText(keys)
        self.__cur_hotkey = keys
        self.__ui.comboBox_press_times.setCurrentIndex(self.__setting.value('Hotkey/press_times/index', 0))
        self.__ui.comboBox_interval.setCurrentIndex(self.__setting.value('Hotkey/interval/index', 0))
        self.setStyleSheet(self.__setting.value('SettingDialogQss',
                                                '''QDialog, QDialog QFrame {
                                                background-color: #ffffff;
                                                }
                                                QDialog QTreeWidget {
                                                border: 0;
                                                border-right: 3px solid #f0f0f0;
                                                }'''))
        language_index = self.__setting.value('Language/index', 0)
        self.__ui.comboBox_language.setCurrentIndex(language_index)
        self.__cur_language = language_index
        self.__ui.comboBox_opacity.setCurrentIndex(self.__setting.value('Opacity/index', 0))
        no_sleep_status = self.__setting.value('NoSleepStatus', 0)
        self.__ui.checkBox_no_sleep.setChecked(no_sleep_status)
        self.__cur_no_sleep_status = no_sleep_status

    def __save_settings(self):
        self.__setting.setValue('SearchEngine/index', self.__ui.comboBox_search_engine.currentIndex())
        self.__setting.setValue('SearchEngine/data', self.__ui.comboBox_search_engine.currentData())
        self.__setting.setValue('SuggestionStatus', int(self.__ui.checkBox_search_suggestion.isChecked()))
        self.__setting.setValue('SuggestionEngine/index', self.__ui.comboBox_suggest_engine.currentIndex())
        self.__setting.setValue('SuggestionEngine/data', self.__ui.comboBox_suggest_engine.currentData())
        self.__setting.setValue('BrowserPath', self.__ui.lineEdit_browser_path.text())
        self.__setting.setValue('PrivateMode', int(self.__ui.checkBox_private_mode.isChecked()))
        self.__setting.setValue('Hotkey/keys', self.__ui.lineEdit_key_setting.text() or 'caps_lock')
        self.__setting.setValue('Hotkey/press_times/index', self.__ui.comboBox_press_times.currentIndex())
        self.__setting.setValue('Hotkey/press_times/data', int(self.__ui.comboBox_press_times.currentText()))
        self.__setting.setValue('Hotkey/interval/index', self.__ui.comboBox_interval.currentIndex())
        self.__setting.setValue('Hotkey/interval/data', float(self.__ui.comboBox_interval.currentText()))
        self.__setting.setValue('Language/index', self.__ui.comboBox_language.currentIndex())
        self.__setting.setValue('Language/data', self.__ui.comboBox_language.currentData())
        self.__setting.setValue('Opacity/index', self.__ui.comboBox_opacity.currentIndex())
        self.__setting.setValue('Opacity/data', float(self.__ui.comboBox_opacity.currentText()))
        self.__setting.setValue('NoSleepStatus', int(self.__ui.checkBox_no_sleep.isChecked()))

    def __select_file(self):
        from Strings import Strings
        filename = QFileDialog.getOpenFileName(parent=self, caption=Strings.SETTING_CHOOSE_BROWSER,
                                               filter='*.exe;*.sh')[0]
        if filename:
            self.__ui.lineEdit_browser_path.setText(filename)

    def __restore_default_settings(self):
        self.__setting.clear()
        self.__load_settings()

    def popup(self):
        self.__load_settings()
        self.__ui.treeWidget.clearSelection()
        self.__ui.frame_search.raise_()
        self.show()

    def __apply(self):
        self.__save_settings()
        self.setting_changed.emit({
            'hotkey': False if self.__cur_hotkey == self.__setting.value('Hotkey/keys', 'caps_lock') else True,
            'language': False if self.__cur_language == self.__setting.value('Language/index', 0) else True,
            'appearance': False,
            'sleep_status': False if self.__cur_no_sleep_status == self.__setting.value('NoSleepStatus', 0) else True
        })

    def __ok(self):
        self.__apply()
        self.hide()

    def __cancel(self):
        self.hide()

    def retranslate_ui(self):
        self.__ui.retranslateUi(self)

    def closeEvent(self, event):
        self.__ok()
        event.ignore()

    def keyPressEvent(self, event):
        key = event.key()
        if Qt.Key_Escape == key:
            self.closeEvent(event)