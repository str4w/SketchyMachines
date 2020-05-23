import numpy as np
def read_line_file(filename):
    with open(filename) as fd:
        limits=[1.e30,1.e30,-1.e30,-1.e30]
        lines=[]
        pointscount=0
        currentPen=0
        maxPen=0
        for line in fd:
            if len(line.strip())==0:
                continue
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
    return lines,limits,maxPen

def point_distance(p1,p2):
    return np.sqrt(np.sum((np.array(p1)-np.array(p2))**2))
def line_distance(l1,l2):
    pi0=l1[0]
    pi1=l1[-1]
    pj0=l2[0]
    pj1=l2[-1]
    return min(point_distance(pi0,pj0),
               point_distance(pi0,pj1),
               point_distance(pi1,pj0),
               point_distance(pi1,pj1))

def write_lines(fd,lines):
    currentPen=-1
    for pen,line in lines:
        if pen != currentPen:
            currentPen=pen
            fd.write('PEN %d\n'%currentPen)
        if len(line)>0:
            fd.write("%f %f"%tuple(line[0]))
            for xy in line[1:]:
                fd.write(" %f %f"%tuple(xy))
            fd.write('\n')
