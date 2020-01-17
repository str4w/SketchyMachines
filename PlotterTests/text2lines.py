from __future__ import print_function
import sys
import argparse
import ThirdParty.hersheydata as hd
import numpy as np


parser=argparse.ArgumentParser()
parser.add_argument("--xkern",type=float, default=0.,help="added to xspacing, tweaks letter spacing")
parser.add_argument("--justification",type=str, default="left", help="left, right or centre")
parser.add_argument("--line_spacing",type=float, default=1., help="Spacing between lines")
parser.add_argument("--pen",type=int, default=0, help="Pen number to use")
parser.add_argument("font",type=str,help="Font to use")
parser.add_argument("input",type=str, help="Text to render")
parser.add_argument("outputfile",type=str, help="Output")
args=parser.parse_args()

def parse(pathString):
    lines=[]
    z=pathString.split()
    midpoint=float(z[0])
    offset=float(z[1])
    if len(z)<3:
        return lines,midpoint,offset
    assert(z[2]=='M')
    z=z[2:]
    assert(len(z)%3==0)
    idx=0
    line=[]
    while idx<len(z):
        key=z[idx]
        x=float(z[idx+1])
        y=float(z[idx+2])
        idx+=3
        if key=='M':
            if len(line)>0:
                lines.append(line)
            line=[]
            line.append((x,y))
        else:
            assert (key=='L')
            line.append((x,y))
    if len(line)>0:
        lines.append(line)
    return lines,midpoint,offset
try:
    fs=eval('hd.'+args.font)
except:
    print("Unknown font",args.font)
    print("Valid fonts are:")
    for f in dir(hd):
        if f[0]!='_':
            print(f)
    parser.print_help()
    exit()
    

yspacing=40.*args.line_spacing
with open(args.input) as fd:
    paragraph=fd.read()

paralines=paragraph.split("\n")
ypos=0
plotlines=[]
plotxpos=[]
for line in paralines:
    plotrow=[]
    xpos=0
    for character in line:
        fontlines,minx,maxx=parse(fs[ord(character)-32])
        charlines=[]
        for fontline in fontlines:
            xs,ys=zip(*fontline)
            plotrow.append((np.array(xs)-minx+xpos,-1.*np.array(ys)+ypos))
            
        
        xpos+=maxx-minx+args.xkern
    plotlines.append(plotrow)
    plotxpos.append(xpos-args.xkern)
    ypos-=yspacing
if args.justification=="left":
    pass
elif args.justification=="center" or args.justification == "centre":
    for i,xpos in enumerate(plotxpos):
        for xs,ys in plotlines[i]:
            xs-=xpos/2.
elif args.justification=="right":
    for i,xpos in enumerate(plotxpos):
        for xs,ys in plotlines[i]:
            xs-=xpos
else:
    raise Exception("Unknown justification %s"%justification)
        
with open(args.outputfile,'w') as fd:
    fd.write("PEN %d\n"%args.pen)
    for row in plotlines:
        for line in row:
            for xy in zip(*line):
                fd.write("%f %f "%xy)
            fd.write("\n")

