#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 09:14:15 2023

@author: tosson
"""
import h5py
import numpy as np

class Data():
    file_name = ""
    
    energy = []
    event = []
    hit = []
    spectrum = []
    raw = []
    def __init__(self, filename):
        self.file_name = filename
        
    def LoadDataFromFile(self):
        with h5py.File(self.file_name, "r") as f:
            self.energy.append(self.energy.append(np.array(f.get('Energy'))) )    
            self.event.append(np.array(f.get('Event')))   
            self.hit.append(np.array(f.get('Hit')))
            self.spectrum.append( np.array(f.get('Spectrum')))
            self.raw.append( np.array(f.get('Raw')))
            
        self.energy = np.array(self.energy)
        self.event = np.array(self.event)
        self.hit = np.array(self.hit)
        self.spectrum = np.array(self.spectrum)
        self.raw = np.array(self.raw)