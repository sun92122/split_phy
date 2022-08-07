# -*- coding: utf-8 -*-

from os import path

from PyQt5 import QtCore, QtGui, QtWidgets

from debugger import new_log, timing
from UI import UiMain


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.logger = new_log()
        self.flash = lambda: QtWidgets.QApplication.processEvents()
        self.ui = UiMain()
        self.ui.setupUi(self)
        self.connect_button()

    @timing        
    def connect_button(self):
        # QPushButton documentation: https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QPushButton.html
        for R in range(1, 6):
            for C in range(1, 6):
                button: QtWidgets.QPushButton = getattr(self.ui, f'R{R}C{C}')
                button.clicked.connect(self.push_button)
                try:
                    button.setIcon(QtGui.QIcon(path.join('img', 'test.jpg')))
                    button.setIconSize(QtCore.QSize(320, 222))
                except:
                    self.logger.warning(f"Button {button.objectName()} icon import failed")

    @timing
    def push_button(self):
        button: QtWidgets.QPushButton = self.sender()
        # button = self.ui.R1C1 # test
        self.logger.info(f"Button {button.objectName()} has been pressed")
        orig = button.geometry()
        dwidth = orig.width()//100 if orig.width() > 200 else 2

        def sub_width(i):
            nonlocal button, dwidth
            if button.geometry().width()-dwidth < 0:
                dx = dwidth//2
                x, y, w, h = button.geometry().getRect()
                button.setGeometry(x-dx, y, 0, h)
                self.flash()
                return False
            else:
                dx = (dwidth+(i%2))//2
                button.setGeometry(button.geometry()-QtCore.QMargins(dx, 0, dwidth, 0))
                self.flash()
                return True

        def add_width(i):
            nonlocal button, dwidth, orig
            if button.geometry().width()+dwidth > orig.width():
                button.setGeometry(orig)
                self.flash()
                return False
            else:
                dx = (dwidth+(i%2))//2
                button.setGeometry(button.geometry()+QtCore.QMargins(dx, 0, dwidth, 0))
                self.flash()
                return True
        

        for i in range(100):
            if not sub_width(i):
                break
        for i in range(100):
            if not add_width(i):
                break
