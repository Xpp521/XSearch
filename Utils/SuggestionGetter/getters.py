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
        self._timeout = t if isinstance(t, (float, int)) and 1 < t < 5 else 2


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
        return {
            self.YOUDAO: 'http://fanyi.youdao.com/translate_o',
            self.BAIDU: 'https://fanyi.baidu.com/v2transapi',
            self.GOOGLE: 'https://translate.google.cn/translate_a/single',
        }

    def __init__(self, provider=None, timeout=None, thread=None):
        self.__language_list = {}
        self.__language_map = {}
        self.__source = ''
        self.__target = ''
        super().__init__(provider, timeout, thread)

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
        self._data['from'] = self.__source
        self._data['to'] = self.__target
        try:
            r = self._session.post(self._api, data=self._data, timeout=self._timeout)
        except RequestException:
            return []
        if 200 == r.status_code:
            json = r.json()
            print('errorCode: {}'.format(json.get('errorCode')))
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
            self.__language_list = {
                'ar': '阿拉伯语', 'de': '德语', 'en': '英语', 'es': '西班牙语', 'fr': '法语', 'id': '印尼语', 'it': '意大利语',
                'ja': '日语', 'ko': '韩语', 'pt': '葡萄牙语', 'ru': '俄语', 'vi': '越南语', 'zh-CHS': '中文', 'AUTO': '自动'
            }
            self.__language_map = {
                'AUTO': ['AUTO'], 'en': ['zh-CHS'], 'ja': ['zh-CHS'], 'ko': ['zh-CHS'], 'fr': ['zh-CHS'],
                'de': ['zh-CHS'], 'ru': ['zh-CHS'], 'es': ['zh-CHS'], 'pt': ['zh-CHS'], 'it': ['zh-CHS'],
                'vi': ['zh-CHS'], 'id': ['zh-CHS'], 'ar': ['zh-CHS'],
                'zh-CHS': ['en', 'ja', 'ko', 'fr', 'de', 'ru', 'es', 'pt', 'it', 'vi', 'id', 'ar'],
            }
            self._data = {'smartresult': 'dict', 'client': 'fanyideskweb', 'doctype': 'json', 'version': '2.1',
                          'keyfrom': 'fanyi.web', 'action': 'FY_BY_REALTlME'}
            try:
                self._session.get('http://fanyi.youdao.com/', timeout=self._timeout)
            except RequestException:
                pass
            self._session.headers['Referer'] = 'http://fanyi.youdao.com/'
        elif self.BAIDU == self._provider:
            self.__language_list = {
                'zh': '中文', 'jp': '日语', 'jpka': '日语假名', 'th': '泰语', 'fra': '法语', 'en': '英语', 'spa': '西班牙语',
                'kor': '韩语', 'tr': '土耳其语', 'vie': '越南语', 'ms': '马来语', 'de': '德语', 'ru': '俄语', 'ir': '伊朗语',
                'ara': '阿拉伯语', 'est': '爱沙尼亚语', 'be': '白俄罗斯语', 'bul': '保加利亚语', 'hi': '印地语', 'is': '冰岛语',
                'pl': '波兰语', 'fa': '波斯语', 'dan': '丹麦语', 'tl': '菲律宾语', 'fin': '芬兰语', 'nl': '荷兰语',
                'ca': '加泰罗尼亚语', 'cs': '捷克语', 'hr': '克罗地亚语', 'lv': '拉脱维亚语', 'lt': '立陶宛语',
                'rom': '罗马尼亚语', 'af': '南非语', 'no': '挪威语', 'pt_BR': '巴西语', 'pt': '葡萄牙语', 'swe': '瑞典语',
                'sr': '塞尔维亚语', 'eo': '世界语', 'sk': '斯洛伐克语', 'slo': '斯洛文尼亚语', 'sw': '斯瓦希里语',
                'uk': '乌克兰语', 'iw': '希伯来语', 'el': '希腊语', 'hu': '匈牙利语', 'hy': '亚美尼亚语', 'it': '意大利语',
                'id': '印尼语', 'sq': '阿尔巴尼亚语', 'am': '阿姆哈拉语', 'as': '阿萨姆语', 'az': '阿塞拜疆语', 'eu': '巴斯克语',
                'bn': '孟加拉语', 'bs': '波斯尼亚语', 'gl': '加利西亚语', 'ka': '格鲁吉亚语', 'gu': '古吉拉特语', 'ha': '豪萨语',
                'ig': '伊博语', 'iu': '因纽特语', 'ga': '爱尔兰语', 'zu': '祖鲁语', 'kn': '卡纳达语', 'kk': '哈萨克语',
                'ky': '吉尔吉斯语', 'lb': '卢森堡语', 'mk': '马其顿语', 'mt': '马耳他语', 'mi': '毛利语', 'mr': '马拉提语',
                'ne': '尼泊尔语', 'or': '奥利亚语', 'pa': '旁遮普语', 'qu': '凯楚亚语', 'tn': '塞茨瓦纳语', 'si': '僧加罗语',
                'ta': '泰米尔语', 'tt': '塔塔尔语', 'te': '泰卢固语', 'ur': '乌尔都语', 'uz': '乌兹别克语', 'cy': '威尔士语',
                'yo': '约鲁巴语', 'yue': '粤语', 'wyw': '文言文', 'cht': '中文繁体'
            }
            self.__language_map = {
                'zh': ['en', 'ara', 'est', 'bul', 'pl', 'dan', 'de', 'ru', 'fra', 'fin', 'kor', 'nl', 'cs', 'rom', 'pt',
                       'jp', 'swe', 'slo', 'th', 'wyw', 'spa', 'el', 'hu', 'it', 'yue', 'cht', 'vie'],
                'en': ['zh', 'ara', 'est', 'bul', 'pl', 'dan', 'de', 'ru', 'fra', 'fin', 'kor', 'nl', 'cs', 'rom', 'pt',
                       'jp', 'swe', 'slo', 'th', 'wyw', 'spa', 'el', 'hu', 'it', 'yue', 'cht', 'vie'],
                'ara': ['zh', 'en', 'est', 'bul', 'pl', 'dan', 'de', 'ru', 'fra', 'fin', 'kor', 'nl', 'cs', 'rom', 'pt',
                        'jp', 'swe', 'slo', 'th', 'wyw', 'spa', 'el', 'hu', 'it', 'yue', 'cht', 'vie'],
                'est': ['zh', 'en', 'ara', 'bul', 'pl', 'dan', 'de', 'ru', 'fra', 'fin', 'kor', 'nl', 'cs', 'rom', 'pt',
                        'jp', 'swe', 'slo', 'th', 'wyw', 'spa', 'el', 'hu', 'it', 'yue', 'cht', 'vie'],
                'bul': ['zh', 'en', 'ara', 'est', 'pl', 'dan', 'de', 'ru', 'fra', 'fin', 'kor', 'nl', 'cs', 'rom', 'pt',
                        'jp', 'swe', 'slo', 'th', 'wyw', 'spa', 'el', 'hu', 'it', 'yue', 'cht', 'vie'],
                'pl': ['zh', 'en', 'ara', 'est', 'bul', 'dan', 'de', 'ru', 'fra', 'fin', 'kor', 'nl', 'cs', 'rom', 'pt',
                       'jp', 'swe', 'slo', 'th', 'wyw', 'spa', 'el', 'hu', 'it', 'yue', 'cht', 'vie'],
                'dan': ['zh', 'en', 'ara', 'est', 'bul', 'pl', 'de', 'ru', 'fra', 'fin', 'kor', 'nl', 'cs', 'rom', 'pt',
                        'jp', 'swe', 'slo', 'th', 'wyw', 'spa', 'el', 'hu', 'it', 'yue', 'cht', 'vie'],
                'de': ['zh', 'en', 'ara', 'est', 'bul', 'pl', 'dan', 'ru', 'fra', 'fin', 'kor', 'nl', 'cs', 'rom', 'pt',
                       'jp', 'swe', 'slo', 'th', 'wyw', 'spa', 'el', 'hu', 'it', 'yue', 'cht', 'vie'],
                'ru': ['zh', 'en', 'ara', 'est', 'bul', 'pl', 'dan', 'de', 'fra', 'fin', 'kor', 'nl', 'cs', 'rom', 'pt',
                       'jp', 'swe', 'slo', 'th', 'wyw', 'spa', 'el', 'hu', 'it', 'yue', 'cht', 'vie'],
                'fra': ['zh', 'en', 'ara', 'est', 'bul', 'pl', 'dan', 'de', 'ru', 'fin', 'kor', 'nl', 'cs', 'rom', 'pt',
                        'jp', 'swe', 'slo', 'th', 'wyw', 'spa', 'el', 'hu', 'it', 'yue', 'cht', 'vie'],
                'fin': ['zh', 'en', 'ara', 'est', 'bul', 'pl', 'dan', 'de', 'ru', 'fra', 'kor', 'nl', 'cs', 'rom', 'pt',
                        'jp', 'swe', 'slo', 'th', 'wyw', 'spa', 'el', 'hu', 'it', 'yue', 'cht', 'vie'],
                'kor': ['zh', 'en', 'ara', 'est', 'bul', 'pl', 'dan', 'de', 'ru', 'fra', 'fin', 'nl', 'cs', 'rom', 'pt',
                        'jp', 'swe', 'slo', 'th', 'wyw', 'spa', 'el', 'hu', 'it', 'yue', 'cht', 'vie'],
                'nl': ['zh', 'en', 'ara', 'est', 'bul', 'pl', 'dan', 'de', 'ru', 'fra', 'fin', 'kor', 'cs', 'rom', 'pt',
                       'jp', 'swe', 'slo', 'th', 'wyw', 'spa', 'el', 'hu', 'it', 'yue', 'cht', 'vie'],
                'cs': ['zh', 'en', 'ara', 'est', 'bul', 'pl', 'dan', 'de', 'ru', 'fra', 'fin', 'kor', 'nl', 'rom', 'pt',
                       'jp', 'swe', 'slo', 'th', 'wyw', 'spa', 'el', 'hu', 'it', 'yue', 'cht', 'vie'],
                'rom': ['zh', 'en', 'ara', 'est', 'bul', 'pl', 'dan', 'de', 'ru', 'fra', 'fin', 'kor', 'nl', 'cs', 'pt',
                        'jp', 'swe', 'slo', 'th', 'wyw', 'spa', 'el', 'hu', 'it', 'yue', 'cht', 'vie'],
                'pt': ['zh', 'en', 'ara', 'est', 'bul', 'pl', 'dan', 'de', 'ru', 'fra', 'fin', 'kor', 'nl', 'cs', 'rom',
                       'jp', 'swe', 'slo', 'th', 'wyw', 'spa', 'el', 'hu', 'it', 'yue', 'cht', 'vie'],
                'jp': ['zh', 'en', 'ara', 'est', 'bul', 'pl', 'dan', 'de', 'ru', 'fra', 'fin', 'kor', 'nl', 'cs', 'rom',
                       'pt', 'swe', 'slo', 'th', 'wyw', 'spa', 'el', 'hu', 'it', 'yue', 'cht', 'jpka', 'vie'],
                'swe': ['zh', 'en', 'ara', 'est', 'bul', 'pl', 'dan', 'de', 'ru', 'fra', 'fin', 'kor', 'nl', 'cs',
                        'rom', 'pt', 'jp', 'slo', 'th', 'wyw', 'spa', 'el', 'hu', 'it', 'yue', 'cht', 'vie'],
                'slo': ['zh', 'en', 'ara', 'est', 'bul', 'pl', 'dan', 'de', 'ru', 'fra', 'fin', 'kor', 'nl', 'cs',
                        'rom', 'pt', 'jp', 'swe', 'th', 'wyw', 'spa', 'el', 'hu', 'it', 'yue', 'cht', 'vie'],
                'th': ['zh', 'en', 'ara', 'est', 'bul', 'pl', 'dan', 'de', 'ru', 'fra', 'fin', 'kor', 'nl', 'cs', 'rom',
                       'pt', 'jp', 'swe', 'slo', 'wyw', 'spa', 'el', 'hu', 'it', 'yue', 'cht', 'vie'],
                'wyw': ['zh', 'en', 'ara', 'est', 'bul', 'pl', 'dan', 'de', 'ru', 'fra', 'fin', 'kor', 'nl', 'cs',
                        'rom', 'pt', 'jp', 'swe', 'slo', 'th', 'spa', 'el', 'hu', 'it', 'yue', 'cht', 'vie'],
                'spa': ['zh', 'en', 'ara', 'est', 'bul', 'pl', 'dan', 'de', 'ru', 'fra', 'fin', 'kor', 'nl', 'cs',
                        'rom', 'pt', 'jp', 'swe', 'slo', 'th', 'wyw', 'el', 'hu', 'it', 'yue', 'cht', 'vie'],
                'el': ['zh', 'en', 'ara', 'est', 'bul', 'pl', 'dan', 'de', 'ru', 'fra', 'fin', 'kor', 'nl', 'cs', 'rom',
                       'pt', 'jp', 'swe', 'slo', 'th', 'wyw', 'spa', 'hu', 'it', 'yue', 'cht', 'vie'],
                'hu': ['zh', 'en', 'ara', 'est', 'bul', 'pl', 'dan', 'de', 'ru', 'fra', 'fin', 'kor', 'nl', 'cs', 'rom',
                       'pt', 'jp', 'swe', 'slo', 'th', 'wyw', 'spa', 'el', 'it', 'yue', 'cht', 'vie'],
                'it': ['zh', 'en', 'ara', 'est', 'bul', 'pl', 'dan', 'de', 'ru', 'fra', 'fin', 'kor', 'nl', 'cs', 'rom',
                       'pt', 'jp', 'swe', 'slo', 'th', 'wyw', 'spa', 'el', 'hu', 'yue', 'cht', 'vie'],
                'yue': ['zh', 'en', 'ara', 'est', 'bul', 'pl', 'dan', 'de', 'ru', 'fra', 'fin', 'kor', 'nl', 'cs',
                        'rom', 'pt', 'jp', 'swe', 'slo', 'th', 'wyw', 'spa', 'el', 'hu', 'it', 'cht', 'vie'],
                'cht': ['zh', 'en', 'ara', 'est', 'bul', 'pl', 'dan', 'de', 'ru', 'fra', 'fin', 'kor', 'nl', 'cs',
                        'rom', 'pt', 'jp', 'swe', 'slo', 'th', 'wyw', 'spa', 'el', 'hu', 'it', 'yue', 'vie'],
                'vie': ['zh', 'en', 'ara', 'est', 'bul', 'pl', 'dan', 'de', 'ru', 'fra', 'fin', 'kor', 'nl', 'cs',
                        'rom', 'pt', 'jp', 'swe', 'slo', 'th', 'wyw', 'spa', 'el', 'hu', 'it', 'yue', 'cht']
            }
            self._data = {}
        elif self.GOOGLE == self._provider:
            self._data = {}
        self._custom_get('test')

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, s):
        if s in self.__language_map.keys():
            self.__source = s

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, t):
        if t in self.__language_map.get(self.__source, []):
            self.__target = t

    @property
    def language_list(self):
        return self.__language_list

    @property
    def language_map(self):
        return self.__language_map


class CalculationGetter(BaseGetter):
    def __init__(self, thread=None):
        super().__init__(thread)

    def _custom_get(self, text):
        pass
