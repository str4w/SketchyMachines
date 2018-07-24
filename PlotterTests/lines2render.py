from __future__ import print_function
import sys

def getExtension(s):
   A=s.split('.')
   if len(A)>1:
      if A[-1].lower() =="svg":
         return "svg"
      elif A[-1].lower() == "hpgl":
         return "hpgl"
   return None

if len(sys.argv) != 7 or getExtension(sys.argv[6]) is None:
    print("Usage: lines2render.py inputfile lowx lowy highx highy outputfile")
    print("       outputfile should end in either .hpgl or .svg")
else:
    limits=[1.e30,1.e30,-1.e30,-1.e30]
    fd=open(sys.argv[1])
    lines=[]
    pointscount=0
    for line in fd:
       z=list(map(float,line.split()))
       try:
           assert(len(z)%2==0)
       except:
           print(z)
           raise
       coords=[(z[i],z[i+1]) for i in range(0,len(z),2)]
       lines.append(coords)
       for x,y in coords:
           pointscount+=1
           limits[0]=min(x,limits[0])
           limits[1]=min(y,limits[1])
           limits[2]=max(x,limits[2])
           limits[3]=max(y,limits[3])
    print("Found %d lines with %d points.  Extent (%f,%f)->(%f,%f)"%(len(lines),pointscount,limits[0],limits[1],limits[2],limits[3]))
    olimits=list(map(float,sys.argv[2:6]))
    s=min((olimits[2]-olimits[0])/(limits[2]-limits[0]),(olimits[3]-olimits[1])/(limits[3]-limits[1]))
    if getExtension(sys.argv[6]) == "svg":
        print("Writing as svg")
        with open(sys.argv[6],'w') as ofd:
           ofd.write(
"""<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
   xmlns:dc="http://purl.org/dc/elements/1.1/"
   xmlns:cc="http://creativecommons.org/ns#"
   xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
   xmlns:svg="http://www.w3.org/2000/svg"
   xmlns="http://www.w3.org/2000/svg"
   version="1.1"
   id="svg2">
  <metadata
     id="metadata3214">
    <rdf:RDF>
      <cc:Work
         rdf:about="">
        <dc:format>image/svg+xml</dc:format>
        <dc:type
           rdf:resource="http://purl.org/dc/dcmitype/StillImage" />
        <dc:title></dc:title>
      </cc:Work>
    </rdf:RDF>
  </metadata>
  <defs
     id="defs3212" />
"""
)
           def xform(p):
              return olimits[0]+s*(p[0]-limits[0]),olimits[1]+s*(p[1]-limits[1])
           for i,line in enumerate(lines):
              if len(line)>1:
                 pts=list(map(xform,line))
                 ofd.write('   <path\n')
                 ofd.write('      id="path%d"\n'%(i,))
                 ofd.write('      style="stroke: #000000; fill:none;"\n')
                 ofd.write('      d="m %f,%f '%pts[0])
                 for i in range(1,len(pts)):
                    ofd.write("%f,%f "%(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]))
                 ofd.write('" />\n')
           ofd.write('</svg>\n')
    elif getExtension(sys.argv[6]) == "hpgl":
        print("Writing as hpgl")
        with open(sys.argv[6],'w') as ofd:
           ofd.write("IN;SP1;")
           def xform(p):
              return int(0.5+olimits[0]+s*(p[0]-limits[0])),int(0.5+olimits[1]+s*(p[1]-limits[1]))
           for line in lines:
              if len(line)>1:
                 pts=list(map(xform,line))
                 ofd.write("PU%d,%d;"%pts[0])
                 ofd.write("PD%d,%d"%pts[0])
                 for p in pts[1:]:
                    ofd.write(",%d,%d"%p)
                 ofd.write(";")
           ofd.write("SP0;")
    

       
