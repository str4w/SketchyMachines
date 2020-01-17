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

newlines=[(pen,rdp.rdp(line,args.epsilon)) for pen,line in lines ]
with open(args.output,'w') as fd:
    write_lines(fd,newlines)
