#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 08:59:57 2023

@author: tosson
"""

from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
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
        self.fig, self.ax = plt.subplots(figsize= (w,h))
        super().__init__(self.fig)
        self.setParent(parent)


class MainWindow(QtWidgets.QMainWindow):
    data_object = data_obj.Data()
    toggle_selector = any
    file_full_path = ""
    y_start, y_end, x_start, x_end = 0,0,0,0
    
    area_direction = 0
    chart_2d = any
    plot_1d = any
    chart_2d_selected_area = any
    
    energy_spectra = any
    
    
    def __init__(self):
        super().__init__()
        uic.loadUi("mainwindow.ui", self)
        self.openFileBtn.clicked.connect(self.upload_file)
        self.streamDataBtn.clicked.connect(self.stream_data_from_file)
        self.generateEngBtn.clicked.connect(self.generate_energy_spectrum)
        self.fitBtn.clicked.connect(self.start_fit)
        self.saveBtn.clicked.connect(self.save_energy)

        self.horCheckBox.stateChanged.connect(self.horizontal_checked)
        self.verCheckBox.stateChanged.connect(self.vertical_checked)
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

        self.chart_2d_selected_area.ax.axis(False)
        self.chart_2d_selected_area.fig.canvas.draw()
        self.engGroupBox.setEnabled(True)
   



    def generate_energy_spectrum(self):
        areas_number = self.numberOfAreasSpinBox.value()
        self.energy_spectra = np.zeros((areas_number, 1024))
        energy_channel_kev = np.round(np.arange(start=1, stop=1025, step=1) * 0.04155, 3)

        all_selected_pixels =  self.data_object.raw[self.x_start:self.x_end, self.y_start:self.y_end]
        self.plot_1d.ax.clear()
        if self.area_direction == 0:        
            step_size = int((self.x_end - self.x_start)/areas_number)
            
            for n in range(areas_number):
                a_s = step_size * n
                a_e = a_s + step_size
                for i in range(a_s, a_e):
                    for j in range(self.y_end-self.y_start-1):
                        self.energy_spectra[n] = self.energy_spectra[n] + all_selected_pixels[i,j, :]
                self.plot_1d.ax.plot(energy_channel_kev,self.energy_spectra[n], label ="Area "+str(n+1))
                
                np.save("d"+str(n+1)+".np",self.energy_spectra[n] )
                
        else:   
            step_size = int((self.y_end - self.y_start)/areas_number)
            for n in range(areas_number):
                a_s = step_size * n
                a_e = a_s + step_size
                for i in range(a_s, a_e):
                    for j in range(self.x_end-self.x_start-1):
                        self.energy_spectra[n] = self.energy_spectra[n] + all_selected_pixels[j,i, :]
                self.plot_1d.ax.plot(energy_channel_kev,self.energy_spectra[n], label ="Area "+str(n+1))
        
        
        self.plot_1d.ax.axis(True)
        self.plot_1d.ax.set_xlabel("Energy [keV]")
        self.plot_1d.ax.set_ylabel("Counts")
        #self.plot_1d.ax.ylabel("Counts")
        self.plot_1d.ax.legend()
        self.plot_1d.fig.canvas.draw()
      
        self.fittingGroupBox.setEnabled(True)
        self.saveBtn.setEnabled(True)
        #plt.savefig(filenames[data_id].replace(".h", "")+"_energy_spectrum_original.png", format='png', dpi=600)
        #plt.show()


    def start_fit(self):
        self.generate_energy_spectrum()
        areas_number = self.numberOfAreasSpinBox.value()
        start = int(self.minEngSpinBox.value()/0.04155)
        end = int(self.maxEngSpinBox.value()/0.04155)
        self.fitText.setPlainText("")
        for n in range(areas_number):   
            ok, p, y_fitted = self.data_object.fit_energy_spectrum(self.data_object.energy_channel_kev[start:end], self.energy_spectra[n,start:end])
            if not ok:
                self.fitText.setPlainText("No valid fitting, please chech the energy interval for fitting")
                self.generate_energy_spectrum()
                return
            t = self.fitText.toPlainText()
            self.fitText.setPlainText(t + "\nEnergy-Area"+str(n+1) + "="+str(np.round(p[2],2))+"keV" )
            #print(p)
            self.plot_1d.ax.plot(self.data_object.energy_channel_kev[start:end], y_fitted, '--', label ="Fitting-Area"+str(n+1))   
        self.fitText.setEnabled(True)
        self.plot_1d.ax.legend()
        self.plot_1d.fig.canvas.update()
        self.plot_1d.fig.canvas.draw()
        
    def horizontal_checked(self):
        self.area_direction = 0 
        if self.horCheckBox.isChecked():
            
            self.verCheckBox.setCheckState(False)
        
    def vertical_checked(self):
        self.area_direction = 1 
        if self.verCheckBox.isChecked():

            self.horCheckBox.setCheckState(False)
    
    def save_energy(self):
        np.savetxt(self.file_full_path.replace(".h", "")+"_POS_X_"+str(self.x_start)+"_TO_" +str(self.x_end)+"_Y_"  +str(self.y_start)+"_TO_" + str(self.y_end) +  '.txt', np.c_[self.data_object.energy_channel_kev, np.transpose(self.energy_spectra)])
        np.savetxt(self.file_full_path.replace(".h", "")+"_POS_X_"+str(self.x_start)+"_TO_" +str(self.x_end)+"_Y_"  +str(self.y_start)+"_TO_" + str(self.y_end) +  '.csv', np.c_[self.data_object.energy_channel_kev, np.transpose(self.energy_spectra)])
        self.saveBtn.setEnabled(False)
    
    
    
    
    
    
    
