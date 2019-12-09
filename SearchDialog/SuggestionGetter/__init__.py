# -*- coding: utf-8 -*-
# @Time    : 2019/12/2 15:35
# @Author  : Xpp
# @Email   : Xpp233@foxmail.com
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
