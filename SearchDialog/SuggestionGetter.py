# -*- coding: utf-8 -*-
# @Time    : 2019/11/26 13:10
# @Author  : Xpp
# @Email   : Xpp233@foxmail.com
from json import loads
from requests.sessions import Session


class SuggestionGetter:

    def __init__(self):
        self.__api = 'https://sug.so.360.cn/suggest/word?'
        self.__session = Session()
        self.__session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, ' \
                                               'like Gecko) Chrome/65.0.3325.162 Safari/537.36 '

    def get_suggestions(self, text):
        l = []
        if not text:
            return l
        if '360' in self.__api:
            l = self.__get_360_suggest(text)
        elif 'baidu' in self.__api:
            l = self.__get_baidu_suggest(text)
        elif 'sogou' in self.__api:
            l = self.__get_sogou_suggest(text)
        return l

    def __get_360_suggest(self, text):
        params = {'callback': 'suggest_so',
                  'encodein': 'utf-8',
                  'encodeout': 'utf-8',
                  'word': text,
                  '_jsonp': 'suggest_so'}
        try:
            r = self.__session.get(self.__api, params=params)
        except Exception:
            return []
        if 200 == r.status_code:
            text = r.text
            p_index = text.find('p:')
            p = text[p_index + 2: text.find(',', p_index)]
            if 'true' in p:
                return loads(text[text.find('['): text.rfind(']') + 1])
        return []

    def __get_baidu_suggest(self, text):
        params = {'wd': text}
        try:
            r = self.__session.get(self.__api, params=params)
        except Exception:
            return []
        if 200 == r.status_code:
            json = r.json()
            if 'true' == json.get('p'):
                return json.get('s')
        return []

    def __get_sogou_suggest(self, text):
        params = {'key': text}
        try:
            r = self.__session.get(self.__api, params=params)
        except Exception:
            return []
        if 200 == r.status_code:
            json = r.json()
            if 'true' == json.get('p'):
                return json.get('s')
        return []

    @property
    def api(self):
        return self.__api

    @api.setter
    def api(self, value):
        self.__api = value if value else 'https://sug.so.360.cn/suggest/word?'
