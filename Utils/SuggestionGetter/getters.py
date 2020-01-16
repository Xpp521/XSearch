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
from re import findall
from json import loads
from PyQt5.QtCore import QThread
from requests import RequestException
from requests.sessions import Session
from PyQt5.QtCore import QObject, pyqtSignal

_thread = QThread()
_thread.start()


class BaseGetter(QObject):
    __signal = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__cached_data = {'': []}
        self.moveToThread(_thread)

    def get(self, keyword):
        keyword = keyword.strip()
        suggestions = self.__cached_data.get(keyword)
        if suggestions is None:
            suggestions = self._custom_get(keyword)
            suggestions = suggestions if isinstance(suggestions, list) else []
            if suggestions:
                self.__cached_data[keyword] = suggestions
        self.__signal.emit(suggestions)

    def _custom_get(self, text):
        raise NotImplementedError

    def clear_cache(self):
        self.__cached_data = {'': []}

    @property
    def cache_count(self):
        return sum([len(v) for v in self.__cached_data.values()])

    @property
    def signal(self):
        return self.__signal


class WebGetter(BaseGetter):
    def __init__(self, api=None, parent=None):
        super().__init__(parent)
        self.__api_map = {self.QH360: 'https://sug.so.360.cn/suggest/word?',
                          self.BAIDU: '',
                          self.SOGOU: '',
                          self.DOGEDOGE: 'https://www.dogedoge.com/sugg/'}
        self.api = api
        self._session = Session()
        self._session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, ' \
                                              'like Gecko) Chrome/65.0.3325.162 Safari/537.36'

    def _custom_get(self, text):
        li = []
        if self.QH360 == self.__api:
            li = self.__get_360_suggestions(text)
        elif self.BAIDU == self.__api:
            li = self.__get_baidu_suggestions(text)
        elif self.SOGOU == self.__api:
            li = self.__get_sogou_suggestions(text)
        elif self.DOGEDOGE == self.__api:
            li = self.__get_dogedoge_suggestions(text)
        return li

    def __get_360_suggestions(self, text):
        params = {'callback': 'suggest_so',
                  'encodein': 'utf-8',
                  'encodeout': 'utf-8',
                  'word': text,
                  '_jsonp': 'suggest_so'}
        try:
            r = self._session.get(self.__api_map.get(self.__api), params=params, timeout=3)
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
            r = self._session.get(self.__api_map.get(self.__api), params=params, timeout=3)
        except RequestException:
            return []
        if 200 == r.status_code:
            return []
        return []

    def __get_sogou_suggestions(self, text):
        params = {'key': text}
        try:
            r = self._session.get(self.__api_map.get(self.__api), params=params, timeout=3)
        except RequestException:
            return []
        if 200 == r.status_code:
            return []
        return []

    def __get_dogedoge_suggestions(self, text):
        try:
            r = self._session.get('{}{}'.format(self.__api_map.get(self.__api), text), timeout=3)
        except RequestException:
            return []
        if 200 == r.status_code:
            return [s.replace('</span>', '') for s in findall(r't-normal">(.*?)</d', r.text)]
        return []

    @property
    def api(self):
        return self.__api

    @api.setter
    def api(self, api_name):
        self.__api = api_name if self.__api_map.get(api_name) else self.QH360

    QH360 = 0
    BAIDU = 1
    SOGOU = 2
    DOGEDOGE = 3
    GOOGLE = 5


#       Extra features
# ↓↓↓ Waiting to be done ↓↓↓
class LocalFileGetter(BaseGetter):
    def __init__(self, parent=None):
        super().__init__(parent)

    def _custom_get(self, text):
        pass


class TranslationGetter(BaseGetter):
    def __init__(self, parent=None):
        super().__init__(parent)

    def _custom_get(self, text):
        pass


class CalculationGetter(BaseGetter):
    def __init__(self, parent=None):
        super().__init__(parent)

    def _custom_get(self, text):
        pass
