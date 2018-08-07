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

colorstrings=["#000000","#FF0000","#00FF00","#0000FF","#FFFF00","#FF00FF","#00FFFF"]

if len(sys.argv) != 7 or getExtension(sys.argv[6]) is None:
    print("Usage: lines2render.py inputfile lowx lowy highx highy outputfile")
    print("       outputfile should end in either .hpgl or .svg")
else:
    limits=[1.e30,1.e30,-1.e30,-1.e30]
    fd=open(sys.argv[1])
    lines=[]
    pointscount=0
    currentPen=0
    maxPen=0
    for line in fd:
       if line[:3]=="PEN":
          tmp=line.split()
          assert(len(tmp)==2)
          currentPen=int(tmp[1])
          assert(currentPen>=0)
          maxPen=max(maxPen,currentPen)
       else:
          z=list(map(float,line.split()))
          try:
              assert(len(z)%2==0)
          except:
              print(z)
              raise
          coords=[(z[i],z[i+1]) for i in range(0,len(z),2)]
          lines.append((currentPen,coords))
          for x,y in coords:
              pointscount+=1
              limits[0]=min(x,limits[0])
              limits[1]=min(y,limits[1])
              limits[2]=max(x,limits[2])
              limits[3]=max(y,limits[3])
    print("Found %d lines with %d points.  Extent (%f,%f)->(%f,%f)"%(len(lines),pointscount,limits[0],limits[1],limits[2],limits[3]))
    print("Found a maximum pen of",maxPen)
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
           for i,(pen,line) in enumerate(lines):
              if len(line)>1:
                 pts=list(map(xform,line))
                 ofd.write('   <path\n')
                 ofd.write('      id="path%d"\n'%(i,))
                 ofd.write('      style="stroke: '+colorstrings[pen%len(colorstrings)]+'; fill:none;"\n')
                 ofd.write('      d="m %f,%f '%pts[0])
                 for i in range(1,len(pts)):
                    ofd.write("%f,%f "%(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]))
                 ofd.write('" />\n')
           ofd.write('</svg>\n')
    elif getExtension(sys.argv[6]) == "hpgl":
        print("Writing as hpgl")
        with open(sys.argv[6],'w') as ofd:
           cp=-1
           ofd.write("IN;")
           def xform(p):
              return int(0.5+olimits[0]+s*(p[0]-limits[0])),int(0.5+olimits[1]+s*(p[1]-limits[1]))
           for pen,line in lines:
              if pen != cp:
                 ofd.write("SP%d;\n"%(pen+1,))
                 cp=pen
              if len(line)>1:
                 pts=list(map(xform,line))
                 ofd.write("PU%d,%d;"%pts[0])
                 ofd.write("PD%d,%d"%pts[1])
                 for p in pts[2:]:
                    ofd.write(",%d,%d"%p)
                 ofd.write(";\n")
           ofd.write("SP0;")
    

       
