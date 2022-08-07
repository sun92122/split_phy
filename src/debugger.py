# -*- coding: utf-8 -*-

import logging
import os
from time import localtime, strftime, perf_counter_ns


def get_log(debug: bool):
    newlogger: logging.Logger = logging.getLogger(name='NTNUCourse')
    newlogger.setLevel(logging.INFO)

    handler: logging.FileHandler = logging.FileHandler('lastlog.log')
    formatter: logging.Formatter = logging.Formatter(
        '[%(levelname)s] %(name)s: %(asctime)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    newlogger.addHandler(handler)

    handler: logging.StreamHandler = logging.StreamHandler()
    if debug:
        handler.setLevel(logging.INFO)  # show info, warning, error, critical
    else:
        handler.setLevel(logging.WARNING)  # show warning, error, critical
    formatter: logging.Formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    newlogger.addHandler(handler)
    return newlogger


def new_log(debug=False):
    try:
        lastlog = strftime("%Y-%m-%d-%H-%M-%S.log",
                           localtime(os.path.getctime("lastlog.log")))
        os.rename('lastlog.log', os.path.join('log', lastlog))
        newlogger = get_log(debug)
        newlogger.info('successfully renamed prelog')
    except:
        newlogger = get_log(debug)
        newlogger.info('failed to rename prelog', exc_info=True)
    return newlogger


def timing(func):
    def wrapper(self=None, *args, **kwargs):
        print(*args, **kwargs)
        print("Start", func.__name__)
        t1 = perf_counter_ns()
        func(self)
        t2 = perf_counter_ns()
        print("Elapsed time(secs):", t2 - t1)
    return wrapper