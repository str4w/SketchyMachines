#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 22:40:48 2018

@author: rupert
"""

fd=open("testpattern3.lines",'w')
y=20
for i in range(100):
    fd.write("%f %f %f %f\n"%(i,y,i,-y))
    y*=-1
fd.close()
