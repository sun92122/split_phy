# -*- coding: utf-8 -*-

from logging import (DEBUG, INFO, WARNING, FileHandler, Formatter, Logger,
                     StreamHandler, getLogger)
from os import listdir, mkdir, path, rename, stat, remove
from time import localtime, perf_counter_ns, strftime


def clean_oldlog():
    oldlog = min((log for log in listdir(path.join('.', 'log'))),
                 key=lambda fn: stat(path.join('.', 'log', fn)).st_mtime)
    remove(path.join('.', 'log', oldlog))


def get_log(debug: bool):
    newlogger: Logger = getLogger(name='NTNUPHY')
    newlogger.setLevel(DEBUG)  # show debug, info, warning, error, critical

    handler: FileHandler = FileHandler(path.join('log', "lastlog.log"), encoding='utf-8')
    formatter: Formatter = Formatter(
        '[%(levelname)s] %(name)s: %(asctime)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    newlogger.addHandler(handler)

    handler: StreamHandler = StreamHandler()
    if debug:
        handler.setLevel(INFO)  # show info, warning, error, critical
    else:
        handler.setLevel(WARNING)  # show warning, error, critical
    formatter: Formatter = Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    newlogger.addHandler(handler)
    return newlogger


def new_log(debug=False):
    if not path.isdir(path.join('log')):
        mkdir(path.join('log'))
    try:
        if len(listdir(path.join('log'))) >= 1:
            lastlog = strftime(
                "%Y-%m-%d-%H-%M-%S.log", localtime(path.getctime(path.join('log', "lastlog.log"))))
            rename(path.join('log', "lastlog.log"),
                   path.join('log', lastlog))
            newlogger = get_log(debug)
            newlogger.info('successfully renamed prelog')
        else:
            newlogger = get_log(debug)
    except:
        newlogger = get_log(debug)
        newlogger.info('failed to rename prelog', exc_info=True)

    MAXLOG = 5
    while len(listdir(path.join('log'))) > MAXLOG:
        clean_oldlog()
    return newlogger


def timing(func):
    def wrapper(*args, **kwargs):
        t1 = perf_counter_ns()
        try:
            func(*args, **kwargs)
        except:
            func()
        t2 = perf_counter_ns()
        secs = f"{(t2-t1)//1000000000}.{(t2-t1)%1000000000:0>9d}"
        try:
            args[0].logger.debug(f"{func.__name__} run: {secs} (secs)")
        except:
            print(f"{func.__name__} run: {secs} (secs)")
    return wrapper
