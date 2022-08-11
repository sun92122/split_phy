# -*- coding: utf-8 -*-

import os
import sys

from PyQt5 import QtWidgets

from core import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    os.system('cls' if os.name == 'nt' else 'clear')
    window.show()
    sys.exit(app.exec_())
