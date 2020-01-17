from __future__ import print_function
import sys
import argparse

from line_tools import read_line_file, write_lines

parser=argparse.ArgumentParser()
parser.add_argument("--fix_aspect",action="store_true",help="fix aspect ratio of composed drawing")
parser.add_argument("--reverse_order",action="store_true",help="Draw addition before base drawing")
parser.add_argument("--pen_shift",type=int, default=0, help="Shift the pens in the addition by this")
parser.add_argument("--scale",type=float, default=0, help="Use a fixed and specified scale")
parser.add_argument("base",type=str, help="Base drawing of lines")
parser.add_argument("x_low",type=float, help="Lower X coord of output box")
parser.add_argument("y_low",type=float, help="Lower Y coord of output box")
parser.add_argument("x_high",type=float, help="Upper X coord of output box")
parser.add_argument("y_high",type=float, help="Upper Y coord of output box")
parser.add_argument("addition",type=str, help="Drawing to add to the base")
parser.add_argument("outputfile",type=str, help="Output")
args=parser.parse_args()




base_lines, base_limits, base_max_pen=read_line_file(args.base)
add_lines, add_limits, add_max_pen=read_line_file(args.addition)

print("Base file has %d lines, max pen %d.  Extent (%f,%f)->(%f,%f)"%(len(base_lines),base_max_pen,
                                                     base_limits[0],base_limits[1],base_limits[2],base_limits[3]))
print("Add  file has %d lines, max pen %d.  Extent (%f,%f)->(%f,%f)"%(len(add_lines),add_max_pen,
                                                     add_limits[0],add_limits[1],add_limits[2],add_limits[3]))
base_extent=(base_limits[2]-base_limits[0],base_limits[3]-base_limits[1])
base_centre=((base_limits[2]+base_limits[0])/2.,(base_limits[3]+base_limits[1])/2.)
add_extent=(add_limits[2]-add_limits[0],add_limits[3]-add_limits[1])
add_centre=((add_limits[2]+add_limits[0])/2.,(add_limits[3]+add_limits[1])/2.)
#olimits=[args.x_low,args.y_low,args.x_high.,args.y_high]
#print("Extents",base_extent,add_extent)
#print("args",args.x_high,args.x_low,args.y_high,args.y_low)
if args.scale>0:
    sx=args.scale
    sy=args.scale
else:
    sx,sy=(args.x_high-args.x_low)*base_extent[0]/add_extent[0],(args.y_high-args.y_low)*base_extent[1]/add_extent[1]
    #print("SX",sx,"SY",sy)
    if args.fix_aspect:
        sx=min(sx,sy)
        sy=sx
add_new_centre=(0.5*(args.x_high+args.x_low)*base_extent[0]+base_limits[0],
                0.5*(args.y_high+args.y_low)*base_extent[1]+base_limits[1])
def xform(p):
    return (p[0]-add_centre[0])*sx+add_new_centre[0],(p[1]-add_centre[1])*sy+add_new_centre[1]

add_transformed_lines=[(pen+args.pen_shift,list(map(xform,lines))) for pen,lines in add_lines]


        
with open(args.outputfile,'w') as fd:
    if args.reverse_order:
        write_lines(fd,add_transformed_lines)
        write_lines(fd,base_lines)
    else:
        write_lines(fd,base_lines)
        write_lines(fd,add_transformed_lines)
