#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ImageToHPGL
Copyright Rupert Brooks 2017
"""
import sys
import os
parentdir=os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.join(parentdir,"Common"))   
import cv2
import numpy as np
import matplotlib.pyplot as plt
import itertools as it
import skimage.morphology as skm
from graph2 import Graph,replace_in_list,Edge
import time
import glob

fbase="Output/frame_20171002T075236"

def drawgraph(h):
    for e in h.edges:
       ys,xs=h.get_polyline(e)
       plt.plot(xs,ys,'k-')
    for n in h.nodes:
       i=h.vertices[n.vertex].y
       j=h.vertices[n.vertex].x
       c=len(n.el)
       if c==3:
         plt.plot(i,j,'r.')
       elif c==4:
         plt.plot(i,j,'ro')
       elif c>4:
         plt.plot(i,j,'r*')


drawDebug=False
lines=[]
f=sys.argv[1]
Z=cv2.imread(f,cv2.IMREAD_GRAYSCALE)

skel=skm.medial_axis(Z)
print("processing %s"%(f))

print("Generating graph...")
t1=time.clock()
nodes=[]
edges=[]
idx=np.ones_like(skel,dtype=np.int32)*-1
for i,j in  it.product(range(skel.shape[0]), range(skel.shape[1])):
    if skel[i,j]>0:
        idx[i,j]=len(nodes)
        nodes.append( (i,j) )
        # im sure to already have covered all the j's for i-1
        if j>0 and idx[i,j-1]>=0:
            edges.append( (idx[i,j-1],idx[i,j]) )
        if i>0:
            if j>0 and idx[i-1,j-1]>=0:
                edges.append( (idx[i-1,j-1],idx[i,j]) )
            if idx[i-1,j]>=0:
                edges.append( (idx[i-1,j],idx[i,j]) )
            if j<skel.shape[1]-1 and idx[i-1,j+1]>=0:
                edges.append( (idx[i-1,j+1],idx[i,j]) )
print("find nodes and edges: %f"%(time.clock()-t1))

g=Graph(nodes,edges)
print("graph: %f"%(time.clock()-t1))
print("Graph has %d nodes and %d edges"%(len(g.nodes),len(g.edges)))
print("Remove small tangles...")
t1=time.clock()
g.remove_3cycles()
print ("Remove tangles: %f"%(time.clock()-t1))
t1=time.clock()
g.remove_pseudonodes()
print ("Remove pseudonodes: %f"%(time.clock()-t1))
print("Graph has %d nodes and %d edges"%(len(g.nodes),len(g.edges)))
lines.extend([list(g.get_polyline(e)) for e in g.edges ])
if drawDebug:    
    plt.imshow(Z+skel)
    lim=plt.axis()
    drawgraph(g)
    plt.axis(lim)
    plt.title("Graph")
    plt.show()

print("There are %d elements in lines"%(len(lines)))
if drawDebug:
    plt.imshow(Z,cmap='gray')
    lim=plt.axis()
    for l in lines[:300]:
       plt.plot(l[1],l[0],'g-')
    plt.axis(lim)
    plt.title("Graph")
    plt.show()
    input("Press enter to continue")
with open(sys.argv[2],'w') as fd:
    for l in lines:
        for x,y in zip(*reversed(l)):
            fd.write("%f %f "%(x,-y))
        fd.write('\n')

