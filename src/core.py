# -*- coding: utf-8 -*-

from os import path
from time import perf_counter

from PyQt5 import QtCore, QtGui, QtWidgets

from debugger import new_log, timing
from UI import UiMain
from imageandsound import img_decode, sound_decode


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.logger = new_log()
        self.flash = lambda: QtWidgets.QApplication.processEvents()
        self.ui = UiMain()
        self.ui.setupUi(self)
        self.connect_button()
        self.set_button_icon()
        self.timer = perf_counter()-5

    @timing    
    def connect_button(self):
        # QPushButton documentation: https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QPushButton.html
        for R in range(1, 6):
            for C in range(1, 6):
                button: QtWidgets.QPushButton = getattr(self.ui, f'R{R}C{C}')
                button.clicked.connect(self.push_button)

    @timing
    def set_button_icon(self):
        debug = False
        img_decode()
        image = './img/'+('test.jpg' if debug else 'image.jpg')
        for R in range(1, 6):
            for C in range(1, 6):
                button: QtWidgets.QPushButton = getattr(self.ui, f'R{R}C{C}')
                try:
                    button.setStyleSheet('QPushButton {'+' border-image: url("{}"); '.format(image)+'}')
                except:
                    self.logger.warning(f"Button {button.objectName()} icon import failed")
        
    @timing
    def push_button(self, checked):
        button: QtWidgets.QPushButton = self.sender()
        if perf_counter()-self.timer > 5:
            self.timer = perf_counter()
            self.logger.info(f"Button {button.objectName()} has been pressed")
        else:
            self.logger.info(f"Button {button.objectName()} has been pressed but still on cooldown")
            return
        # button = self.ui.R1C1 # test
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
        
        button.setStyleSheet('QPushButton {'+' border-image: url("{}"); '.format('none')+'}')

        for i in range(100):
            if not add_width(i):
                break


    def play_sound(self):
        sound_decode()