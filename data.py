#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 09:14:15 2023

@author: tosson
"""
import h5py
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

class Data():
    file_name = ""
    
    energy = []
    event = []
    hit = []
    spectrum = []
    raw = []
    energy_channel_kev = np.round(np.arange(start=1, stop=1025, step=1) * 0.04155, 3)
        
    def load_data_from_file(self):
        with h5py.File(self.file_name, "r") as f:
            self.energy = np.array(f.get('Energy'))     
            self.event = np.array(f.get('Event'))   
            self.hit = np.array(f.get('Hit'))
            self.spectrum = np.array(f.get('Spectrum'))
            self.raw = np.array(f.get('Raw'))
            
        self.energy = np.array(self.energy)
        self.event = np.array(self.event)
        self.hit = np.array(self.hit)
        self.spectrum = np.array(self.spectrum)
        self.raw = np.array(self.raw)
    
        
    def gauss(self, x, H, A, x0, sigma):
        return H + A * np.exp(-(x - x0) ** 2 / (2 * sigma ** 2))

    
    def gaussian_fit(self, x_data, y_data):
        mean = sum(x_data * y_data) / sum(y_data)
        sigma = np.sqrt(sum(y_data * (x_data - mean) ** 2) / sum(y_data))
        popt, pcov = curve_fit(self.gauss, x_data, y_data, p0=[min(y_data), max(y_data), mean, sigma])
        return popt
        
    
    def fit_energy_spectrum(self, x, y):
        try:
            p = self.gaussian_fit(x, y)
            y_f = self.gauss(x, *p)
        except:
            return False, [],[]
        return True, p, y_f