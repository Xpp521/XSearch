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
from time import sleep
from PyQt5.QtCore import QThread
from pynput.keyboard import Key, Controller


class BaseWorker(QThread):
    def __init__(self, sleepTime=None, parent=None):
        super().__init__(parent)
        self.__is_paused = False
        self.sleepTime = sleepTime

    def work(self):
        raise NotImplementedError

    def run(self):
        while True:
            if not self.__is_paused:
                self.work()
            sleep(self.__sleep_time)

    def suspend(self):
        self.__is_paused = True

    def resume(self):
        self.__is_paused = False

    def changeWorkingState(self):
        """
        Suspend or resume this worker.
        """
        self.__is_paused = not self.__is_paused

    @property
    def isWorking(self):
        return self.isRunning() and not self.__is_paused

    @property
    def sleepTime(self):
        return self.__sleep_time

    @sleepTime.setter
    def sleepTime(self, time):
        self.__sleep_time = time if isinstance(time, int) and 0 < time <= 1800 else 60


class KeyBoardWorker(BaseWorker):
    def __init__(self, sleepTime=None, key=None, parent=None):
        super().__init__(sleepTime, parent)
        self.key = key
        self.__keyboard = Controller()

    def work(self):
        self.__keyboard.press(self.__key)
        self.__keyboard.release(self.__key)

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, key):
        self.__key = key if isinstance(key, Key) else Key.alt


class WindowsWorker(BaseWorker):
    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001
    ES_DISPLAY_REQUIRED = 0x00000002
    ES_AWAYMODE_REQUIRED = 0x00000040

    def __init__(self, sleepTime=None, parent=None):
        from ctypes import windll
        super().__init__(sleepTime, parent)
        self.__set_thread_execution_state = windll.kernel32.SetThreadExecutionState

    def work(self):
        self.__set_thread_execution_state(self.ES_SYSTEM_REQUIRED | self.ES_CONTINUOUS |
                                          self.ES_DISPLAY_REQUIRED)
