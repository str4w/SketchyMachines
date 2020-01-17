from __future__ import print_function
import sys
sys.path.append("SketchyLines")
sys.path.append("Common")
import pyximport; pyximport.install()
import ImageToVectors
import argparse
from collections import defaultdict

from line_tools import read_line_file, write_lines

parser=argparse.ArgumentParser()
parser.add_argument("input",type=str, help="lines to organize")
parser.add_argument("output",type=str, help="Output")
args=parser.parse_args()




lines, limits, max_pen=read_line_file(args.input)
pen_lines=defaultdict(list)
for pen,line in lines:
    z=list(zip(*line))
    pen_lines[pen].append([list(z[0]),list(z[1])])

for pen in pen_lines.keys():
    print("Sorting lines for pen",pen)
    newlines=ImageToVectors.organize_lines(pen_lines[pen])
    pen_lines[pen]=[ list(zip(*line)) for line in newlines]

newlines=[]
for pen in pen_lines.keys():
    for line in pen_lines[pen]:
        newlines.append((pen,line))


with open(args.output,'w') as fd:
    write_lines(fd,newlines)