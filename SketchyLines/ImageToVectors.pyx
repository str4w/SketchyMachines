#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ImageToHPGL
Copyright Rupert Brooks 2017
"""
import sys
sys.path.append("../Common")
import cv2
import numpy as np
import matplotlib.pyplot as plt
import itertools as it
import skimage.morphology as skm
from graph2 import Graph,replace_in_list,Edge
import time
import glob
import pickle


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

def jitter(a):
    return a+np.random.randn(len(a))*0.25

def linedist(l1,l2):
    dx1=l1[0][-1]-l2[0][0]
    dy1=l1[1][-1]-l2[1][0]
    dx2=l1[0][-1]-l2[0][-1]
    dy2=l1[1][-1]-l2[1][-1]
    d1=dx1*dx1+dy1*dy1
    d2=dx2*dx2+dy2*dy2
    if d1<=d2:
        return d1,False
    else:
        return d2,True

def condense_images(files,ratio,outfile):
    drawDebug=False
    zs=[cv2.imread(f,cv2.IMREAD_GRAYSCALE)/255.0 for f in files]
    for i in range(1,len(zs)):
        zs[0]+=zs[i]
    res=((zs[0]/len(zs)>ratio)*255).astype(np.uint8)
    print(res)
    cv2.imwrite(outfile,res)
 

def make_lines_from_images(files,crop):
    drawDebug=False
    lines=[]
    for f in files:
        Z=cv2.imread(f,cv2.IMREAD_GRAYSCALE)
        if crop is not None:
            Z[:crop[0][1],:]=0
            Z[crop[1][1]:,:]=0
            Z[:,:crop[0][0]]=0
            Z[:,crop[1][0]:]=0
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
    return lines

def organize_lines(lines):
    t1=time.clock()

    lines.sort(key=lambda x: -len(x[0]) )
    print ("Sorting lines: %f"%(time.clock()-t1))
    t1=time.clock()

    originallength=len(lines)
    available=[True]*originallength

    remaining=[originallength]
    finallines=[]
    minindex=0
    def popitem(idx,flip=False):
        assert(available[idx])
        if flip:
            lines[idx][0].reverse()
            lines[idx][1].reverse()
        finallines.append(lines[idx])
        available[idx]=False
        remaining[0]-=1
    
    popitem(minindex)
    counter=0
    while remaining[0]>0:
        minindex=None
        mindistance=999999999.9
        minflip=False
        for i,l in enumerate(lines):
            if available[i]:
                d,flip=linedist(finallines[-1],l)
                if d<mindistance:
                    mindistance=d
                    minindex=i
                    minflip=flip
                    if mindistance==0:
                        break;
        popitem(minindex,minflip)
        counter+=1
        if counter % 1000==0:
            print ("--- %d lines: %f"%(counter,time.clock()-t1))
            
    print ("Organized lines: %f"%(time.clock()-t1))

    assert(remaining[0]==0)
    assert(len(finallines)==originallength)
    return finallines



#fbase="SketchyEggOutput/frame_20180324T170312"
#files=sorted(glob.glob(fbase+"_*.png"))
#lines=make_lines_from_images(files)
#finallines=organize_lines(lines)

#print("There are %d elements in lines"%(len(finallines)))    
#fd=open(fbase+".pkl",'wb')
#pickle.dump(finallines,fd)
#plt.imshow(Z)
#lim=plt.axis()
#for l in lines[:300]:
#       plt.plot(l[1],l[0],'k-')
#plt.axis(lim)
#plt.title("Graph")
#plt.show()

#inextents =np.array([[0,0],[480,640]])
#outextents=np.array([[100,100],[8100,10100]])
#scale=min( (outextents[1,0]-outextents[0,0])/(inextents[1,0]-inextents[0,0]),  (outextents[1,1]-outextents[0,1])/(inextents[1,1]-inextents[0,1]))
#incenter=(inextents[1,:]+inextents[0,:])/2.0
#outcenter=(outextents[1,:]+outextents[0,:])/2.0
#fd=open(fbase+".hpgl",'w')
#fd.write("SP1;\n")
#for l in lines:
#    xs=np.round((l[0]-incenter[0])*scale+outcenter[0]).astype(np.int)
#    ys=np.round((l[1]-incenter[1])*scale+outcenter[1]).astype(np.int)
#    fd.write("PU%d,%d;\n"%(xs[0],ys[0]))
#    for x,y in zip(xs,ys):
#        fd.write("PD%d,%d;\n"%(x,y))
#    fd.write("PU%d,%d;\n"%(xs[-1],ys[-1]))
#fd.write("SP0;\n")

