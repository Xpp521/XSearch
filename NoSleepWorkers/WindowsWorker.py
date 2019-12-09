# -*- coding: utf-8 -*-
# @Time    : 2019/12/4 20:16
# @Author  : Xpp
# @Email   : Xpp233@foxmail.com
"""
This file is for Windows system.
Use Windows api function: "SetThreadExecutionState" to prevent devices from sleeping.
"""
from time import sleep
from ctypes import windll
from PyQt5.QtCore import QThread


class WindowsWorker(QThread):
    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001
    ES_DISPLAY_REQUIRED = 0x00000002
    ES_AWAYMODE_REQUIRED = 0x00000040

    def __init__(self, sleep_time=None):
        super().__init__()
        self.__is_paused = False
        self.__set_thread_execution_state = windll.kernel32.SetThreadExecutionState
        self.sleep_time = sleep_time

    def run(self):
        while True:
            if not self.__is_paused:
                self.__set_thread_execution_state(self.ES_SYSTEM_REQUIRED | self.ES_CONTINUOUS |
                                                  self.ES_DISPLAY_REQUIRED)
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
