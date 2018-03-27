#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright 2018 Rupert Brooks

Simple OpenCV app with onscreen overlay

@author: rupert
"""

import cv2
import numpy as np
import time


class OpenCVApp:
    def __init__(self,windowTitle="Someone forgot to set a window title",videoDevice=0,delay=3):
        self.windowTitle=windowTitle
        self.videoDevice=videoDevice
        self.delay=int(delay)
        self.fps=0.
        pass

    def compute_fps(self):
        now=time.time()
        deltaTime=now-self.lastTime
        self.frameTimesSum-=self.frameTimes[self.frameTimesIndex]
        self.frameTimes[self.frameTimesIndex]=deltaTime
        self.frameTimesSum+=self.frameTimes[self.frameTimesIndex]
        self.frameTimesIndex=(self.frameTimesIndex+1)%len(self.frameTimes)
        self.lastTime=now
        self.fps=len(self.frameTimes)/self.frameTimesSum
 
    def on_key(self,key):
        if key != 255:
            if key==27:
                return False
            else:
                print("OpenCVApp: The key was",key)
                
        return True
    
    def process_frame(self,frame):
        return frame

    def overlay(self,frame):
        resultFrame=frame.copy()
        cv2.putText(resultFrame,"FPS: %3.1f"%(self.fps),
                    (int(resultFrame.shape[0]*0.8), int(resultFrame.shape[1]*0.05)),
                    cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,255))
        return resultFrame

    def run(self):
        cv2.namedWindow(self.windowTitle)
        self.capture = cv2.VideoCapture(self.videoDevice)
        if self.capture is None or not self.capture.isOpened():
            print ('OpenCVApp: Error: unable to open video source: %s'%(str(self.videoDevice)))
            cv2.destroyWindow(self.windowTitle)
            return
        # sometimes cameras don't init right away, read until init.
        startTime=time.time()
        self.frameTimes=[0.]*10
        self.frameTimesSum=0.
        self.frameTimesIndex=0
        ret = False
        while(not ret):
            ret,frame = self.capture.read()
            if time.time()-startTime > 6.:
                print ('OpenCVApp: Error: Unable to get a frame from the video source after 6 seconds, giving up')
                return 

        loop = True
        self.lastTime=time.time()
        while(loop):
            ret,self.rawFrame = self.capture.read()
            if (self.rawFrame is None):
                break
       
            self.processedFrame=self.process_frame(self.rawFrame)
            self.overlayFrame=self.overlay(self.processedFrame)
            cv2.imshow(self.windowTitle,self.overlayFrame)
       
            char = cv2.waitKey(self.delay)
            loop=self.on_key(char)
            self.compute_fps()
            
        cv2.destroyWindow(self.windowTitle)

    


if __name__ == '__main__':
    # simple test here.
    App=OpenCVApp("Test OpenCVApp")
    App.run()