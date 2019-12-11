# -*- coding: utf-8 -*-
# @Time    : 2019/12/4 20:15
# @Author  : Xpp
# @Email   : Xpp233@foxmail.com
"""
NoSleepWorker
~~~~~~~~~~~~~
This module can prevent devices from sleeping.

Usage:
    from NoSleepWorkers import Worker

    worker = Worker()

    # start
    worker.start()

    # show working state
    print(worker.isWorking)

    # suspend
    worker.suspend()

    # resume
    worker.resume()
"""
from sys import platform
if 'win' == platform[:3]:
    from .Workers import WindowsWorker as Worker
else:
    from .Workers import KeyBoardWorker as Worker
