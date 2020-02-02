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
Language management tool.
"""
from sys import argv
from os import remove
from json import loads, dumps
from os.path import join, dirname

CUR_DIR = dirname(__file__)
LANGUAGE_DIR = join(dirname(CUR_DIR), 'Languages')


def show_language_map(language_map_path):
    """
    :param language_map_path: language_map file path.
    """
    with open(language_map_path, encoding='utf') as f:
        language_map = loads(f.read())
    print('\n\tcode\tname\n\t-----\t-----')
    for code, name in language_map.items():
        print('\t{}\t{}\n'.format(code, name))
    print()


def delete_language(code, language_map_path):
    """
    :param code: language code.
    :param language_map_path: language_map file path.
    :rtype: bool.
    """
    with open(language_map_path, encoding='utf') as f1:
        language_map = loads(f1.read())
    if 1 == len(language_map):
        print('Delete failed. At least one language is required.')
        return False
    name = language_map.pop(code, None)
    if name:
        with open(language_map_path, 'w', encoding='utf') as f2:
            f2.write(dumps(language_map))
        try:
            remove(join(dirname(language_map_path), 'Strings_{}.py'.format(code)))
        except OSError:
            pass
        print('Deleted successfully.')
        return True
    else:
        print('Delete failed. No Such language.')
        return False


def add_language(name, code, model, language_map_path):
    """
    :param name: language name.
    :param code: language code.
    :param model: model file path.
    :param language_map_path: language_map file path.
    :rtype: bool.
    """
    with open(language_map_path, encoding='utf') as f1:
        language_map = loads(f1.read())
    if name in language_map.values() or code in language_map.keys():
        print('Failed to add language. Language already exists.')
        return False
    with open(language_map_path, 'w', encoding='utf') as f2:
        language_map[code] = name
        f2.write(dumps(language_map))
    with open(model, encoding='utf') as f3:
        text = f3.read()
    filepath = join(dirname(model), 'Strings_{}.py'.format(code))
    with open(filepath, 'w', encoding='utf') as f4:
        r = f4.write(text.replace('{language}', name))
    print('Language added successfully. Filepath: {}'.format(filepath))
    return bool(r)


def main():
    note = '''Language management tool

Usage:


\t1. lang map:\t\t\tView language map.


\t2. lang del {code}:\t\tDelete language.
\tex: lang del en


\t3. lang add {code} {name}:\tAdd new language.
\tex: lang add en English


'''
    language_map_path = join(LANGUAGE_DIR, 'map.json')
    try:
        operation = argv[1]
        if 'map' == operation:
            show_language_map(language_map_path)
        elif 'add' == operation:
            add_language(argv[3], argv[2], join(LANGUAGE_DIR, 'model.txt'), language_map_path)
        elif 'del' == operation:
            delete_language(argv[2], language_map_path)
        else:
            print(note)
    except IndexError:
        print(note)


if __name__ == '__main__':
    main()
