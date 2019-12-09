# -*- coding: utf-8 -*-
# @Time    : 2019/12/4 20:16
# @Author  : Xpp
# @Email   : Xpp233@foxmail.com
"""
Simulate keyboard activity to prevent devices from sleeping.
"""
from time import sleep
from PyQt5.QtCore import QThread
from pynput.keyboard import Key, Controller


class KeyBoardWorker(QThread):

    def __init__(self, sleep_time=None, key=None):
        super().__init__()
        self.__is_paused = False
        self.key = key
        self.sleep_time = sleep_time
        self.__keyboard = Controller()

    def run(self):
        while True:
            if not self.__is_paused:
                self.__keyboard.press(self.__key)
                self.__keyboard.release(self.__key)
            sleep(self.__sleep_time)

    def suspend(self):
        self.__is_paused = True

    def resume(self):
        self.__is_paused = False

    @property
    def isWorking(self):
        return not self.__is_paused

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, key):
        self.__key = key if isinstance(key, Key) else Key.alt

    @property
    def sleep_time(self):
        return self.__sleep_time

    @sleep_time.setter
    def sleep_time(self, time):
        self.__sleep_time = time if isinstance(time, int) and 0 < time <= 1800 else 60
