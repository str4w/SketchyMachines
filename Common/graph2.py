# -*- coding: utf-8 -*-
"""
Copyright Rupert Brooks 2017

A class representing a graph embedded in R2
"""

def replace_in_list(A,x,y):
    count=0
    for i in range(len(A)):
        if A[i] == x:
            A[i] = y
            count +=1
    return count

class Vertex:
    def __init__(self,p):
        self.x=p[0]
        self.y=p[1]
class Node:
    def __init__(self,v):
        self.vertex=v
        self.el=[]
    def __str__(self):
        estrs=map(lambda x :"+%d"%(x[0],) if x[1]>0 else "-%d"%(x[0],),self.el)
        return "Vertex id: %d Edges: "%(self.vertex,)+",".join(estrs)
class Edge:
    def __init__(self,e):
        self.n0=e[0]
        self.n1=e[1]
        self.line=[]

class Graph:
    def __init__(self,nodes,edges):
        # nodes is a list of points
        # edges is a list of connected node indices
        # construct a topology 
        # augment with an edge list at nodes and polyline at each edge
        self.vertices=[Vertex(n) for n in nodes]
        self.nodes=[Node(n) for n in range(len(nodes)) ]
        self.edges=[Edge(e) for e in edges ]
        for i,e in enumerate(self.edges):
           self.nodes[e.n0].el.append((i,+1))
           self.nodes[e.n1].el.append((i,-1))

    def get_polyline(self,e):
        xs=[self.vertices[self.nodes[e.n0].vertex].x,]
        ys=[self.vertices[self.nodes[e.n0].vertex].y,]
        for p in e.line:
           xs.append(self.vertices[p].x)
           ys.append(self.vertices[p].y)
        xs.append(self.vertices[self.nodes[e.n1].vertex].x)
        ys.append(self.vertices[self.nodes[e.n1].vertex].y)
        return xs,ys

    def getNeighborNodes(self,n):
        return set([z for z in 
               [self.edges[e].n1 if d>0 else self.edges[e].n0 for e,d in self.nodes[n].el] 
               if z!=n])
            
    def remove_3cycles(self):
        edgesToKeep =[ True,]*len(self.edges)
        # go in order of highest min valency to avoid dangles
        temp=[(e,min(len(self.nodes[self.edges[e].n0].el),len(self.nodes[self.edges[e].n0].el))) for e in range(len(self.edges))]
        for ei,dummy in sorted(temp,key=lambda x:-x[1]):
            e=self.edges[ei]
            nbrs0=[ nb for nb in self.getNeighborNodes(e.n0) if not nb == e.n1 ]
            nbrs1=[ nb for nb in self.getNeighborNodes(e.n1) if not nb == e.n0 ]
            common=set(nbrs0) & set(nbrs1)
            if len(common)>0:
                edgesToKeep[ei]=False
                self.nodes[e.n0].el=[(ee,dd) for ee,dd in self.nodes[e.n0].el if ee != ei ]
                self.nodes[e.n1].el=[(ee,dd) for ee,dd in self.nodes[e.n1].el if ee != ei ]
        newEdgeIndex=[-1,]*len(self.edges)
        newEdgeCount=0
        for i in range(len(self.edges)):
            if edgesToKeep[i]:
                newEdgeIndex[i]=newEdgeCount
                newEdgeCount+=1
        self.edges=[self.edges[i] for i in range(len(self.edges)) if newEdgeIndex[i] >=0]
        for i in range(len(self.nodes)):
            for e in range(len(self.nodes[i].el)):
               self.nodes[i].el[e]=(newEdgeIndex[self.nodes[i].el[e][0]],self.nodes[i].el[e][1])
               assert(self.nodes[i].el[e][0]>=0)
    def split_cycles(self):
        for ei,e in enumerate(self.edges):
            if e.n0==e.n1: # loop
                assert len(e.line)>0
                newEdgeIndex=len(self.edges)
                middleVertexIndex=len(e.line)//2
                newNodeIndex=len(self.nodes)
                self.nodes.append(Node(e.line[middleVertexIndex]))
                self.nodes[-1].el=[(ei,1),(newEdgeIndex,-1)]
                found=replace_in_list(self.nodes[e.n1].el,(ei,1),(newEdgeIndex,1))
                assert(found==1)
                self.edges.append(Edge((newNodeIndex,e.n1)))
                self.edges[-1].line=e.line[middleVertexIndex+1:]
                e.n1=newNodeIndex
                e.line=e.line[:middleVertexIndex]
        
    def remove_pseudonodes(self):
        nodeCount=0
        newNodeIndex=[-1,]*len(self.nodes)
        nodeToEdgeIndex=[-1,]*len(self.nodes)
        edgesToKeep =[ True,]*len(self.edges)
        def reverse_edge(e):
            n0=self.edges[e].n0
            n1=self.edges[e].n1
            self.edges[e].n0=n1
            self.edges[e].n1=n0
            self.edges[e].line.reverse()
            found=replace_in_list(self.nodes[n0].el,(e,1),(e,-1))
            assert(found==1)
            found=replace_in_list(self.nodes[n1].el,(e,-1),(e,1))
            assert(found==1)
        def join_edge(e0,e1):
            #print "append edge",e1,"to",e0
            midnode=self.nodes[self.edges[e0].n1]
            self.edges[e0].line.append( midnode.vertex )
            self.edges[e0].line.extend( self.edges[e1].line )
            self.edges[e0].n1=self.edges[e1].n1
            found=replace_in_list(self.nodes[self.edges[e0].n1].el,(e1,-1),(e0,-1))
            assert(found==1)
            
        edgeLookup=[-1,]*len(self.edges)
        for i in range(len(self.nodes)):
           keepNode=True
           if len(self.nodes[i].el)==2:
               e0=self.nodes[i].el[0] 
               e1=self.nodes[i].el[1]
               if e0[0] != e1[0]:
                  #print "remove node",i
                  #print self.nodes[i]
                  # remove pseudonode
                  keepNode=False
                  if e0[1] ==  e1[1]:
                      reverse_edge(e1[0])
                  if e0[1] < 0:
                      join_edge(e0[0],e1[0])
                      edgesToKeep[e1[0]]=0
                      edgeLookup[e1[0]]=e0[0]
                      nodeToEdgeIndex[i]=e0[0]
                  else:
                      join_edge(e1[0],e0[0])
                      edgesToKeep[e0[0]]=0
                      edgeLookup[e0[0]]=e1[0]
                      nodeToEdgeIndex[i]=e1[0]
           if keepNode:
               newNodeIndex[i]=nodeCount
               nodeCount += 1
        self.nodes=[self.nodes[i] for i in range(len(self.nodes)) if newNodeIndex[i] >=0]
        newEdgeIndex=[-1,]*len(self.edges)
        newEdgeCount=0
        for i in range(len(self.edges)):
            if edgesToKeep[i]:
                self.edges[i].n0=newNodeIndex[self.edges[i].n0]
                self.edges[i].n1=newNodeIndex[self.edges[i].n1]
                newEdgeIndex[i]=newEdgeCount
                newEdgeCount+=1
        for i in range(len(nodeToEdgeIndex)):
            if nodeToEdgeIndex[i]>=0:
                while edgeLookup[nodeToEdgeIndex[i]]>=0:
                    nodeToEdgeIndex[i]=edgeLookup[nodeToEdgeIndex[i]]
                nodeToEdgeIndex[i]=newEdgeIndex[nodeToEdgeIndex[i]]
        self.edges=[self.edges[i] for i in range(len(self.edges)) if newEdgeIndex[i] >=0]
        for i in range(len(self.nodes)):
            #print "Nodescan\n",self.nodes[i]
            for e in range(len(self.nodes[i].el)):
               self.nodes[i].el[e]=(newEdgeIndex[self.nodes[i].el[e][0]],self.nodes[i].el[e][1])
               assert(self.nodes[i].el[e][0]>=0)
        
        return newNodeIndex,newEdgeIndex,nodeToEdgeIndex        
              #    nodes[i].el[0][1] e0=nodes[i][1][0]
        
#        e1=nodes[i][1][1]
#        if(e0>0):
#            reverse_edge(e0-1)
#        if(e1<0):
#            reverse_edge(e1-1)
#        e0=abs(e0)-1
#        e1=abs(e1)-1
#        edges[e0][1].append(nodes[i][0])
#        edges[e0][1].extend(edges[e1][1])
#        edges[e0][0][1]=edges[e1][0][1]
#        edgesToKeep[e1]=0
#        nodes[i][1]=[]
#        replaceInList(nodes[ edges[e0][0][1] ][1],-e1+1,-e0+1)
#    else:
#        newNodeIndex[i]=newNodeCount
#        newNodeCount+=1
#    def reverse_edge(self):


if __name__ == '__main__':
   import matplotlib.pyplot as plt
   from itertools import product
   def drawgraph(g):
       nx,ny=zip(*[ (g.vertices[n.vertex].x,g.vertices[n.vertex].y) for n in g.nodes])
       plt.plot(nx,ny,'r+')
       for e in g.edges:
           xs,ys=g.get_polyline(e)
           plt.plot(xs,ys,color='pink')
           #plt.arrow(xs[-2],ys[-2],xs[-1],ys[-1],color='pink')
       limits=plt.axis()
       step=(limits[1]-limits[0])/20.
       plt.axis([limits[0]-step,limits[1]+step,limits[2]-step,limits[3]+step])
       plt.show()   

   g=Graph([(0,0),(0,1),(1,0),(1,1)],[(0,1),(2,3),(1,2),(3,0)])

   drawgraph(g)
   g.remove_pseudonodes()      
   drawgraph(g)
   g.split_cycles()
   drawgraph(g)


   g2=Graph(list(product(range(3),range(5))),[(0,1),(1,2),(2,3),(3,4),
                                       (0,5),(1,6),(3,8),(4,9),
                                       (10,5),(11,6),(13,8),(14,9),
                                       (6,7),(7,8),
                                       (14,13),(13,12),(12,11),(11,10)])
   drawgraph(g2)
   g2.remove_pseudonodes()      
   drawgraph(g2)
   g2.split_cycles()
   drawgraph(g2)
   
   g3=Graph([(0,0),(0,1),(0,2),(1,0),(2,0)],[(0,1),(1,2),(0,3),(3,4),(1,3)])
   drawgraph(g3)
   g3.remove_3cycles()      
   drawgraph(g3)
        