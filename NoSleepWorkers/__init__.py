# -*- coding: utf-8 -*-
# @Time    : 2019/12/4 20:15
# @Author  : Xpp
# @Email   : Xpp233@foxmail.com
"""
This module can prevent devices from sleeping.

Usage:
    from NoSleepWorkers import Worker

    worker = Worker()
    worker.start()

    # show working state
    print(worker.isWorking)

    # suspend
    worker.suspend()

    # resume
    worker.resume()
"""
from sys import platform
# import "Worker" according to the user's system platform.
if 'win' == platform[:3]:
    from .WindowsWorker import WindowsWorker as Worker
else:
    from .KeyBoardWorker import KeyBoardWorker as Worker
