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
from Resources import resource
from Utils.SuggestionGetter import KeywordGetter, TranslationGetter

default_setting = {
    'TipState': '1',
    'StartupState': '1',
    'Language': 'cn',
    'SearchEngine/count': '9',
    'SearchEngine/engines/0': 'baidu||{}||https://www.baidu.com/s?ie=utf-8&wd=%s'.format(
        resource.image.get('baidu.png')),
    'SearchEngine/engines/1': 'google||{}||https://www.google.com/search?q=%s'.format(resource.image.get('google.png')),
    'SearchEngine/engines/2': 'bing||{}||http://www.bing.com/search?q=%s'.format(resource.image.get('bing.png')),
    'SearchEngine/engines/3': 'cnbing||{}||http://cn.bing.com/search?q=%s'.format(resource.image.get('bing.png')),
    'SearchEngine/engines/4': '360||{}||https://www.so.com/s?ie=utf-8&q=%s'.format(resource.image.get('360.png')),
    'SearchEngine/engines/5': 'sogou||{}||https://www.sogou.com/web?ie=utf8&query=%s'.format(
        resource.image.get('sogou.png')),
    'SearchEngine/engines/6': 'toutiao||{}||https://m.toutiao.com/search/?&keyword=%s'.format(
        resource.image.get('toutiao.png')),
    'SearchEngine/engines/7': 'yandex||{}||https://yandex.com/search/?text=%s'.format(resource.image.get('yandex.png')),
    'SearchEngine/engines/8': 'douban||{}||https://search.douban.com/movie/subject_search?search_text=%s'.format(
        resource.image.get('douban.png')),
    'SearchEngine/default_engine_index': '0',
    'KeywordGetter/state': '1',
    'KeywordGetter/provider/index': '0',
    'KeywordGetter/provider/data': str(KeywordGetter.QH360),
    'TranslationGetter/state': '1',
    'TranslationGetter/keyword': 'fy',
    'TranslationGetter/provider/index': '0',
    'TranslationGetter/provider/data': str(TranslationGetter.YOUDAO),
    'TranslationGetter/source': '',
    'TranslationGetter/target': '',
    'CalculationGetter/state': '1',
    'CalculationGetter/keyword': '+',
    'BrowserPath': '',
    'PrivateMode': '0',
    'Hotkey/keys': 'caps_lock',
    'Hotkey/interval': '0.3',
    'Hotkey/repetitions': '2',
    'Ui/distance': '3',
    'Ui/opacity': '0.9',
    'Ui/theme_index': '0',
    'Ui/border_radius': '0',
    'Ui/font_color': 'black',
    'Ui/theme_color': '#3498db',
    'Ui/border_color': '#a7acaf',
    'Ui/selected_color': '#91c9f7',
    'Ui/background_color': 'white',
    'NoSleepState': '0',
}
