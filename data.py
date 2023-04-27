#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 09:14:15 2023

@author: tosson
"""
import h5py
import numpy as np
import random

class Data():
    file_name = ""
    
    energy = []
    event = []
    hit = []
    spectrum = []
    raw = []

        
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
        
        
