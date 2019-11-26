# -*- coding: utf-8 -*-
# @Time    : 2019/11/25 14:09
# @Author  : Xpp
# @Email   : Xpp233@foxmail.com
"""
This module will automatically import "Strings" according to the setting.
If the setting doesn't exist, use the system default language.
"""
from PyQt5.QtCore import QSettings
from locale import getdefaultlocale
from importlib import import_module
lang = QSettings().value('language/data')
if lang:
    module = import_module('.Strings_{}'.format(lang), 'Strings')
    from . import module as Strings
else:
    if 'zh_cn' in getdefaultlocale()[0].lower():
        from . import Strings_cn as Strings
    else:
        from . import Strings_en as Strings
