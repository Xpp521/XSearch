# -*- coding: utf-8 -*-
# @Time    : 2019/12/2 15:35
# @Author  : Xpp
# @Email   : Xpp233@foxmail.com
"""
Usage:
    from SuggestionGetter import keyword_suggestion_getter
    keyword_suggestion_getter.signal.connect(func)

    def func(suggestions):
        print(suggestions)

    # get suggestions
    keyword_suggestion_getter.get('keyword')

    # clear cached data
    keyword_suggestion_getter.clear_cache()
"""
from .__main import KeywordSuggestionGetter as __KeywordSuggestionGetter, URLSuggestionGetter as __URLSuggestionGetter
from PyQt5.QtCore import QThread as __QThread

__thread = __QThread()
__thread.start()
keyword_suggestion_getter = __KeywordSuggestionGetter()
keyword_suggestion_getter.moveToThread(__thread)
url_suggestion_getter = __URLSuggestionGetter()
url_suggestion_getter.moveToThread(__thread)
