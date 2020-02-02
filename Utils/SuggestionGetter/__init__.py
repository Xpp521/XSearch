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
    from SuggestionGetter import KeywordGetter


    class A:
        signal = pyqtSignal(str)

        def __init__(self):
            self.getter = KeywordGetter()

            # Bind the signal to be emitted
            self.signal.connect(self.getter.get)

            # Bind callback function
            self.getter.signal.connect(lambda li: print(li))

        def get_suggestions(keyword):
            self.signal.emit(keyword)


    a = A()

    # Query keyword suggestions
    a.get_suggestions('China')

    # Clear suggestion cache
    a.getter.clear_cache()

    # Switch suggestion provider
    a.getter.provider = KeywordGetter.GOOGLE
"""
from .getters import KeywordGetter
