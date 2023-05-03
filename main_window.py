#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 08:59:57 2023

@author: tosson
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector, PolygonSelector, SpanSelector
import matplotlib.pyplot as plt
import numpy as np

if int(QtCore.qVersion()[0]) > 4:
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)


import data as data_obj





class Canvas(FigureCanvas):
    ax = any
    fig = any
    def __init__(self, parent):
        w = int(parent.frameGeometry().width()/80)
        h = int(parent.frameGeometry().height()/80)
        print(w)
        self.fig, self.ax = plt.subplots(figsize= (w,h))
        #plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
        #plt.margins(0,0)
        super().__init__(self.fig)
        self.setParent(parent)


class MainWindow(QtWidgets.QMainWindow):
    data_object = data_obj.Data()
    toggle_selector = any
    file_full_path = ""
    y_start, y_end, x_start, x_end = 0,0,0,0
    
    chart_2d = any
    plot_1d = any
    chart_2d_selected_area = any
    def __init__(self):
        super().__init__()
        uic.loadUi("mainwindow.ui", self)
        self.openFileBtn.clicked.connect(self.upload_file)
        self.streamDataBtn.clicked.connect(self.stream_data_from_file)
        self.generateEngBtn.clicked.connect(self.generate_energy_spectrum)

        self.chart_2d  = Canvas(self.mainPlotWidget)
        toolbar_2d = NavigationToolbar(self.chart_2d, self.toolBarWidget)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar_2d)
        self.chart_2d.ax.axis(False)
        self.chart_2d_selected_area  = Canvas(self.selectedAreaPlotWidget)
        self.chart_2d_selected_area.ax.axis(False)
        self.plot_1d  = Canvas(self.engWidget)
        self.chart_2d.fig.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
        self.chart_2d_selected_area.fig.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
        toolbar_1d = NavigationToolbar(self.plot_1d, self.engWidget)
        layout2 = QtWidgets.QVBoxLayout()
        layout2.addWidget(toolbar_1d)

        
        
        
        
        
    def upload_file(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setWindowTitle('Open Data File')
        dialog.setNameFilter('Data files (*.h5)')
        dialog.setDirectory(QtCore.QDir.currentPath())
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.file_full_path = str(dialog.selectedFiles()[0])
        self.fileNameText.setText(self.file_full_path)
        self.data_object.file_name = self.file_full_path
    
    def stream_data_from_file(self):
        self.data_object.load_data_from_file()
        self.plot()
    
    def plot(self):
        self.chart_2d.ax.clear()
        self.chart_2d.ax.imshow(self.data_object.event, interpolation='none')
        self.chart_2d.ax.axis(False)
        self.chart_2d.fig.canvas.draw()
        self.toggle_selector = RectangleSelector(self.chart_2d.ax, self.line_select_callback, useblit=True,
                                       button=[1, 3],  # don't use middle button
                                       minspanx=5, minspany=5,
                                       spancoords='pixels',
                                       interactive=True)
        
    def line_select_callback(self, eclick, erelease):
        self.chart_2d_selected_area.ax.clear()
        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata
        self.y_start, self.y_end, self.x_start, self.x_end =  int(x1), int(x2) , int(y1), int(y2)  
        self.chart_2d_selected_area.ax.imshow(self.data_object.event[self.x_start:self.x_end, self.y_start:self.y_end], interpolation='none')
        #self.chart_2d_selected_area.ax.set_xticks(np.arange(self.x_start, self.x_end))

        self.chart_2d_selected_area.ax.axis(False)
        self.chart_2d_selected_area.fig.canvas.draw()
        self.engGroupBox.setEnabled(True)
   
        
        #self.chart_2d_selected_area.fig.canvas.mpl_connect("axes_leave_event", self.test_profile_2)
        #self.chart_2d_selected_area.fig.canvas.mpl_connect("axes_enter_event", self.test_profile)



    def generate_energy_spectrum(self):
        areas_number = self.numberOfAreasSpinBox.value()
        all_selected_pixels =  self.data_object.raw[self.x_start:self.x_end, self.y_start:self.y_end]
        energy_spectra = np.zeros((areas_number, 1024))
        
        step_size = int((self.x_end - self.x_start)/areas_number)
        
        energy_channel_kev = np.round(np.arange(start=1, stop=1025, step=1) * 0.04155, 3)
        self.plot_1d.ax.clear()
        for n in range(areas_number):
            a_s = step_size * n
            a_e = a_s + step_size
            for i in range(a_s, a_e):
                for j in range(self.y_end-self.y_start-1):
                    energy_spectra[n] = energy_spectra[n] + all_selected_pixels[i,j, :]
            self.plot_1d.ax.plot(energy_channel_kev,energy_spectra[n], label ="Area "+str(n+1))
        
        self.plot_1d.ax.axis(True)
        self.plot_1d.ax.set_xlabel("Energy [keV]")
        self.plot_1d.ax.set_ylabel("Counts")
        #self.plot_1d.ax.ylabel("Counts")
        self.plot_1d.ax.legend()
        self.plot_1d.fig.canvas.draw()

        #plt.savefig(filenames[data_id].replace(".h", "")+"_energy_spectrum_original.png", format='png', dpi=600)
        #plt.show()


    def line_profile(self, event):

        print("==========NEW==========")
        print("EY: ",event.y)
        print("EYD: ",event.ydata)
        print("YS: ",self.y_start)
        print("YN: ",self.y_end)
        print("====================")
        print("EX: ", event.x)   
        print("EXD: ", event.xdata)  
        print("XS: ",self.x_start)
        print("XE: ",self.x_end)
        
        
    def test_profile(self, event):
        plt.connect("button_press_event", self.line_profile)
        print("Con")
        
    def test_profile_2(self, event):
        plt.disconnect(self.line_profile)
        print("Dis")
        #self.chart_2d_selected_area.ax.plot(event.xy, c='r')
        
        
        #self.init_ui()
    # prparing plotting scene
    
    """
    
    static_ax = any
    canvas_2d = any
    static_ax_selected_area = any
    canvas_2d_selected_area = any
    data_object = data_obj.Data()
    toggle_selector = any
    file_full_path = ""
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        #px = 1/plt.rcParams['figure.dpi'] 
        #TODO: Set tooltips
        uic.loadUi("mainwindow.ui", self)
        self.openFileBtn.clicked.connect(self.upload_file)
        self.streamDataBtn.clicked.connect(self.stream_data_from_file)
        self.canvas_2d = FigureCanvas(Figure())
        self.static_ax = self.canvas_2d.figure.subplots()
        layout = QtWidgets.QVBoxLayout(self.mainPlotWidget)
        layout.addWidget(self.canvas_2d)
        self.canvas_2d_selected_area = FigureCanvas(Figure())
        self.static_ax_selected_area = self.canvas_2d_selected_area.figure.subplots()
        layout = QtWidgets.QVBoxLayout(self.selectedAreaPlotWidget)
        layout.addWidget(self.canvas_2d_selected_area)
        
    
    
    
    
    """
    
    
    
    
    
    
