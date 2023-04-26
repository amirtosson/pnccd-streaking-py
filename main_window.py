#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 08:59:57 2023

@author: tosson
"""


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic



class MainWindow(QtWidgets.QMainWindow):
    
    file_full_path = ""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()
    
    def initUI(self):
        #TODO: Set tooltips
        uic.loadUi("mainwindow.ui", self)
        self.openFileBtn.clicked.connect(self.UploadFile)

        
    def UploadFile(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setWindowTitle('Open Data File')
        dialog.setNameFilter('Data files (*.h5)')
        dialog.setDirectory(QtCore.QDir.currentPath())
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.file_full_path = str(dialog.selectedFiles()[0])
        self.fileNameText.setText(self.file_full_path)

