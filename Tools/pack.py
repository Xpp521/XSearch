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
from sys import path
from shutil import rmtree, move
from os.path import join, dirname
from os import walk, popen, listdir
from zipfile import ZipFile, ZIP_DEFLATED
path.append('../')
import info


# Current directory
CUR_DIR = dirname(__file__)

# Root directory
ROOT = dirname(CUR_DIR)


def clean():
    """Clean old version."""
    paths = [join(ROOT, 'build'),
             join(ROOT, 'dist')]
    for p in paths:
        print('Cleaning directory: {}'.format(p))
        try:
            rmtree(p, True)
        except FileNotFoundError:
            continue


def pack():
    """Pack a new version."""
    print(popen('pyinstaller {}'.format(join(CUR_DIR, 'pack.spec'))).read())
    for p in listdir(CUR_DIR):
        if p in ('build', 'dist'):
            move(join(CUR_DIR, p), join(ROOT, p))


def compress():
    """Compress the new version."""
    directory = join(ROOT, 'dist', listdir(join(ROOT, 'dist'))[0])
    d = dirname(directory)
    print('Compressing...')
    with ZipFile('{}_Portable.zip'.format(directory), 'w') as zip_file:
        for root, dirs, files in walk(directory):
            for file in files:
                zip_file.write(join(root, file), join(root.replace(d, ''), file), ZIP_DEFLATED)
        zip_file.comment = '''{}_{}
Author: {}
Email: {}
License: GNU General Public v3.0
Open source address: {}'''.format(info.APP_NAME, info.VERSION,
                                  info.AUTHOR_NAME, info.AUTHOR_EMAIL,
                                  info.OPEN_SOURCE_ADDRESS).encode()
    print('Compression completed')


def main():
    clean()
    pack()
    compress()


if __name__ == '__main__':
    main()
    input('Script end.')
