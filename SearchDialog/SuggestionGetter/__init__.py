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
Usage:
    from PyQt5.QtCore import pyqtSignal
    from SuggestionGetter import keyword_suggestion_getter as getter


    class A:
        get_suggestion_signal = pyqtSignal(str)

        def __init__(self):
            self.get_suggestion_signal.connect(getter.get)
            getter.signal.connect(self.__show_suggestions)

        def get_suggestions(keyword):
            self.get_suggestion_signal.emit(keyword)

        def __show_suggestions(suggestions):
            print(suggestions)


    a = A()
    a.get_suggestions('keyword')
"""
from .main import KeywordSuggestionGetter as __KeywordSuggestionGetter, URLSuggestionGetter as __URLSuggestionGetter
from PyQt5.QtCore import QThread as __QThread
__thread = __QThread()
__thread.start()
keyword_suggestion_getter = __KeywordSuggestionGetter()
keyword_suggestion_getter.moveToThread(__thread)
url_suggestion_getter = __URLSuggestionGetter()
url_suggestion_getter.moveToThread(__thread)
