"""
Sketchy Lines
Copyright Rupert Brooks 2017-2018
"""
import cv2
import numpy as np
import os
import sys
import time

from OpenCVApp import OpenCVApp

def adjust_gamma(image, gamma=1.0):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
 
	# apply gamma correction using the lookup table
	return cv2.LUT(image, table)

class SketchyLines(OpenCVApp):
    def __init__(self,videoDevice=0,basename="frame_"):
        super(SketchyLines,self).__init__("Sketchy Lines",videoDevice)
        self.basename=basename
        self.edgeCache=[]
        self.maxEdges=10
        self.outputDirectory="Output"
        
        self.showStats=False
        self.showAppTitle=True
        self.showHelpMenu=False
        self.fontSizeSmall=0.4
        self.fontThicknessSmall=1
        self.fontThicknessLarge=2
        self.fontSizeLarge=1.0
        self.font=cv2.FONT_HERSHEY_SIMPLEX
        self.statsColor=(255,0,0)
        self.titleColor=(0,0,0)
        self.menuColor=(255,255,255)
        
        
    def save_frames(self):
        if not os.path.exists(self.outputDirectory):
            os.makedirs(self.outputDirectory)
        timestamp=time.strftime("%Y%m%dT%H%M%S")
        framename=self.outputDirectory+"/"+self.basename + timestamp +".png" 
        print( "Saving "+framename)
        cv2.imwrite(framename,self.processedFrame)
        for i,e in enumerate(self.edgeCache):
            framename="%s/%s%s_%02d.png"%(self.outputDirectory,self.basename,timestamp,i)
            print( "Saving "+framename)
            cv2.imwrite(framename,e)

    def on_key(self,key):
        if   key == ord('f'): 
            self.save_frames()
        elif key == ord('h'): 
            self.showHelpMenu=not self.showHelpMenu
        elif key == ord('s'):     
            self.showStats=not self.showStats
        elif key == 27:
            return False
        
        return True
    
    def process_frame(self,frame):
       for _ in range(1):
           frame=cv2.bilateralFilter(frame,d=7,sigmaColor=9,sigmaSpace=7)
       gs=cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
       edges = np.zeros_like(gs)
       cv2.Canny(frame,15000,3000,edges,7,False)

       self.edgeCache.append(edges)
       if len(self.edgeCache)>self.maxEdges:
           self.edgeCache.pop(0)
       self.sumimage=np.zeros_like(edges,dtype=np.float64)
       for e in self.edgeCache:
           self.sumimage+=e
       self.edgeout=np.uint8(np.minimum(2.0*self.sumimage/len(self.edgeCache),255))
#       print (frame.shape)
       
       outimg=np.minimum(cv2.cvtColor((255-self.edgeout),cv2.COLOR_GRAY2RGB),adjust_gamma(frame,2.0))
       return outimg
    
    def overlay(self,frame):
        resultFrame=frame.copy()
        if self.showStats:
            fpsText="FPS: %3.1f"%(self.fps)
            szfps,_=cv2.getTextSize(fpsText,self.font,self.fontSizeSmall,self.fontThicknessSmall)
            edgeText="Edge Px: %d"%(np.sum(self.sumimage))
            szedge,_=cv2.getTextSize(edgeText,self.font,self.fontSizeSmall,self.fontThicknessSmall)
            posX=resultFrame.shape[1]-max([szfps[0],szedge[0]])-10
            cv2.putText(resultFrame,fpsText,
                        (posX, int(resultFrame.shape[0]*0.85)),
                        self.font,self.fontSizeSmall,self.statsColor,self.fontThicknessSmall)
            cv2.putText(resultFrame,edgeText,
                        (posX, int(resultFrame.shape[0]*0.9)),
                        self.font,self.fontSizeSmall,self.statsColor,self.fontThicknessSmall)
        if self.showAppTitle:
            sz,_=cv2.getTextSize("Sketchy Lines",self.font,self.fontSizeLarge,self.fontThicknessLarge)
            cv2.putText(resultFrame,"Sketchy Lines",
                        (int(resultFrame.shape[1]*0.5-sz[0]*0.5), int(resultFrame.shape[0]*0.05)),
                        self.font,self.fontSizeLarge,self.titleColor,self.fontThicknessLarge)
            sz,_=cv2.getTextSize("Press h for help",self.font,self.fontSizeSmall,self.fontThicknessSmall)
            cv2.putText(resultFrame,"Press h for help",
                        (int(resultFrame.shape[1]*0.5-sz[0]*0.5), int(resultFrame.shape[0]*0.1)),
                        self.font,self.fontSizeSmall,self.titleColor,self.fontThicknessSmall)
        if self.showHelpMenu:
            cv2.putText(resultFrame,"h - show / hide this menu",
                        (int(resultFrame.shape[1]*0.1), int(resultFrame.shape[0]*0.2)),
                        self.font,self.fontSizeSmall,self.menuColor,self.fontThicknessSmall)
            cv2.putText(resultFrame,"f - save current set of frames",
                        (int(resultFrame.shape[1]*0.1), int(resultFrame.shape[0]*0.25)),
                        self.font,self.fontSizeSmall,self.menuColor,self.fontThicknessSmall)
            cv2.putText(resultFrame,"s - show / hide stats",
                        (int(resultFrame.shape[1]*0.1), int(resultFrame.shape[0]*0.3)),
                        self.font,self.fontSizeSmall,self.menuColor,self.fontThicknessSmall)
            cv2.putText(resultFrame,"ESC - quit",
                        (int(resultFrame.shape[1]*0.1), int(resultFrame.shape[0]*0.35)),
                        self.font,self.fontSizeSmall,self.menuColor,self.fontThicknessSmall)
        return resultFrame



if __name__ == '__main__':
    
    App=SketchyLines()
    App.run()
    

