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
from time import time
from re import findall
from json import loads
from hashlib import md5
from random import random
from PyQt5.QtCore import QThread
from requests import RequestException
from requests.sessions import Session
from PyQt5.QtCore import QObject, pyqtSignal


class BaseGetter(QObject):
    __signal = pyqtSignal(list)

    def __init__(self, thread=None):
        super().__init__()
        self.__cached_data = {'': []}
        self.__thread = thread
        if not isinstance(thread, QThread):
            self.__thread = QThread()
            self.__thread.start()
        self.moveToThread(self.__thread)

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

    @property
    def thread(self):
        return self.__thread


class WebGetter(BaseGetter):
    @property
    def _provider_map(self):
        raise NotImplementedError

    def __init__(self, provider=None, timeout=None, thread=None):
        super().__init__(thread)
        self._session = Session()
        self._session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, ' \
                                              'like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        self.timeout = timeout
        self.provider = provider

    def _custom_get(self, text):
        raise NotImplementedError

    @property
    def provider(self):
        return self._provider

    @provider.setter
    def provider(self, p):
        self._provider = p if self._provider_map.get(p) else list(self._provider_map.keys())[0]
        self._api = self._provider_map.get(self._provider)

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, t):
        self._timeout = t if isinstance(t, (float, int)) and 1 < t < 5 else 3


class KeywordGetter(WebGetter):
    QH360 = 0
    BAIDU = 1
    SOGOU = 2
    DOGEDOGE = 3
    GOOGLE = 5

    @property
    def _provider_map(self):
        return {self.QH360: 'https://sug.so.360.cn/suggest/word?',
                self.BAIDU: '',
                self.SOGOU: '',
                self.DOGEDOGE: 'https://www.dogedoge.com/sugg/',
                self.GOOGLE: 'http://suggestqueries.google.com/complete/search?'}

    def __init__(self, provider=None, timeout=None, thread=None):
        super().__init__(provider, timeout, thread)

    def _custom_get(self, text):
        li = []
        if self.QH360 == self._provider:
            li = self.__get_360(text)
        elif self.BAIDU == self._provider:
            li = self.__get_baidu(text)
        elif self.SOGOU == self._provider:
            li = self.__get_sogou(text)
        elif self.DOGEDOGE == self._provider:
            li = self.__get_dogedoge(text)
        elif self.GOOGLE == self._provider:
            li = self.__get_google(text)
        return li

    def __get_360(self, text):
        params = {'callback': 'suggest_so',
                  'encodein': 'utf-8',
                  'encodeout': 'utf-8',
                  'word': text,
                  '_jsonp': 'suggest_so'}
        try:
            r = self._session.get(self._api, params=params, timeout=self._timeout)
        except RequestException:
            return []
        if 200 == r.status_code:
            text = r.text
            p_index = text.find('p:')
            p = text[p_index + 2: text.find(',', p_index)]
            if 'true' in p:
                return loads(text[text.find('['): text.rfind(']') + 1])
        return []

    def __get_baidu(self, text):
        params = {'wd': text}
        try:
            r = self._session.get(self._api, params=params, timeout=self._timeout)
        except RequestException:
            return []
        if 200 == r.status_code:
            return []
        return []

    def __get_sogou(self, text):
        params = {'key': text}
        try:
            r = self._session.get(self._api, params=params, timeout=self._timeout)
        except RequestException:
            return []
        if 200 == r.status_code:
            return []
        return []

    def __get_dogedoge(self, text):
        try:
            r = self._session.get('{}{}'.format(self._api, text), timeout=self._timeout)
        except RequestException:
            return []
        if 200 == r.status_code:
            return [s.replace('</span>', '') for s in findall(r't-normal">(.*?)</d', r.text)]
        return []

    def __get_google(self, text):
        params = {'client': 'firefox', 'q': text}
        try:
            r = self._session.get(self._api, params=params, timeout=self._timeout)
        except RequestException:
            return []
        if 200 == r.status_code:
            return r.json()[1]
        return []

    @property
    def provider(self):
        return self._provider

    @provider.setter
    def provider(self, p):
        self._provider = p if self._provider_map.get(p) else list(self._provider_map.keys())[0]
        self._api = self._provider_map.get(self._provider)
        self._custom_get('')


#       Extra features
# ↓↓↓ Waiting to be done ↓↓↓
class TranslationGetter(WebGetter):
    YOUDAO = 0
    BAIDU = 1
    GOOGLE = 2

    @property
    def _provider_map(self):
        return {self.YOUDAO: 'http://fanyi.youdao.com/translate_o',
                self.BAIDU: 'https://fanyi.baidu.com/v2transapi',
                self.GOOGLE: ''}

    def __init__(self, provider=None, timeout=None, thread=None):
        super().__init__(provider, timeout, thread)
        self.__source = None
        self.__target = None

    def _custom_get(self, text):
        li = []
        if self.YOUDAO == self._provider:
            li = self.__get_youdao(text)
        elif self.BAIDU == self._provider:
            li = self.__get_baidu(text)
        elif self.GOOGLE == self._provider:
            li = self.__get_google(text)
        return li

    def __get_youdao(self, text):
        # Algorithm source：http://shared.ydstatic.com/fanyi/newweb/v1.0.20/scripts/newweb/fanyi.min.js
        t = md5(self._session.headers.get('User-Agent').encode()).hexdigest()
        r = str(int(time() * 1000))
        i = '{}{}'.format(r, int(10 * random()))
        self._data['i'] = text
        self._data['salt'] = i
        self._data['sign'] = md5('fanyideskweb{}{}n%A-rKaT5fb[Gy?;N5@Tj'.format(text, i).encode()).hexdigest()
        self._data['ts'] = r
        self._data['bv'] = t
        try:
            r = self._session.post(self._api, data=self._data, timeout=self._timeout)
        except Exception:
            return []
        if 200 == r.status_code:
            json = r.json()
            if 0 == json.get('errorCode'):
                return [json.get('translateResult')[0][0].get('tgt')]
        return []

    def __get_baidu(self, text):
        return []

    def __get_google(self, text):
        return []

    @property
    def provider(self):
        return self._provider

    @provider.setter
    def provider(self, p):
        self._provider = p if self._provider_map.get(p) else list(self._provider_map.keys())[0]
        self._api = self._provider_map.get(self._provider)
        if self.YOUDAO == self._provider:
            self._data = {'smartresult': 'dict', 'client': 'fanyideskweb', 'doctype': 'json', 'version': '2.1',
                          'keyfrom': 'fanyi.web', 'action': 'FY_BY_REALTlME',
                          'from': self.__source, 'to': self.__target}
            self._session.headers['Referer'] = 'http://fanyi.youdao.com/'
        elif self.BAIDU == self._provider:
            self._data = {}
        elif self.GOOGLE == self._provider:
            self._data = {}
        self._custom_get('')

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, s):
        self.__source = s

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, t):
        self.__target = t


class CalculationGetter(BaseGetter):
    def __init__(self, thread=None):
        super().__init__(thread)

    def _custom_get(self, text):
        pass
