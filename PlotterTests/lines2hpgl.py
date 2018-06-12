from __future__ import print_function
import sys
if len(sys.argv) != 7:
    print("Usage: lines2hpgl.py inputfile lowx lowy highx highy outputfile")
else:
    limits=[1.e30,1.e30,-1.e30,-1.e30]
    fd=open(sys.argv[1])
    lines=[]
    pointscount=0
    for line in fd:
       z=map(float,line.split())
       assert(len(z)%2==0)
       coords=[(z[i],z[i+1]) for i in range(0,len(z),2)]
       lines.append(coords)
       for x,y in coords:
           pointscount+=1
           limits[0]=min(x,limits[0])
           limits[1]=min(y,limits[1])
           limits[2]=max(x,limits[2])
           limits[3]=max(y,limits[3])
    print("Found %d lines with %d points.  Extent (%f,%f)->(%f,%f)"%(len(lines),pointscount,limits[0],limits[1],limits[2],limits[3]))
    olimits=map(float,sys.argv[2:6])
    s=min((olimits[2]-olimits[0])/(limits[2]-limits[0]),(olimits[3]-olimits[1])/(limits[3]-limits[1]))
    ofd=open(sys.argv[6],'w')
    ofd.write("IN;SP1;")
    def xform(p):
       return int(0.5+olimits[0]+s*(p[0]-limits[0])),int(0.5+olimits[1]+s*(p[1]-limits[1]))
    for line in lines:
       if len(line)>1:
	   pts=map(xform,line)
       	   ofd.write("PU%d,%d;"%pts[0])
           ofd.write("PD%d,%d"%pts[0])
           for p in pts[1:]:
              ofd.write(",%d,%d"%p)
           ofd.write(";")
    ofd.write("SP0;")
    

       
