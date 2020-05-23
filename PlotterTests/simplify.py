from __future__ import print_function
import sys
import argparse
import rdp

from line_tools import read_line_file, write_lines

parser=argparse.ArgumentParser()
parser.add_argument("--epsilon",type=float, default=1.0, help="filter jags smaller than this")
parser.add_argument("input",type=str, help="lines to simplify")
parser.add_argument("output",type=str, help="Output")
args=parser.parse_args()




lines, limits, max_pen=read_line_file(args.input)

#newlines=[(pen,rdp.rdp(line,args.epsilon)) for pen,line in lines ]
newlines=[]
countbefore=0
countafter=0
for i,( pen,line) in enumerate(lines):
  filtered=rdp.rdp(line,args.epsilon)
  countbefore+=len(line)
  countafter+=len(filtered)
  newlines.append((pen,filtered))
  #print(i,"/",len(lines))
print("Reduced",countbefore,"points to",countafter)
with open(args.output,'w') as fd:
    write_lines(fd,newlines)
