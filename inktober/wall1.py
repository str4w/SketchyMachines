#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ImageToHPGL
Copyright Rupert Brooks 2017
"""
import glob
import pickle
import numpy as np
import cv2
import matplotlib.pyplot as plt
import pyximport; pyximport.install()
import ImageToVectors #as i2v # import make_lines_from_images,organize_lines

file="../SourceMaterial/wall_crop.png"
    
gs=cv2.imread(file,cv2.IMREAD_GRAYSCALE)



edges=cv2.adaptiveThreshold(gs,255,cv2.THRESH_BINARY,cv2.ADAPTIVE_THRESH_MEAN_C,15,3)



edges2=cv2.erode(edges,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)))
edges2=cv2.dilate(edges2,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5)))

edges=255-edges2

lines=ImageToVectors.make_lines_from_image(edges)
z=map(lambda x:len(x[0]),lines)
z=list(z)
z=np.array(z)
lines2=sorted( lines,key=lambda x:-len(x[0]))
finallines=ImageToVectors.organize_lines(lines2)

#lines=[ (jitter(a),jitter(b)) for a,b in lines]
print("There are %d elements in lines"%(len(finallines)))
xlim=gs.shape[1]
ylim=-gs.shape[0]

fd=open("wall1.lines",'w')
fd.write("%f %f %f %f %f %f\n"%(20,0,0,0,0,-20))
fd.write("%f %f %f %f %f %f\n"%(20,ylim,0,ylim,0,ylim+20))
fd.write("%f %f %f %f %f %f\n"%(xlim-20,0,xlim,0,xlim,-20))
fd.write("%f %f %f %f %f %f\n"%(xlim-20,ylim,xlim,ylim,xlim,ylim+20))
for l in finallines:
    for (x,y) in zip(l[0],l[1]):
        fd.write("%f %f "%(y,-x))
    fd.write("\n")
# register marks
fd.write("%f %f %f %f %f %f\n"%(20,0,0,0,0,-20))
fd.write("%f %f %f %f %f %f\n"%(20,ylim,0,ylim,0,ylim+20))
fd.write("%f %f %f %f %f %f\n"%(xlim-20,0,xlim,0,xlim,-20))
fd.write("%f %f %f %f %f %f\n"%(xlim-20,ylim,xlim,ylim,xlim,ylim+20))
fd.close()
