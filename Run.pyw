from sys import argv
from main import XSearch
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(argv)
    app.setOrganizationName('Xpp')
    app.setOrganizationDomain('Xpp.com')
    app.setApplicationName('XSearch')
    search = XSearch()
    exit(app.exec_())
