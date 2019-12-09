from os.path import join
from PyQt5.QtCore import Qt
from PyQt5.Qt import QCursor
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QAction, QMenu, QSystemTrayIcon


class TrayIcon(QSystemTrayIcon):
    qss = '''QMenu {
                     font: 17px;
                     background-color: white;
                     padding:3px 3px;
                     border: 1px solid grey;
                     border-radius: 5px;
                 }
                 QMenu::item {
                     border-radius: 5px;
                     background-color: transparent;
                     padding:8px 32px;
                     margin:1px 1px;
                     /* border-bottom:1px solid #DBDBDB; */
                 }
                 QMenu::item:selected {
                     /* background-color: #2dabf9; */
                     background-color: lightgrey;
                 }'''

    def __init__(self):
        super().__init__()
        menu = QMenu()
        menu.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        menu.setAttribute(Qt.WA_TranslucentBackground)
        action_show = QAction(menu)
        action_setting = QAction(menu)
        action_separator = QAction(menu)
        action_separator.setSeparator(True)
        action_exit = QAction(menu, triggered=QApplication.instance().quit)
        self.actions = {'search': action_show, 'setting': action_setting, 'exit': action_exit}
        menu.addActions((action_show, action_setting, action_separator, action_exit))
        menu.setStyleSheet(self.qss)
        self.setContextMenu(menu)
        self.__cursor = QCursor()
        self.activated.connect(lambda: menu.popup(self.__cursor.pos()))
        self.setIcon(QIcon(join('Icons', 'XSearch.ico')))
        self.retranslate_ui()

    def set_action_handler(self, action_name, handler):
        action = self.actions.get(action_name)
        if isinstance(action, QAction) and callable(handler):
            action.triggered.connect(handler)
            return True
        return False

    def retranslate_ui(self):
        from Strings import Strings
        self.setToolTip(Strings.APP_NAME)
        self.actions.get('search').setText(Strings.TRAY_SEARCH)
        self.actions.get('setting').setText(Strings.TRAY_SETTING)
        self.actions.get('exit').setText(Strings.TRAY_EXIT)
