#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 22:40:48 2018

@author: rupert
"""
import argparse
parser=argparse.ArgumentParser()
parser.add_argument("--pens",type=int, default=1,help="Specify number of pens")
parser.add_argument("--number",type=int, default=10,help="Specify number of lines")
args=parser.parse_args()

pens=max(args.pens,1)

pen=0
print("PEN 0")

for i in range(args.number):
    if pens>1:
       pen=(pen+1)%pens
       print("PEN %d"%(pen))
    r=i+1.0
    print("%f %f %f %f"%(-r,-r,r,-r))
    print("%f %f %f %f"%( r, r,-r, r))
    print("%f %f %f %f"%(-r, r,-r,-r))
    print("%f %f %f %f"%( r,-r,r, r))
