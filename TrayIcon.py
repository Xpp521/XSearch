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
        self.action_show = QAction('显示界面', menu)
        self.action_setting = QAction('设置', menu)
        action_separator = QAction(menu)
        action_separator.setSeparator(True)
        menu.addActions((self.action_show, self.action_setting,
                         action_separator, QAction('退出', menu, triggered=QApplication.instance().quit)))
        menu.setStyleSheet(self.qss)
        self.setContextMenu(menu)
        self.__cursor = QCursor()
        self.activated.connect(lambda: menu.popup(self.__cursor.pos()))
        self.setIcon(QIcon('Leaf.ico'))
        self.setToolTip('XSearch')
