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
Packing tool.


Recommended packaging environment:
System:
    - 32-bit Windows 7;

Python version:
    - python 3.5.4;

Python package requirements:
    - lxml>=4.4.2
    - PyQt5>=5.14.1
    - pynput==1.4.5
    - pycrypto==2.6.1
    - PyHotKey>=1.3.3
    - requests>=2.22.0
    - PyInstaller>=3.6
"""
from sys import argv, path
from shutil import rmtree, move
from zipfile import ZipFile, ZIP_DEFLATED
from os import walk, popen, remove, listdir
from os.path import join, dirname, isdir, isfile
path.append('../')
import INFO

# Current directory
CUR_DIR = dirname(__file__)

# Root directory
ROOT = dirname(CUR_DIR)


def remove_paths(paths):
    """Remove all directories and files in the given paths."""
    for p in paths:
        try:
            if isfile(p):
                print('Removing file: {}'.format(p))
                remove(p)
            elif isdir(p):
                print('Removing directory: {}'.format(p))
                rmtree(p, True)
        except FileNotFoundError:
            continue


def filter_path(directory, include=None, exclude=None, key=None, walk_dir=False):
    """Filter paths in the given directory.
    :param directory: directory to filter.
    :param include: include list.
    :param exclude: exclude list.
    :param key: filter function.
    :param walk_dir: whether to walk the given directory.
    :rtype: list.
    """
    include = include if isinstance(include, list) else []
    exclude = exclude if isinstance(exclude, list) else []
    if callable(key):
        key = key
    elif include and not exclude:
        def key(pa):
            return False
    elif exclude and not include:
        def key(pa):
            return True
    else:
        key = None

    def check(pa):
        if pa in include:
            return True
        if pa not in exclude:
            if key:
                if key(pa):
                    return True
        return False
    result = []
    if walk_dir:
        for root, dirs, files in walk(directory):
            for f in files:
                if check(f):
                    result.append(join(root, f))
            for d in dirs:
                if check(d):
                    result.append(join(root, d))
    else:
        for p in listdir(directory):
            if check(p):
                result.append(join(directory, p))
    return result


def clean():
    """Remove old version and all __pycache__ files."""
    remove_paths(filter_path(ROOT, ['__pycache__'], walk_dir=True))
    remove_paths([join(ROOT, 'build'), join(ROOT, 'dist')])


def pack():
    """Package new version."""
    print(popen('pyinstaller {}'.format(join(CUR_DIR, 'pack.spec'))).read())
    for p in listdir(CUR_DIR):
        if p in ('build', 'dist'):
            move(join(CUR_DIR, p), join(ROOT, p))
    directory = join(ROOT, 'dist', listdir(join(ROOT, 'dist'))[0])
    paths = [join(directory, 'Icons', 'ico')]
    paths.extend(filter_path(directory, ['opengl32sw.dll', 'd3dcompiler_47.dll'],
                             ['Qt5Core.dll', 'Qt5Widgets.dll', 'Qt5Gui.dll'], lambda pa: pa.startswith('Qt5')))
    directory = join(directory, 'PyQt5')
    paths.extend(filter_path(directory, exclude=['Qt', 'Qt.pyd', 'QtGui.pyd',
                                                 'QtCore.pyd', 'QtWidgets.pyd', 'sip.cp35-win32.pyd']))
    directory = join(directory, 'Qt')
    paths.extend(filter_path(directory, exclude=['plugins']))
    directory = join(directory, 'plugins')
    paths.extend(filter_path(directory, exclude=['iconengines', 'imageformats', 'platforms', 'styles']))
    remove_paths(paths)


def compress():
    """Compress current version."""
    try:
        directory = join(ROOT, 'dist', listdir(join(ROOT, 'dist'))[0])
    except IndexError:
        return
    d = dirname(directory)
    print('Compressing...')
    with ZipFile('{}_Portable.zip'.format(directory), 'w') as zip_file:
        for root, dirs, files in walk(directory):
            for file in files:
                zip_file.write(join(root, file), join(root.replace(d, ''), file), ZIP_DEFLATED)
        zip_file.comment = '''{}_{}
Author: {}
Email: {}
License: GPLv3.0
Open source address: {}'''.format(INFO.APP_NAME, INFO.VERSION,
                                  INFO.AUTHOR_NAME, INFO.AUTHOR_EMAIL,
                                  INFO.OPEN_SOURCE_ADDRESS).encode()
    print('Compression completed.')


def main():
    note = '''Packing tool

Usage:


\t1. pack r:\t\tRemove old version and all "__pycache__" files.


\t2. pack p:\t\tPackage new version.


\t3. pack c:\t\tCompress current version.


\t4. pack pc:\t\tPackage and compress new version.


'''
    if 2 != len(argv):
        print(note)
        return
    operation = argv[1]
    if 'r' == operation:
        clean()
    elif 'p' == operation:
        pack()
    elif 'c' == operation:
        compress()
    elif 'pc' == operation:
        pack()
        compress()
    else:
        print(note)


if __name__ == '__main__':
    main()
