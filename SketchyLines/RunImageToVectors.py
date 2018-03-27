#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ImageToHPGL
Copyright Rupert Brooks 2017
"""
import glob
import pickle
import pyximport; pyximport.install()
import ImageToVectors #as i2v # import make_lines_from_images,organize_lines

fbase="SketchyEggOutput/frame_20180324T170312" # rupe
fbase="SketchyEggOutput/frame_20180325T165316"
files=sorted(glob.glob(fbase+"_edges.png"))
lines=ImageToVectors.make_lines_from_images(files,[(90,120),(556,442)])
finallines=ImageToVectors.organize_lines(lines)

#lines=[ (jitter(a),jitter(b)) for a,b in lines]
print("There are %d elements in lines"%(len(finallines)))

#for i,l in enumerate(finallines):
#    if i==50:
#        break
#    print("Line",i,"length",len(l[0]),(l[0][0],l[1][0]),(l[0][-1],l[1][-1]))
    
fd=open(fbase+"_a.pkl",'wb')
pickle.dump(finallines,fd)
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

