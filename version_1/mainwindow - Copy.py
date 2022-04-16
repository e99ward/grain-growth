import sys
#from tkinter import Scrollbar
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFrame, QSplitter
from PyQt5.QtWidgets import QGridLayout, QLabel, QLineEdit, QTextEdit, QSlider, QScrollBar
from PyQt5.QtCore import Qt


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        top = QFrame()
        top.setFrameShape(QFrame.Box)
        top.setFrameShadow(QFrame.Sunken)

        midleft = QFrame()
        midleft.setFrameShape(QFrame.StyledPanel)

        grid = QGridLayout(midleft)

        grid.addWidget(QLabel('Title:'), 0, 0)
        grid.addWidget(QLabel('Author:'), 1, 0)
        grid.addWidget(QLabel('Review:'), 2, 0)

        grid.addWidget(QLineEdit(), 0, 1)
        grid.addWidget(QLineEdit(), 1, 1)
        grid.addWidget(QTextEdit(), 2, 1)

        middle = QFrame()
        middle.setFrameShape(QFrame.Panel)
        db_setup = QGridLayout(middle)
        db_setup.addWidget(QLabel('Initial Time Step [0]:'), 0, 0)
        db_setup.addWidget(QLabel('End TIme Step [5000]:'), 1, 0)
        db_setup.addWidget(QLabel('Save Grain Size Interval [200]:'), 2, 0)
        db_setup.addWidget(QLabel('Save Histogram Interval [200]:'), 3, 0)
        db_setup.addWidget(QLineEdit('0'), 0, 1)
        db_setup.addWidget(QLineEdit('5000'), 1, 1)
        db_setup.addWidget(QLineEdit('200'), 2, 1)
        db_setup.addWidget(QLineEdit('200'), 3, 1)
        db_setup.setAlignment(Qt.AlignCenter)
        #topleft.setLayout(var_setup)
        
        bottom = QFrame()
        bottom.setFrameShape(QFrame.WinPanel)

        rbtn1 = QLabel('First Button', bottom)
        rbtn1.setGeometry(10, 10, 300, 45)
        slider = QSlider(Qt.Horizontal, bottom)
        slider.setRange(0, 10)
        slider.setTickPosition(QSlider.TicksBelow)
        #slider.move(100, 100)
        slider.setGeometry(100, 100, 300, 45)
        scrollBar = QScrollBar(Qt.Horizontal, bottom)
        scrollBar.setRange(0,100)
        scrollBar.setValue(0)
        scrollBar.setGeometry(100, 180, 300, 50)
        #slider.valueChanged.connect(self.dial.setValue)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(midleft)
        splitter.addWidget(middle)
        #splitter = QSplitter(Qt.Vertical)
        #splitter.addWidget(topleft)
        #splitter.addWidget(middle)
        #splitter.addWidget(bottom)
        
        vbox = QVBoxLayout()
        vbox.addWidget(splitter, 10)
        vbox.addWidget(top, 1)
        vbox.addWidget(bottom, 10)
        self.setLayout(vbox)

        self.setGeometry(300, 300, 1300, 1000)
        self.setWindowTitle('Grain Growth Calculator')
        self.show()

        scrollBar.valueChanged.connect(lambda: do_action())
        def do_action():
            value = scrollBar.value()
            rbtn1.setText("Current Value : " + str(value))
            slider.setValue(value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())