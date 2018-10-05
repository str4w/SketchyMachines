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

file="../SourceMaterial/hops-gray.png"
    
gs=cv2.imread(file,cv2.IMREAD_GRAYSCALE)
gshalf=cv2.resize(gs,(0,0),fx=0.5,fy=0.5)
#greenhalf=cv2.resize(hops_img[...,1],(0,0),fx=0.5,fy=0.5)
gshalffloat=gshalf/255.0

ksize=50
im1=cv2.GaussianBlur(gshalffloat,(0,0),ksize)
im2=cv2.GaussianBlur((gshalffloat-im1)**2,(0,0),ksize)

#plt.imshow(im2,cmap='gray')

enhanced=(np.clip((gshalffloat-im1)/(.5+im2)+0.5,0,1)*255).astype(np.uint8)

edges=np.zeros_like(enhanced)
edges2=np.zeros_like(enhanced)
edges=cv2.Canny(enhanced,25000,500,edges,7,True)+cv2.Canny(cv2.GaussianBlur(cv2.resize(gs,(0,0),fx=0.5,fy=0.5),(0,0),1),100,1,edges2,3,False)
edges[edges>100]=255
edges=cv2.GaussianBlur(edges,(0,0),1)
plt.imshow(edges)
plt.show()
edges[edges>100]=255
edges[edges<=100]=0
#edges=(255-edges)
#edges[greenhalf<40]=128
#print(edges.dtype,edges.shape,np.max(edges))
#fig=plt.figure(figsize=(14,9))
#plt.imshow(edges,cmap='gray')
#plt.show()

#edges = np.zeros_like(gs)
#cv2.Canny(gs,15000,2000,edges,7,False)

#ImageToVectors.condense_images(files,0.4,fbase+"_edges.png")
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

fd=open("hops2.lines",'w')
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
