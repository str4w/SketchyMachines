#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 14:30:48 2018

@author: rupert
"""

import cv2
import numpy as np

from OpenCVApp import OpenCVApp

class ThisApp (OpenCVApp):
    def __init__(self,videoDevice=0):
        super(ThisApp,self).__init__("ThisApp",videoDevice)
    
    def process_frame(self,frame):
        print("Processing")
        z=cv2.bilateralFilter(frame,d=7,sigmaColor=9,sigmaSpace=7)
        return z
    
thisApp=ThisApp()
thisApp.run()