# -*- coding: utf-8 -*-
# @Time    : 2019/12/11 10:03
# @Author  : Xpp
# @Email   : Xpp233@foxmail.com
from time import sleep
from ctypes import windll
from PyQt5.QtCore import QThread
from pynput.keyboard import Key, Controller


class BaseWorker(QThread):
    def __init__(self, sleep_time=None, parent=None):
        super().__init__(parent)
        self.__is_paused = False
        self.sleep_time = sleep_time

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

    @property
    def isWorking(self):
        return not self.__is_paused

    @property
    def sleep_time(self):
        return self.__sleep_time

    @sleep_time.setter
    def sleep_time(self, time):
        self.__sleep_time = time if isinstance(time, int) and 0 < time <= 1800 else 60


class KeyBoardWorker(BaseWorker):
    def __init__(self, sleep_time=None, key=None, parent=None):
        super().__init__(sleep_time, parent)
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

    def __init__(self, sleep_time=None, parent=None):
        super().__init__(sleep_time, parent)
        self.__set_thread_execution_state = windll.kernel32.SetThreadExecutionState

    def work(self):
        self.__set_thread_execution_state(self.ES_SYSTEM_REQUIRED | self.ES_CONTINUOUS |
                                          self.ES_DISPLAY_REQUIRED)
