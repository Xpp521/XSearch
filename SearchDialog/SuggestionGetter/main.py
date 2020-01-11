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
from json import loads
from requests import RequestException
from requests.sessions import Session
from PyQt5.QtCore import QObject, pyqtSignal


class BaseSuggestionGetter(QObject):
    __signal = pyqtSignal(list)
    _api_map = {}

    def __init__(self, api=None, parent=None):
        super().__init__(parent)
        self.api = api
        self.__cached_data = {'': []}
        self._session = Session()
        self._session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, ' \
                                              'like Gecko) Chrome/65.0.3325.162 Safari/537.36 '

    def get(self, keyword):
        keyword = keyword.strip()
        suggestions = self.__cached_data.get(keyword)
        if suggestions is None:
            suggestions = self._get_from_network(keyword)
            suggestions = suggestions if isinstance(suggestions, list) else []
            if suggestions:
                self.__cached_data[keyword] = suggestions
        self.__signal.emit(suggestions)

    def _get_from_network(self, text):
        """
        :param text: keyword text.
        :return: suggestion list.
        :rtype: list.
        """
        raise NotImplementedError

    def clear_cache(self):
        self.__cached_data = {'': []}

    @property
    def cache_size(self):
        return sum([len(v) for v in self.__cached_data.values()])

    @property
    def api(self):
        return self._api

    @api.setter
    def api(self, api_name):
        self._api = api_name if self._api_map.get(api_name) else list(self._api_map.keys())[0]

    @property
    def api_list(self):
        return list(self._api_map.keys())

    @property
    def signal(self):
        return self.__signal


class KeywordSuggestionGetter(BaseSuggestionGetter):
    _api_map = {'360': 'https://sug.so.360.cn/suggest/word?',
                'baidu': '', 'sogou': ''}

    def __init__(self, api=None, parent=None):
        super().__init__(api, parent)

    def _get_from_network(self, text):
        li = []
        if '360' == self._api:
            li = self.__get_360_suggestions(text)
        elif 'baidu' == self._api:
            li = self.__get_baidu_suggestions(text)
        elif 'sogou' == self._api:
            li = self.__get_sogou_suggestions(text)
        return li

    def __get_360_suggestions(self, text):
        params = {'callback': 'suggest_so',
                  'encodein': 'utf-8',
                  'encodeout': 'utf-8',
                  'word': text,
                  '_jsonp': 'suggest_so'}
        try:
            r = self._session.get(self._api_map.get(self._api), params=params, timeout=3)
        except RequestException:
            return []
        if 200 == r.status_code:
            text = r.text
            p_index = text.find('p:')
            p = text[p_index + 2: text.find(',', p_index)]
            if 'true' in p:
                return loads(text[text.find('['): text.rfind(']') + 1])
        return []

    def __get_baidu_suggestions(self, text):
        params = {'wd': text}
        try:
            r = self._session.get(self._api_map.get(self._api), params=params, timeout=3)
        except RequestException:
            return []
        if 200 == r.status_code:
            json = r.json()
            if 'true' == json.get('p'):
                return json.get('s')
        return []

    def __get_sogou_suggestions(self, text):
        params = {'key': text}
        try:
            r = self._session.get(self._api_map.get(self._api), params=params, timeout=3)
        except RequestException:
            return []
        if 200 == r.status_code:
            json = r.json()
            if 'true' == json.get('p'):
                return json.get('s')
        return []


class URLSuggestionGetter(BaseSuggestionGetter):
    _api_map = {'360': 'https://sug.so.360.cn/suggest/word?'}

    def __init__(self, api=None, parent=None):
        super().__init__(api, parent)

    def _get_from_network(self, text):
        li = []
        if '360' == self._api:
            li = self.__get_360_suggestions(text)
        return li

    def __get_360_suggestions(self, text):
        params = {'word': text}
        try:
            r = self._session.get(self._api_map.get(self._api), params=params, timeout=3)
        except RequestException:
            return []
        if 200 == r.status_code:
            # parse html...
            return []
        return []
