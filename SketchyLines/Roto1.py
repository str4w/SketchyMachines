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

files=glob.glob("rotoscope/amen_0*.jpg")
for file in files:
    gs=cv2.imread(file,cv2.IMREAD_GRAYSCALE)
    edges = np.zeros_like(gs)
    cv2.Canny(gs,15000,3000,edges,7,False)

    #ImageToVectors.condense_images(files,0.4,fbase+"_edges.png")
    lines=ImageToVectors.make_lines_from_image(edges)
    finallines=ImageToVectors.organize_lines(lines)

    #lines=[ (jitter(a),jitter(b)) for a,b in lines]
    print("There are %d elements in lines"%(len(finallines)))
    xlim=gs.shape[1]
    ylim=-gs.shape[0]

    fd=open(file[:-3]+"lines",'w')
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
