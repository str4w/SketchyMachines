#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 25 15:13:35 2018

@author: rupert
"""

import pickle
import numpy as np

fbase="SketchyEggOutput/frame_20180325T165316"

fd=open(fbase+"_a.pkl",'rb')
lines=pickle.load(fd)

xmin=9999999
xmax=-9999999
ymin=99999999
ymax=-999999999
for l in lines:
    xmin=min(xmin,np.min(l[0]))
    ymin=min(ymin,np.min(l[1]))
    xmax=max(xmax,np.max(l[0]))
    ymax=max(ymax,np.max(l[1]))

xrng=xmax-xmin
yrng=ymax-ymin
rng=max(xrng,yrng)
xmin-=rng*0.02
xmax+=rng*0.02
ymin-=rng*0.02
ymax+=rng*0.02

xrng=xmax-xmin
yrng=ymax-ymin
rng=max(xrng,yrng)

def jitter(a):
    return a+np.random.randn(len(a))*0.25

fd=open(fbase+".svg",'w')

fd.write('<svg  xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">')
fd.write("\n")
for l in lines:
    xs=(jitter(l[0])-xmin)*(100./rng)
    ys=(jitter(l[1])-ymin)*(100./rng)
    fd.write('<path d="m %f,%f '%(xs[0],ys[0]))
    for i in range(1,len(xs)):
        fd.write("%f,%f "%(xs[i]-xs[i-1],ys[i]-ys[i-1]))
    fd.write('" style="stroke: #000000; fill:none;"/>')
    fd.write("\n")
fd.write('</svg>')
fd.write("\n")
