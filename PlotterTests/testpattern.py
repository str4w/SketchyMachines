#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 22:40:48 2018

@author: rupert
"""

fd=open("testpattern.lines",'w')
for i in range(10):
    fd.write("%f %f %f %f\n"%(i/1.0,-20+i,i/1.0,20-i))
    fd.write("%f %f %f %f\n"%(30-i/1.0,-20+i,30-i/1.0,20-i))
fd.close()
