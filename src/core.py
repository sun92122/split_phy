# -*- coding: utf-8 -*-

from os import path
from random import sample, seed, shuffle
from time import perf_counter

from pygame import mixer
from PyQt5 import QtCore, QtGui, QtWidgets

from data import Debug, group, try_again
from debugger import new_log, timing
from imageandsound import img_decode, sound_decode
from UI import UiMain


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.logger = new_log()
        self.flash = lambda: QtWidgets.QApplication.processEvents()
        self.ui = UiMain()
        self.ui.setupUi(self)
        self.img_size = (1086, 730)
        self.ui.backgrond.setStyleSheet('background-color: white;')
        self.image_style = """
            QPushButton {
                border-image: url("./img/test.jpg");
                border: 5px solid #7091FF;
                border-radius: 10px;
            }
            QPushButton:hover, QPushButton:pressed {
                border-image: url("./img/test.jpg");
                border: 5px solid #0000FF;
            }
        """
        self.front_style = """
            QPushButton {
                background-color: white;
                border-radius: 10px;
                padding: 2px 4px
            }
        """
        self.showFullScreen()
        self.has_pressed = {}
        self.connect_button()
        self.set_button_icon()
        self.timer = perf_counter()-5
        self.set_push_sound()
        self.play_sound = lambda: mixer.music.play()
        self.rand_result = {}
        self.rand()

    @timing
    def connect_button(self):
        # QPushButton documentation: https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QPushButton.html
        for R in range(1, 6):
            for C in range(1, 6):
                button: QtWidgets.QPushButton = getattr(self.ui, f'R{R}C{C}')
                button.clicked.connect(self.push_button)
                self.has_pressed[f'R{R}C{C}'] = False

    @timing
    def set_button_icon(self):
        debug = Debug.set_button_icon
        if not path.exists(path.join('.', 'img', 'image.jpg')) and not path.exists(path.join('.', 'img', 'image.png')):
            img_type, self.img_size = img_decode()
        else:
            img_type, self.img_size = img_decode(True)
        if not debug:
            self.image_style = self.image_style.replace('test.jpg', f'image{img_type}')
        for R in range(1, 6):
            for C in range(1, 6):
                button: QtWidgets.QPushButton = getattr(self.ui, f'R{R}C{C}')
                try:
                    button.setStyleSheet(self.image_style)
                except:
                    self.logger.warning(
                        f"Button {button.objectName()} icon import failed")

    @timing
    def set_push_sound(self):
        debug = Debug.set_push_sound
        sound_path = path.join(
            '.', 'sound', 'test.mp3' if debug else 'sound.mp3')
        if not path.exists(sound_path):
            sound_decode()
        mixer.init()
        mixer.music.load(sound_path)

    @timing
    def push_button(self, checked):
        button: QtWidgets.QPushButton = self.sender()
        button_name = button.objectName()
        debug = Debug.push_button
        if self.has_pressed[button_name]:
            self.logger.info(
                f"Button {button_name} has been pressed but has been flipped")
        elif perf_counter()-self.timer > 5 or debug:
            self.timer = perf_counter()
            self.logger.info(f"Button {button_name} has been pressed")
        else:
            self.logger.info(
                f"Button {button_name} has been pressed but still on cooldown")
            return

        self.play_sound()
        self.flip_button(button)

    def flip_button(self, button: QtWidgets.QPushButton):
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
                dsize = QtCore.QMargins((dwidth+(i % 2))//2, 0, dwidth, 0)
                button.setGeometry(button.geometry()-dsize)
                self.flash()
                return True

        def add_width(i):
            nonlocal button, dwidth, orig
            if button.geometry().width()+dwidth > orig.width():
                button.setGeometry(orig)
                self.flash()
                return False
            else:
                dsize = QtCore.QMargins((dwidth+(i % 2))//2, 0, dwidth, 0)
                button.setGeometry(button.geometry()+dsize)
                self.flash()
                return True

        for i in range(100):
            if not sub_width(i):
                break

        if button.styleSheet() != self.front_style:
            button.setStyleSheet(self.front_style)
            button.setText(self.rand_result[button.objectName()])
            self.has_pressed[button.objectName()] = True
        else:
            button.setText("")
            button.setStyleSheet(self.image_style)

        for i in range(100):
            if not add_width(i):
                break

    @timing
    def rand(self):
        seed(self.timer)
        group_25 = group + sample(try_again, 25-len(group))
        shuffle(group_25)
        for R in range(1, 6):
            for C in range(1, 6):
                self.rand_result[f"R{R}C{C}"] = group_25[R+C*5-6]

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        width, height = a0.size().width(), a0.size().height()
        img_w, img_h = self.img_size
        if width/img_w > height/img_h:
            dw = (width-height/img_h*img_w)/2
            self.ui.Rspacer.changeSize(dw, 40)
            self.ui.Lspacer.changeSize(dw, 40)
        else:
            self.ui.Rspacer.changeSize(0, 40)
            self.ui.Lspacer.changeSize(0, 40)
        self.flash()
    
    def keyPressEvent(self, a0: QtGui.QKeyEvent):
        if a0.key() == QtCore.Qt.Key_Escape:
            QtCore.QCoreApplication.instance().quit()
