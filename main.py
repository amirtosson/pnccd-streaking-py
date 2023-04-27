#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 08:48:20 2023

@author: tosson
"""


from PyQt5 import QtWidgets
import main_window as _main_win
import sys

def main():
    app = QtWidgets.QApplication(sys.argv)
    mw = _main_win.MainWindow()
    mw.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()