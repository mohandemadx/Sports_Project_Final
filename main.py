import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from pyqtgraph import PlotWidget, PlotDataItem
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np
from scipy import fftpack
from PyQt5 import QtWidgets, uic 



class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):
        self.ui = uic.loadUi('design.ui', self)
        self.setWindowTitle("Projectile Simulation Application")
        self.setWindowIcon(QIcon("icons/2.png"))
        
        self.initTimer()
        self.current_index = 0

        self.firing_speed = 0
        self.angle_value = 0
        self.distance_value = 0

        self.speed_slider.valueChanged.connect(self.speed_changed)
        self.angle.textChanged.connect(self.angle_changed)
        self.done.clicked.connect(self.update_plot)

        self.simulation = PlotWidget()
        self.horizontalLayout.addWidget(self.simulation)
        self.horizontalLayout.removeWidget(self.simulation_qwid)

        # Draw x and y axes
        self.simulation.addItem(PlotDataItem(x=[-1000, 1000], y=[0, 0], pen='w'))
        self.simulation.addItem(PlotDataItem(x=[0, 0], y=[-1000, 1000], pen='w'))
        self.simulation.setXRange(-2, 100)
        self.simulation.setYRange(-2, 100)
        self.simulation.plot(x = [0], y = [0], pen=None, symbol='o', symbolSize=20)


    
    def speed_changed(self):
        # self.speed.setText(str(round(self.speed_slider.value(), 4)))
        self.firing_speed = self.speed_slider.value()
    
    def angle_changed(self):
        angle_text = self.angle.text()
        if angle_text.isdigit():
            angle_value = int(angle_text)
            if 0 <= angle_value <= 90:
                self.angle_value = np.radians(angle_value)
            else:
                self.angle_value = np.radians(min(max(angle_value, 0), 90))
        else:
            self.angle_value = 0



    def update_plot(self):
        time_max = (2 * self.firing_speed * np.sin(self.angle_value)) / 9.81
        t = np.linspace(0, time_max, 500)
        self.x = self.firing_speed * np.cos(self.angle_value) * t
        self.y = self.firing_speed * np.sin(self.angle_value) * t - 0.5 * 9.81 * t**2

        self.distance.setText(str(round(max(self.x), 4)))

    
        self.simulation.clear()
        self.simulation.addItem(PlotDataItem(x=[-1000, 1000], y=[0, 0], pen='w'))  # x-axis
        self.simulation.addItem(PlotDataItem(x=[0, 0], y=[-1000, 1000], pen='w'))  # y-axis
        self.simulation.setXRange((-1/100)*max(self.x), max(self.x) + 1, 0)
        self.simulation.setYRange((-1/100)*max(self.y), max(self.y) + 1, 0)
        self.current_index = 0
        self.timer.start(1)
    
    def update_animation(self):
        if self.current_index < len(self.x):
            x_point = self.x[self.current_index]
            y_point = self.y[self.current_index]
            if self.current_index > 0:  # Remove previous point if it exists
                self.simulation.removeItem(self.previous_point)
            self.previous_point = self.simulation.plot(x=[x_point], y=[y_point], pen=None, symbol='o', symbolSize=20)
            self.current_index += 1
        else:
            self.timer.stop()

    def initTimer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainApp()
    mainWin.show()
    sys.exit(app.exec())
