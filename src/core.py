# -*- coding: utf-8 -*-

# QPushButton documentation: https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QPushButton.html

from os import path
from random import sample, seed, shuffle
from time import perf_counter

from pygame import mixer
from PyQt5 import QtCore, QtGui, QtWidgets

from data import Debug, group, try_again
from debugger import new_log, timing
from imageandsound import img_decode, sound_decode, hover_decode, icon_decode, front_decode
from UI import UiMain


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.logger = new_log()
        self.flash = lambda: QtWidgets.QApplication.processEvents()
        self.ui = UiMain()
        self.ui.setupUi(self)
        self.newfont = self.get_font()
        self.setWindowTitle('我愛瑞典肉丸')
        try:
            icon_type = icon_decode()
            self.setWindowIcon(QtGui.QIcon(path.join('.', 'img', f'icon{icon_type}')))
        except:
            pass
        self.img_size = (1086, 730)
        self.ui.backgrond.setStyleSheet('background-color: #BABABA;')
        self.image_style = """
            QPushButton {
                border-image: url("./img/test.jpg");
            }
            QPushButton:hover, QPushButton:pressed {
                border-image: url("./img/test_hover.jpg");
            }
        """
        self.front_style = """
            QPushButton {
                border-image: url("./img/test.jpg");
                color: #333
            }
        """
        self.space_size = 0
        self.showFullScreen()
        self.has_pressed = {}
        self.connect_button()
        self.set_button_icon()
        self.set_close()
        self.timer = perf_counter()-5
        self.set_push_sound()
        self.play_sound = lambda: mixer.music.play()
        self.rand_result = {}
        self.rand()


    def get_font(self):
        font = QtGui.QFont()
        font.setFamily('微軟正黑體')
        font.setPixelSize(50)
        return font


    def set_close(self):
        self.close = QtWidgets.QDockWidget(self)
        self.close.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable)
        self.close.setFloating(True)
        self.close_button = QtWidgets.QPushButton()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.close_button.setSizePolicy(sizePolicy)
        self.close_button.setMinimumSize(QtCore.QSize(0, 0))
        self.close_button.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.close_button.setText("X")
        self.close_button.setObjectName("Close")
        self.close_button.clicked.connect(QtCore.QCoreApplication.instance().quit)
        size = self.space_size/2+1
        self.logger.debug(self.close_button.geometry().size())
        self.close.setWidget(self.close_button)
        self.close.setTitleBarWidget(QtWidgets.QWidget())
        self.close.setGeometry(self.size().width()-size+1, 0, size, size)
        self.close.setStyleSheet("background-color: #BABABA;")
        self.close_button.setStyleSheet("""
            QPushButton {
                border: 2px solid #222;
                border-radius: 38%;
                background-color: #FF0;
                font-size: 20px;
            }
            QPushButton:hover, QPushButton:pressed {
                background-color: #F00;
            }
        """.replace('num', str(38)))
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.close)
                

    @timing
    def connect_button(self):
        for R in range(1, 6):
            for C in range(1, 6):
                button: QtWidgets.QPushButton = getattr(self.ui, f'R{R}C{C}')
                button.clicked.connect(self.push_button)
                button.setFont(self.newfont)
                self.has_pressed[f'R{R}C{C}'] = False

    @timing
    def set_button_icon(self):
        debug = Debug.set_button_icon

        if not path.exists(path.join('.', 'img', 'image.jpg')) and not path.exists(path.join('.', 'img', 'image.png')):
            img_type, self.img_size = img_decode()
        else:
            img_type, self.img_size = img_decode(True)

        if not path.exists(path.join('.', 'img', 'hover.jpg')) and not path.exists(path.join('.', 'img', 'hover.png')):
            hover_type = hover_decode()
        else:
            hover_type = hover_decode(True)

        if not path.exists(path.join('.', 'img', 'front.jpg')) and not path.exists(path.join('.', 'img', 'front.png')):
            front_type = front_decode()
        else:
            front_type = front_decode(True)

        if not debug:
            self.image_style = self.image_style.replace('test.jpg', f'image{img_type}').replace('test_hover.jpg', f'hover{hover_type}')
            self.front_style = self.front_style.replace('test.jpg', f'front{front_type}')

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

    def resizeEvent(self, a0: QtGui.QResizeEvent): # not callable
        width, height = a0.size().width(), a0.size().height()
        img_w, img_h = self.img_size
        if width/img_w > height/img_h:
            self.space_size = (width-height/img_h*img_w)/2
        else:
            self.space_size = 0
        self.ui.Rspacer.changeSize(self.space_size, 40)
        self.ui.Lspacer.changeSize(self.space_size, 40)
        self.flash()
    
    def keyPressEvent(self, a0: QtGui.QKeyEvent): # not callable
        if a0.key() == QtCore.Qt.Key_Escape:
            QtCore.QCoreApplication.instance().quit()
