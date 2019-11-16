from sys import argv
from main import XSearch
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(argv)
    search = XSearch()
    exit(app.exec_())
