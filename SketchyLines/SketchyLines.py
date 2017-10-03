"""
Sketchy Lines
Copyright Rupert Brooks 2017
"""
import cv2
import numpy as np
import sys
import time

def adjust_gamma(image, gamma=1.0):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
 
	# apply gamma correction using the lookup table
	return cv2.LUT(image, table)


if __name__ == '__main__':
    windowName="SketchyLines"
    cv2.namedWindow(windowName)
    videodevice=0

    g_capture = cv2.VideoCapture(videodevice)
    if g_capture is None or not g_capture.isOpened():
        print ('Warning: unable to open video source: %s'%(str(videodevice)))
    ret = False
    while(not ret):
       ret,frame = g_capture.read()

    loop = True

    basename="frame_"
    if(len(sys.argv)>1):
      basename=sys.argv[1]
    edgecache=[]
    maxedges=10
    while(loop):
       ret,frame = g_capture.read()
       if (frame is None):
          break
       for _ in range(1):
           frame=cv2.bilateralFilter(frame,d=7,sigmaColor=9,sigmaSpace=7)
       edges = np.zeros_like(cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY))
       cv2.Canny(frame,15000,3000,edges,7,False)
       gs=cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)

       edgecache.append(edges)
       if len(edgecache)>maxedges:
           edgecache.pop(0)
       edgeout=np.zeros_like(edges)
       sumimage=np.zeros_like(edges,dtype=np.float64)
       for e in edgecache:
           sumimage+=e
       edgeout=np.uint8(np.minimum(2.0*sumimage/len(edgecache),255))
#       print (frame.shape)
       
       outimg=np.minimum(cv2.cvtColor((255-edgeout),cv2.COLOR_GRAY2RGB),adjust_gamma(frame,2.0))
#       outimg=cv2.cvtColor((255-edgeout),cv2.COLOR_GRAY2RGB)
#       print(outimg.shape)
       cv2.imshow(windowName,outimg)
       
       char = cv2.waitKey(3)
       if (char != -1):
          if(char == 102):
             timestamp=time.strftime("%Y%m%dT%H%M%S")
             framename=basename + timestamp +".png" 
             print( "Saving "+framename)
             cv2.imwrite(framename,outimg)
             for i,e in enumerate(edgecache):
                 framename="%s%s_%d.png"%(basename,timestamp,i)
                 print( "Saving "+framename)
                 cv2.imwrite(framename,e)
          elif (char == 27):
             loop = False
    cv2.destroyWindow(windowName)

