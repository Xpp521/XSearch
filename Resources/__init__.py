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
"""
Resource module.


Usage:

    >>> from Resources import resource as res

    >>> res.image.get('app.ico')
    'D:/xxx/XSearch/Resources/image/app.ico'

    >>> res.image.get_relative('app.ico')
    'Resources/image/app.ico'

    >>> res.ttf.get('mvboli.ttf')
    'D:/xxx/XSearch/Resources/ttf/mvboli.ttf'
"""
from os import walk
from os.path import join, isabs, dirname


class ResourceGetter:
    """A resource getter for the given directory.
    The resource in the directory cannot have duplicate filename, otherwise it will be ignored."""
    def __init__(self, base_dir):
        if isabs(base_dir):
            self.__directory = base_dir.replace('\\', '/')
        else:
            raise ValueError('"base_dir" must be an absolute path')
        self.__root_dir = dirname(dirname(base_dir)).replace('\\', '/')
        self.__map = {}
        self.__scan()

    def __scan(self):
        """Scan all files in self.__directory and save them in self.__map.
        Data format: (key, value) => (filename, filepath).
        Ps: If there is a duplicate filename, it will be ignored!"""
        for root, dirs, files in walk(self.__directory):
            for filename in files:
                if self.__map.get(filename):
                    continue
                self.__map[filename] = join(root, filename).replace('\\', '/')

    def get(self, filename):
        """Get absolute file path."""
        return self.__map.get(filename)

    def get_relative(self, filename):
        """Get relative file path."""
        return self.__map.get(filename).replace(self.__root_dir, '')[1:]

    @property
    def directory(self):
        return self.__directory


class Resource:
    def __init__(self, res_dir):
        if isabs(res_dir):
            self.__directory = res_dir
        else:
            raise ValueError('"res_dir" must be an absolute path')
        self.__image = ResourceGetter(join(res_dir, 'image'))
        self.__ttf = ResourceGetter(join(res_dir, 'ttf'))

    @property
    def image(self):
        return self.__image

    @property
    def ttf(self):
        return self.__ttf


resource = Resource(dirname(__file__))
