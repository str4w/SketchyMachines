#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 16:00:35 2018

@author: rupert
"""

# Inspired by https://www.desmos.com/calculator/xuztx3bd35
# See also https://twitter.com/dandersod/status/982246268549214208?s=19

import numpy as np
import matplotlib.pyplot as plt
n=800
T=np.linspace(np.pi*2.0/n,2.0*np.pi,n)

x1s=np.cos(3*T+0.5*np.sin(7*T))
y1s=np.sin(3*T+0.5*np.sin(7*T))
x2s=np.cos(5*T-0.5*np.cos(11*T))
y2s=np.sin(5*T-0.5*np.cos(11*T))

#fig=plt.figure()
#ax=fig.add_axes([0.1,0.1,1,1])
inextents =np.array([[-1.,-1.],[1.,1.]])
outextents=np.array([[100,100],[16000,10000]])
scale=min( (outextents[1,0]-outextents[0,0])/(inextents[1,0]-inextents[0,0]),  (outextents[1,1]-outextents[0,1])/(inextents[1,1]-inextents[0,1]))
incenter=(inextents[1,:]+inextents[0,:])/2.0
outcenter=(outextents[1,:]+outextents[0,:])/2.0

fdsvg=open("murmuration.svg",'w')

fdsvg.write('<svg  xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">')
fdsvg.write("\n")

fdhpgl=open("murmuration.hpgl",'w')
fdhpgl.write("SP1;\n")


for x1,y1,x2,y2 in zip(x1s,y1s,x2s,y2s):
    dx=x2-x1
    dy=y2-y1
    if dx>0:
        deltax1=-1-x1
        deltax2=1-x1
    else:
        deltax1=1-x1
        deltax2=-1-x1
    if dy>0:
        deltay1=-1-y1
        deltay2=1-y1
    else:
        deltay1=1-y1
        deltay2=-1-y1
    t1=np.maximum(deltax1/dx,deltay1/dy)
    t2=np.minimum(deltax2/dx,deltay2/dy)
    xs=[x1+t1*dx,x1+t2*dx]
    ys=[y1+t1*dy,y1+t2*dy]
    plt.plot(xs,ys,'r-')
    fdsvg.write('<path d="m %f,%f '%(xs[0]*100,ys[0]*100))
    for i in range(1,len(xs)):
        fdsvg.write("%f,%f "%((xs[i]-xs[i-1])*100,(ys[i]-ys[i-1])*100))
    fdsvg.write('" style="stroke: #000000; fill:none;"/>')
    fdsvg.write("\n")
    x1hpgl=np.round((xs[0]-incenter[0])*scale+outcenter[0]).astype(np.int)
    y1hpgl=np.round((ys[0]-incenter[1])*scale+outcenter[1]).astype(np.int)
    x2hpgl=np.round((xs[1]-incenter[0])*scale+outcenter[0]).astype(np.int)
    y2hpgl=np.round((ys[1]-incenter[1])*scale+outcenter[1]).astype(np.int)
    fdhpgl.write("PU%d,%d;\n"%(x1hpgl,y1hpgl))
    fdhpgl.write("PD%d,%d;\n"%(x2hpgl,y2hpgl))
    fdhpgl.write("PU%d,%d;\n"%(x2hpgl,y2hpgl))

fdsvg.write('</svg>')
fdsvg.write("\n")
fdsvg.close()
fdhpgl.write("SP0;\n")
fdhpgl.close()
plt.show()

#fd=open(fbase+".hpgl",'w')
#fd.write("SP1;\n")
#for l in lines:
#    xs=np.round((l[0]-incenter[0])*scale+outcenter[0]).astype(np.int)
#    ys=np.round((l[1]-incenter[1])*scale+outcenter[1]).astype(np.int)
#    fd.write("PU%d,%d;\n"%(xs[0],ys[0]))
#    for x,y in zip(xs,ys):
#        fd.write("PD%d,%d;\n"%(x,y))
#    fd.write("PU%d,%d;\n"%(xs[-1],ys[-1]))
