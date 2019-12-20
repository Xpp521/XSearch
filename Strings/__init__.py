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
"""
This module will automatically import "Strings" according to the setting.
If the setting doesn't exist, use the system default language.
"""
from PyQt5.QtCore import QSettings
from locale import getdefaultlocale
from importlib import import_module
# QSettings().clear()
lang = QSettings().value('Language/data')
if lang:
    module = import_module('.Strings_{}'.format(lang), 'Strings')
    from . import module as Strings
else:
    if 'zh_cn' in getdefaultlocale()[0].lower():
        from . import Strings_cn as Strings
    else:
        from . import Strings_en as Strings
