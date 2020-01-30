# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Xpp521
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
    from SuggestionGetter import WebGetter


    class A:
        suggestion_signal = pyqtSignal(str)

        def __init__(self):
            getter = WebGetter()

            # switch suggestion provider
            getter.api = WebGetter.GOOGLE

            # bind the signal to be emitted
            self.suggestion_signal.connect(getter.get)

            # bind callback function
            getter.signal.connect(self.__show_suggestions)

        def get_suggestions(keyword):
            self.suggestion_signal.emit(keyword)

        def __show_suggestions(suggestions):
            print(suggestions)


    a = A()
    a.get_suggestions('keyword')
"""
from .getters import WebGetter
