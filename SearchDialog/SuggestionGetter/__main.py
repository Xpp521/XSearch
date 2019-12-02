# -*- coding: utf-8 -*-
# @Time    : 2019/11/26 13:10
# @Author  : Xpp
# @Email   : Xpp233@foxmail.com
from json import loads
from requests import RequestException
from requests.sessions import Session
from PyQt5.QtCore import QObject, pyqtSignal


class KeywordSuggestionGetter(QObject):
    signal = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__api = 'https://sug.so.360.cn/suggest/word?'
        self.__cached_data = {'': []}
        self.__session = Session()
        self.__session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, ' \
                                               'like Gecko) Chrome/65.0.3325.162 Safari/537.36 '

    def get(self, keyword):
        keyword = keyword.strip()
        r = self.__cached_data.get(keyword)
        if r is not None:
            self.signal.emit(r)
        else:
            self.signal.emit(self.__get_from_network(keyword))

    def __get_from_network(self, text):
        li = []
        if '360' in self.__api:
            li = self.__get_360_suggestion(text)
        elif 'baidu' in self.__api:
            li = self.__get_baidu_suggestion(text)
        elif 'sogou' in self.__api:
            li = self.__get_sogou_suggestion(text)
        if li:
            self.__cached_data[text] = li
        return li

    def __get_360_suggestion(self, text):
        params = {'callback': 'suggest_so',
                  'encodein': 'utf-8',
                  'encodeout': 'utf-8',
                  'word': text,
                  '_jsonp': 'suggest_so'}
        try:
            r = self.__session.get(self.__api, params=params)
        except RequestException:
            return []
        if 200 == r.status_code:
            text = r.text
            p_index = text.find('p:')
            p = text[p_index + 2: text.find(',', p_index)]
            if 'true' in p:
                return loads(text[text.find('['): text.rfind(']') + 1])
        return []

    def __get_baidu_suggestion(self, text):
        params = {'wd': text}
        try:
            r = self.__session.get(self.__api, params=params)
        except RequestException:
            return []
        if 200 == r.status_code:
            json = r.json()
            if 'true' == json.get('p'):
                return json.get('s')
        return []

    def __get_sogou_suggestion(self, text):
        params = {'key': text}
        try:
            r = self.__session.get(self.__api, params=params)
        except RequestException:
            return []
        if 200 == r.status_code:
            json = r.json()
            if 'true' == json.get('p'):
                return json.get('s')
        return []

    def clear_cache(self):
        self.__cached_data.clear()

    @property
    def api(self):
        return self.__api

    @api.setter
    def api(self, value):
        self.__api = value if value else 'https://sug.so.360.cn/suggest/word?'


class URLSuggestionGetter(QObject):
    signal = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__api = 'https://sug.so.360.cn/suggest/word?'
        self.__cached_data = {'': []}
        self.__session = Session()
        self.__session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, ' \
                                               'like Gecko) Chrome/65.0.3325.162 Safari/537.36 '

    def get(self, url):
        url = url.strip()
        r = self.__cached_data.get(url)
        if r is not None:
            self.signal.emit(r)
        else:
            self.signal.emit(self.__get_from_network(url))

    def __get_from_network(self, url):
        li = []
        return li

    def clear_cache(self):
        self.__cached_data.clear()

    @property
    def api(self):
        return self.__api

    @api.setter
    def api(self, value):
        self.__api = value if value else 'https://sug.so.360.cn/suggest/word?'

