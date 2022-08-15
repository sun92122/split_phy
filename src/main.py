# -*- coding: utf-8 -*-

# magical 2022.8

import os
import sys
import ctypes

from PyQt5 import QtWidgets

from core import MainWindow

if __name__ == '__main__':
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('arbitrary string')
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    os.system('cls' if os.name == 'nt' else 'clear')
    window.show()
    sys.exit(app.exec_())
