"""
Sketchy Egg
Copyright Rupert Brooks 2017-2018
"""
import cv2
import numpy as np
import os
import sys
import time

import matplotlib.pyplot as plt
import itertools as it
import skimage.morphology as skm

sys.path.append("../Common")
from graph2 import Graph,replace_in_list,Edge
from OpenCVApp import OpenCVApp

def adjust_gamma(image, gamma=1.0):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
 
	# apply gamma correction using the lookup table
	return cv2.LUT(image, table)

class SketchyEgg(OpenCVApp):
    def __init__(self,videoDevice=0,basename="frame_"):
        super(SketchyEgg,self).__init__("Sketchy Egg",videoDevice)
        self.basename=basename
        self.edgeCache=[]
        self.maxEdges=10
        self.outputDirectory="SketchyEggOutput"
        
        self.CannyHigh=15000
        self.CannyLow=3000
        self.CannyFilter=7
        self.keepfactor=10
        
        self.showStats=False
        self.showAppTitle=True
        self.showHelpMenu=False
        self.showRaw=False
        self.fontSizeSmall=0.4
        self.fontThicknessSmall=1
        self.fontThicknessLarge=2
        self.fontSizeLarge=1.0
        self.font=cv2.FONT_HERSHEY_SIMPLEX
        self.statsColor=(255,0,0)
        self.titleColor=(0,0,0)
        self.menuColor=(255,0,255)
    def generate_plot(self): 
        print("not written yet, cof")
        
    def save_frames(self):
        if not os.path.exists(self.outputDirectory):
            os.makedirs(self.outputDirectory)
        timestamp=time.strftime("%Y%m%dT%H%M%S")
        framename=self.outputDirectory+"/"+self.basename + timestamp +".png" 
        print( "Saving "+framename)
        cv2.imwrite(framename,self.processedFrame)
        framename=self.outputDirectory+"/"+self.basename + timestamp +"_edges.png" 
        print( "Saving "+framename)
        cv2.imwrite(framename,self.edgeout)
        for i,e in enumerate(self.edgeCache):
            framename="%s/%s%s_%02d.png"%(self.outputDirectory,self.basename,timestamp,i)
            print( "Saving "+framename)
            cv2.imwrite(framename,np.minimum(e,self.edgeout))

    def on_key(self,key):
        if   key == ord('f'): 
            self.save_frames()
        if   key == ord('p'): 
            self.generate_plot()
        elif key == ord('h'): 
            self.showHelpMenu=not self.showHelpMenu
        elif key == ord('s'):     
            self.showStats=not self.showStats
        elif key == ord('r'):     
            self.showRaw=not self.showRaw
        elif key == ord('b'):     
            br=self.capture.get(cv2.CAP_PROP_BRIGHTNESS)
            print("Current Brightness",br)
            self.capture.set(cv2.CAP_PROP_BRIGHTNESS,br-0.05)
        elif key == ord('B'):     
            br=self.capture.get(cv2.CAP_PROP_BRIGHTNESS)
            print("Current Brightness",br)
            self.capture.set(cv2.CAP_PROP_BRIGHTNESS,br+0.05)
        elif key == ord('c'):     
            ct=self.capture.get(cv2.CAP_PROP_CONTRAST)
            print("Current Contrast",ct)
            self.capture.set(cv2.CAP_PROP_CONTRAST,ct-0.05)
        elif key == ord('C'):     
            ct=self.capture.get(cv2.CAP_PROP_CONTRAST)
            print("Current Contrast",ct)
            self.capture.set(cv2.CAP_PROP_CONTRAST,ct+0.05)
        elif key == ord('k'):     
            self.keepfactor-=1
            print("Current keep factor",self.keepfactor)
        elif key == ord('K'):     
            self.keepfactor+=1
            print("Current keep factor",self.keepfactor)
        elif key == ord('1'):     
            self.CannyHigh-=500
            print("Current Canny High",self.CannyHigh)
        elif key == ord('2'):     
            self.CannyHigh+=500
            print("Current Canny High",self.CannyHigh)
        elif key == ord('3'):     
            self.CannyLow-=500
            print("Current Canny Low",self.CannyLow)
        elif key == ord('4'):     
            self.CannyLow+=500
            print("Current Canny Low",self.CannyLow)
        elif key == 27:
            return False
        
        return True
#    0. CV_CAP_PROP_POS_MSEC Current position of the video file in milliseconds.
#1. CV_CAP_PROP_POS_FRAMES 0-based index of the frame to be decoded/captured next.
#3. CV_CAP_PROP_POS_AVI_RATIO Relative position of the video file
#4. CV_CAP_PROP_FRAME_WIDTH Width of the frames in the video stream.
#5. CV_CAP_PROP_FRAME_HEIGHT Height of the frames in the video stream.
#6. CV_CAP_PROP_FPS Frame rate.
#7. CV_CAP_PROP_FOURCC 4-character code of codec.
#8. CV_CAP_PROP_FRAME_COUNT Number of frames in the video file.
#9. CV_CAP_PROP_FORMAT Format of the Mat objects returned by retrieve() .
#10. CV_CAP_PROP_MODE Backend-specific value indicating the current capture mode.
#11. CV_CAP_PROP_BRIGHTNESS Brightness of the image (only for cameras).
#12. CV_CAP_PROP_CONTRAST Contrast of the image (only for cameras).
#13. CV_CAP_PROP_SATURATION Saturation of the image (only for cameras).
#14. CV_CAP_PROP_HUE Hue of the image (only for cameras).
#15. CV_CAP_PROP_GAIN Gain of the image (only for cameras).
#16. CV_CAP_PROP_EXPOSURE Exposure (only for cameras).
#17. CV_CAP_PROP_CONVERT_RGB Boolean flags indicating whether images should be converted to RGB.
#18. CV_CAP_PROP_WHITE_BALANCE Currently unsupported
#19. CV_CAP_PROP_RECTIFICATION Rectification flag for stereo cameras (note: only supported by DC1394 v 2.x backend currently)
    def process_frame(self,frame):
       for _ in range(1):
           frame=cv2.bilateralFilter(frame,d=7,sigmaColor=9,sigmaSpace=7)
       gs=cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
       edges = np.zeros_like(gs)
       cv2.Canny(frame,self.CannyHigh,self.CannyLow,edges,self.CannyFilter,False)

       self.edgeCache.append(edges)
       if len(self.edgeCache)>self.maxEdges:
           self.edgeCache.pop(0)
       self.sumimage=np.zeros_like(edges,dtype=np.float64)
       for e in self.edgeCache:
           self.sumimage+=e
       #self.sumimage=np.maximum(self.sumimage-len(self.edgeCache)/2.0,0)
       self.edgeout=np.uint8(self.sumimage>len(self.edgeCache)*255*(10-self.keepfactor)/10)*255 
       #np.uint8(np.minimum(4.0*self.sumimage/len(self.edgeCache),255))
#       print (frame.shape)
       
       outimg=cv2.cvtColor((255-self.edgeout),cv2.COLOR_GRAY2RGB)
       if self.showRaw:
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
            sz,_=cv2.getTextSize("Sketchy Egg",self.font,self.fontSizeLarge,self.fontThicknessLarge)
            cv2.putText(resultFrame,"Sketchy Egg",
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
            cv2.putText(resultFrame,"p - generate plot",
                        (int(resultFrame.shape[1]*0.1), int(resultFrame.shape[0]*0.3)),
                        self.font,self.fontSizeSmall,self.menuColor,self.fontThicknessSmall)
            cv2.putText(resultFrame,"s - show / hide stats",
                        (int(resultFrame.shape[1]*0.1), int(resultFrame.shape[0]*0.35)),
                        self.font,self.fontSizeSmall,self.menuColor,self.fontThicknessSmall)
            cv2.putText(resultFrame,"ESC - quit",
                        (int(resultFrame.shape[1]*0.1), int(resultFrame.shape[0]*0.4)),
                        self.font,self.fontSizeSmall,self.menuColor,self.fontThicknessSmall)
        return resultFrame



if __name__ == '__main__':
    
    App=SketchyEgg()
    App.run()
    #del App
    

