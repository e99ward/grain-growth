import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox
from PyQt5.QtWidgets import QFrame, QGridLayout, QSlider, QScrollBar
from PyQt5.QtWidgets import QLabel, QLineEdit, QRadioButton, QCheckBox, QPushButton
from PyQt5.QtCore import Qt
from datainit import GenerateInitGrain
from growth import Grain
import numpy as np
from plotlib import MplCanvas

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self._cts = 0
        self.graingrowth = Grain()
        self.stat = np.array([])
        self.initUI()

    def initUI(self):
        #fist frame (topleft) - set-up parameters
        topleft = QFrame()
        topleft.setFrameShape(QFrame.Box)
        label1 = QLabel('Calculation Set-up', topleft)
        label1.setGeometry(10, 0, 300, 50)
        font_header = label1.font()
        font_header.setPointSize(12)
        label1.setFont(font_header)
        rbtn1 = QRadioButton('AGG')
        rbtn2 = QRadioButton('NGG')
        cbox = QCheckBox('Screw-disl. assisted')
        var_setup = QGridLayout(topleft)
        var_setup.addWidget(QLabel('Calculation Mode:'), 0, 0)
        var_setup.addWidget(QLabel('Temperature (1100C - 1700C):'), 1, 0)
        var_setup.addWidget(QLabel('Step Free Energy (0.0hG - 1.0hG):'), 2, 0)
        var_setup.addWidget(QLabel('Liquid Volume Fraction (0.00L - 1.00L):'), 3, 0)
        var_setup.addWidget(QLabel('Calculation Time Step (=speed):'), 4, 0)
        var_setup.addWidget(QLabel(''), 5, 0)
        var_mode = self.CalcMode(rbtn1, rbtn2, cbox)
        var_temp = QLineEdit('1500')
        var_stfe = QLineEdit('0.82')
        var_liqv = QLineEdit('0.46')
        var_ctsv = self.CalcTimeStep()        
        var_setup.addWidget(var_mode, 0, 1)
        var_setup.addWidget(var_temp, 1, 1)
        var_setup.addWidget(var_stfe, 2, 1)
        var_setup.addWidget(var_liqv, 3, 1)
        var_setup.addWidget(var_ctsv, 4, 1)
        label2 = QLabel('0.01 s\t __0.1 s\t ____1 s')
        label2.setMaximumHeight(15)
        var_setup.addWidget(label2, 5, 1)
        var_setup.setAlignment(Qt.AlignCenter)
        
        #second frame (middle) - database
        middle = QFrame()
        middle.setFrameShape(QFrame.Box)
        label3 = QLabel('Calculation Data', middle)
        label3.setGeometry(10, 0, 300, 50)
        label3.setFont(font_header)
        db_setup = QGridLayout(middle)
        db_setup.addWidget(QLabel('Initial Time Step [0]:'), 0, 0)
        db_setup.addWidget(QLabel('End TIme Step [5000]:'), 1, 0)
        db_setup.addWidget(QLabel('Save Grain Size Interval [200]:'), 2, 0)
        db_setup.addWidget(QLabel('Save Histogram Interval [200]:'), 3, 0)
        cts_from = QLineEdit('0')
        cts_to = QLineEdit('5000')
        cts_save_data = QLineEdit('200')
        cts_save_hist = QLineEdit('200')
        db_setup.addWidget(cts_from, 0, 1)
        db_setup.addWidget(cts_to, 1, 1)
        db_setup.addWidget(cts_save_data, 2, 1)
        db_setup.addWidget(cts_save_hist, 3, 1)
        db_setup.setAlignment(Qt.AlignCenter)
        
        #third frame (bottom) - generate initial grain set
        bottom = QFrame()
        bottom.setFrameShape(QFrame.Box)
        label4 = QLabel('Generation Initial Grain Set', bottom)
        label4.setGeometry(10, 0, 300, 50)
        label4.setFont(font_header)
        db_init = QGridLayout(bottom)
        db_init.addWidget(QLabel('Number of Grains:'), 0, 0)
        db_init.addWidget(QLabel('Standard Gaussian DIstribution'), 1, 0)
        db_init.addWidget(QLabel('Average (100 = 1 um):'), 2, 0)
        db_init.addWidget(QLabel('Standard Deviation:'), 3, 0)
        init_size = QLineEdit('100000')
        init_ave = QLineEdit('100')
        init_std = QLineEdit('20')
        db_init.addWidget(init_size, 0, 1)
        db_init.addWidget(QLabel(''), 1, 1)
        db_init.addWidget(init_ave, 2, 1)
        db_init.addWidget(init_std, 3, 1)
        init_On = QPushButton('Generate')
        db_init.addWidget(init_On, 2,3,-1,-1)
        init_On.clicked.connect(lambda: do_generate())
        def do_generate():
            ave = init_ave.text()
            std = init_std.text()
            size = init_size.text()
            GenerateInitGrain(ave, std, size)
            init_On.setText('DONE')
        db_init.setAlignment(Qt.AlignCenter)

        #right frame: calculation overview
        topright = QFrame()
        topright.setFrameShape(QFrame.Box)
        topright.setFrameShadow(QFrame.Sunken)
        label5 = QLabel('Calculation Overview', topright)
        label5.setGeometry(10, 0, 300, 50)
        label5.setFont(font_header)
        label_cts = QLabel('Progress: 0 CTS (0 s)', topright)
        label_cts.setGeometry(10, 70, 300, 45)
        label_cts_look = QLabel('Histogram CTS: 0', topright)
        label_cts_look.setGeometry(600, 70, 300, 45)
        scrollBar = QScrollBar(Qt.Horizontal, topright)
        scrollBar.setRange(0,100)
        scrollBar.setValue(0)
        scrollBar.setGeometry(280, 70, 300, 50)
        scrollBar.valueChanged.connect(lambda: do_action())
        def do_action():
            value = scrollBar.value()
            label_cts_look.setText('Histogram CTS: ' + str(value))
            #show histogram

        # RUN
        execute = QFrame()
        execute.setFrameShape(QFrame.NoFrame)
        okButton = QPushButton('START', execute)
        okButton.setFont(font_header)
        okButton.setGeometry(50, 0, 200, 80)
        okButton.clicked.connect(lambda: do_run())
        cancelButton = QPushButton('Resume', execute)
        cancelButton.setGeometry(300, 0, 200, 80)
        cancelButton.setEnabled(False)
        cancelButton.clicked.connect(lambda: do_cancel())
        def do_run():
            okButton.setEnabled(False)
            cancelButton.setEnabled(True)
            temp = int(var_temp.text())
            stfe = float(var_stfe.text())
            liqv = float(var_liqv.text())
            ctsv = self.CalcSpeed(var_ctsv.value())
            mode1 = rbtn1.isChecked()
            mode2 = cbox.isChecked()
            self.graingrowth.CalcControl(temp, stfe, liqv, ctsv, mode1, mode2)
            #load starting file, and input to np-array
            t_from = int(cts_from.text())
            t_to = int(cts_to.text())
            t_step1 = int(cts_save_data.text())
            t_step2 = int(cts_save_hist.text())
            t_step = min(t_step1, t_step2)
            self.graingrowth.LoadGrain(t_from)
            #preparation of the plot: r_ave, r_max with time
            #t_plot = round((t_to - t_from)/100)
            #if t_plot == 0:
            #    t_plot = 1
            sc = MplCanvas(self, width=10, height=5, dpi=100)
            #sc.axes.plot([np.random.randint(0, 10) for i in range(10)])            
            graph = QGridLayout(topright)
            graph.addWidget(QLabel(''))
            graph.addWidget(sc)
            graph.addWidget(QLabel(''))
            graph.setAlignment(Qt.AlignCenter)
            #get Av St Rmax
            #self.stat = self.graingrowth.GetStatistics()
            while self._cts < t_to:
                #calc grain growth
                label_cts.setText('Progress: ' + str(self._cts) + ' CTS (' + str(self._cts*ctsv) +' s)')
                self.graingrowth.CalcGrowth(self._cts)
                #get Av St Rmax
                #self.stat = self.graingrowth.GetStatistics()
                self._cts += 1
                if self._cts%t_step == 0:
                    #show overview
                    self.stat = self.graingrowth.GetStatistics()
                    ave = self.stat[:,1]
                    rst = self.stat[:,2]
                    sc.axes.plot(ave,'b-')
                    sc.axes.plot(rst,'r-')
                    graph.update()
                    graph.deleteLater()
                if self._cts%t_step1 == 0:
                    #save grain if 
                    print('in while loop')
                if self._cts%t_step2 == 0:
                    #save hist if 
                    print('in while loop')
                self.show()
                #show overview
                
            print('calc end', self._cts)
            self.stat = self.graingrowth.GetStatistics()
            self.SaveStatistics()
            graph.deleteLater()
            
        def do_cancel():
            okButton.setEnabled(True)
        
        vbox = QVBoxLayout()
        vbox.addWidget(topleft, 4)
        vbox.addWidget(middle, 3)
        vbox.addWidget(bottom, 3)
        vbox.addWidget(execute, 1)
        hbox = QHBoxLayout()
        hbox.addLayout(vbox, 1)
        hbox.addWidget(topright, 2) 
        self.setLayout(hbox)
        self.setGeometry(300, 300, 1500, 1000)
        self.setWindowTitle('Grain Growth Calculator')
        self.show()

    def CalcMode(self, rbtn1, rbtn2, cb):
        groupbox = QGroupBox()
        #rbtn1 = AGG, rbtn2 = NGG
        rbtn1.setChecked(True)
        rbtn1.move(100,0)
        hbox = QHBoxLayout()
        hbox.addWidget(rbtn1)
        hbox.addWidget(rbtn2)
        #cb = QCheckBox('Screw-disl. assisted')
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(cb)
        groupbox.setLayout(vbox)
        groupbox.setMaximumHeight(150)
        return groupbox

    def CalcTimeStep(self):
        slider = QSlider(Qt.Horizontal, self)
        slider.setRange(0, 2)
        slider.setValue(1)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setFixedWidth(200)
        #value: 0=0.01s, 1=0.1s, 2=1s
        return slider

    def CalcSpeed(self, val):
        if val==0:
            calc_speed = 0.01
        elif val==1:
            calc_speed = 0.1
        else:
            calc_speed = 1.0
        return calc_speed

    def GrainLoading(self, cts_num):
        #filename = 'd_0000000.txt.npy'
        filename = 'd_' + '{:07d}'.format(cts_num) + '.txt.npy'
        self._grain = np.load(filename)
        #in case of using ascii format
        #filename = 'd_' + '{:07d}'.format(cts_num) + '.txt'
        #read line by line, and append to _grain
        
    def SaveStatistics(self):
        filename = 'r_star_and_grain_ave.txt'
        with open(filename, 'w') as handle:
            handle.write('step\t r_star\t r_ave\t r_std\t r_max\t g_num\n')
            np.savetxt(handle, self.stat, fmt='%15.2f')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())