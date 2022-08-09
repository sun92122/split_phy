# -*- coding: utf-8 -*-

import logging
import os
from time import localtime, strftime, perf_counter_ns


def get_log(debug: bool):
    if not os.path.isdir(os.path.join('log')):
        os.mkdir(os.path.join('log'))
    newlogger: logging.Logger = logging.getLogger(name='NTNUPHY')
    newlogger.setLevel(logging.DEBUG) # show debug, info, warning, error, critical

    handler: logging.FileHandler = logging.FileHandler(
        os.path.join('log', "lastlog.log"))
    formatter: logging.Formatter = logging.Formatter(
        '[%(levelname)s] %(name)s: %(asctime)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    newlogger.addHandler(handler)

    handler: logging.StreamHandler = logging.StreamHandler()
    if debug:
        handler.setLevel(logging.INFO) # show info, warning, error, critical
    else:
        handler.setLevel(logging.WARNING) # show warning, error, critical
    formatter: logging.Formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    newlogger.addHandler(handler)
    return newlogger


def new_log(debug=False):
    try:
        lastlog = strftime("%Y-%m-%d-%H-%M-%S.log",
                           localtime(os.path.getctime(os.path.join('log', "lastlog.log"))))
        os.rename(os.path.join('log', "lastlog.log"),
                  os.path.join('log', lastlog))
        newlogger = get_log(debug)
        newlogger.info('successfully renamed prelog')
    except:
        newlogger = get_log(debug)
        newlogger.info('failed to rename prelog', exc_info=True)
    return newlogger


def timing(func):
    def wrapper(*args, **kwargs):
        t1 = perf_counter_ns()
        try:    
            func()
        except:
            func(*args, **kwargs)
        t2 = perf_counter_ns()
        secs = f"{(t2-t1)//1000000000}.{(t2-t1)%1000000000:0>9d}"
        try:
            args[0].logger.debug(f"{func.__name__} run: {secs} (secs)")
        except:
            print(f"{func.__name__} run: {secs} (secs)")
    return wrapper