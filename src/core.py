from PyQt5 import QtCore, QtGui, QtWidgets

from UI import UiMain


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = UiMain()
        self.ui.setupUi(self)
        self.connect_button()

    def connect_button(self):
        # QPushButton documentation: https://doc.qt.io/qt-5/qpushbutton.html
        for R in range(1, 6):
            for C in range(1, 6):
                getattr(self.ui, f'R{R}C{C}').clicked.connect(self.push_button)
    
    def push_button(self):
        button = self.sender().objectName()
        print(button)