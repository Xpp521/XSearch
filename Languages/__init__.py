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
"""
This module contains all the strings that appear in the program.


Usage:
    from sys import modules
    from PyQt5.QtCore import QSettings
    from PyQt5.QtWidgets import QDialog


    class MyDialog(QDialog)

        def __init__(self)
            super().__init__()
            self.translate_ui()

        def translate_ui(self):
            # Module must be imported inside your method
            from Languages import Strings

            # Translate ui with strings in the module
            self.setWindowTitle(Strings.APP_NAME)
            ...

        @staticmethod
        def show_language_map():
            from Languages import language_map
            print(language_map)

        def switch_language(self, lang):
            # Set new language
            QSetting().setValue('Language', lang)

            # Pop "Language" module
            modules.pop('Languages')

            # Re translation ui
            self.translate_ui()
"""
from json import load
from os.path import join, dirname
from PyQt5.QtCore import QSettings
from locale import getdefaultlocale
from importlib import import_module
language_map = load(open(join(dirname(__file__), 'map.json'), encoding='utf'))
lang = QSettings().value('Language')
if lang:
    module = import_module('.Strings_{}'.format(lang), 'Languages')
    from . import module as Strings
else:
    # If language setting doesn't exist, use the system default language.
    if 'zh_cn' in getdefaultlocale()[0].lower():
        from . import Strings_cn as Strings
    else:
        from . import Strings_en as Strings
