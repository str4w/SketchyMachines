float pad=2.0;
int rings=3;
int splits=10;
int hatches=10;
boolean writeLinesToFile=true;
String LineFileName="Mondrian_jul30.lines";
PrintWriter output;

PVector intersection(PVector p1,PVector v1,PVector p2, PVector v2)
{
  //println("intersection: "+p1.x+","+p1.y);
  PVector delta=new PVector(p2.x-p1.x,p2.y-p1.y);
  float denominator=v1.x*v2.y-v1.y*v2.x;
  float numerator=delta.x*v2.y-delta.y*v2.x;
  //return new PVector(p1.x,p1.y);
  return new PVector(p1.x+v1.x*numerator/denominator,p1.y+v1.y*numerator/denominator);
}
float distance2d(PVector p1,PVector p2)
{
  float dx=p1.x-p2.x;
  float dy=p1.y-p2.y;
  return sqrt(dx*dx+dy*dy);
}

class Pen
{
  boolean _doStroke;
  color _stroke;
  boolean _doFill;
  color _fill;
  void set()
  {
    if (_doStroke)
    {
      stroke(_stroke);
    }
    else
    {
      noStroke();
    }
    if (_doStroke)
    {
      fill(_fill);
    }
    else
    {
      noFill();
    }
  }
}

void drawLine(x1,y1,x2,y2)
{
}
void drawRectangle(x1,y1,x2,y2)
{
}

class Rectangle
{
  Rectangle(PVector a, PVector b,boolean filled)
  {
    _a=a.copy();
    _b=b.copy();
    _filled=filled;
  }
  PVector _a,_b;
  boolean _filled;
  Rectangle child1;
  Rectangle child2;
  void draw()
  {
    if (child1 != null) {
      child1.draw();
      child2.draw();
    }
    else
    {
      stroke(int(random(128)),int(random(128)),int(random(128)));
      if (_filled)
      {
        float w=rings-0.5;
        //fill(random(0.2*255,0.8*255));
        //noStroke();
        //rect(_x1+pad*w,_y1+pad*w,_x2-_x1-2*pad*w,_y2-_y1-2*pad*w);
      //  stroke(0);
        float[] xs={_a.x+pad*w,_b.x-pad*w,_b.x-pad*w,_a.x+pad*w};
        float[] ys={_a.y+pad*w,_a.y+pad*w,_b.y-pad*w,_b.y-pad*w};
       // stroke(255,0,0);
       // line(xs[0],ys[0],xs[2],ys[2]);
      //  stroke(0,0,255);
      //  line(xs[1],ys[1],xs[3],ys[3]);
        int corner=int(random(4));
       // stroke(0);
        float dx=xs[(corner+2)%4]-xs[corner];
        float dy=ys[(corner+2)%4]-ys[corner];
        PVector c1=new PVector(xs[corner],ys[corner]);
        PVector c2=new PVector(xs[(corner+2)%4],ys[(corner+2)%4]);
        PVector v1=new PVector(c2.x-c1.x,c2.y-c1.y);
        PVector v2=new PVector((v1.x>0?-1:1),(v1.y>0?1:-1));
        println("c1: "+c1.x+", "+c1.y+" v1 "+v1.x+", "+v1.y);
        for(int i=1;i<hatches;++i)
        {
          float alpha=(i/float(hatches))*(i/float(hatches));
          PVector pcurrent=new PVector(c1.x+v1.x*alpha,c1.y+v1.y*alpha);
          println("alpha " +alpha +" c1: "+c1.x+", "+c1.y+" v1 "+v1.x+", "+v1.y);
          PVector[] ps={
             intersection(pcurrent,v2,c1,new PVector(1,0)),
             intersection(pcurrent,v2,c1,new PVector(0,1)),
             intersection(pcurrent,v2,c2,new PVector(1,0)),
             intersection(pcurrent,v2,c2,new PVector(0,1))
          };
          
          float[] dists={
            distance2d(ps[0],pcurrent),          
            distance2d(ps[1],pcurrent),          
            distance2d(ps[2],pcurrent),          
            distance2d(ps[3],pcurrent)
          };
          int min0=0;
          for (int j=1;j<4;++j)
          {
            if (dists[j]<dists[min0]) {min0=j;}
          }
          int min1=(min0+1)%4;
          for (int j=0;j<4;++j)
          {
            if (j!=min0 && dists[j]<dists[min1]) {min1=j;}
          }
          
          line(ps[min0].x,ps[min0].y,ps[min1].x,ps[min1].y);
          if (writeLinesToFile) {
             output.println(ps[min0].x+" " + ps[min0].y*-1 +" " + ps[min1].x + " " + ps[min1].y*-1);
          }

        }
        
      }
      for(int i=1;i<=rings;++i)
      {
        noFill();
       // stroke(0);
        float w=i-0.5;
        float x1=_a.x+pad*w;
        float x2=_b.x-pad*w;
        float y1=_a.y+pad*w;
        float y2=_b.y-pad*w;
        rect(x1,y1,x2-x1,y2-y1);
        if (writeLinesToFile) {
           output.print(x1+" "+y1*-1+" ");
           output.print(x2+" "+y1*-1+" ");
           output.print(x2+" "+y2*-1+" ");
           output.print(x1+" "+y2*-1+" ");
           output.println(x1+" "+y1*-1);
        }
      }
    }
  }
  void split()
  {
    if (child1==null) {
      PVector offset=new PVector(4*pad*rings,4*pad*rings);
      PVector minPoint=PVector.add(_a,offset);
      PVector maxPoint=PVector.sub(_b,offset);
      PVector availableSpace=PVector.sub(maxPoint,minPoint);
      float xspace=max(0,availableSpace.x);
      float yspace=max(0,availableSpace.y);
      float totalspace=xspace+yspace;
      if (totalspace>0) {
        float splitdistance=random(totalspace);
        if (splitdistance<=xspace)
        {
          float splitpoint=minPoint.x+splitdistance;
          child1=new Rectangle(_a,new PVector(splitpoint,_b.y),_filled);
          child2=new Rectangle(new PVector(splitpoint,_a.y),_b,_filled);
        } else {
          float splitpoint=minPoint.y+splitdistance-xspace;
          child1=new Rectangle(_a,new PVector(_b.x,splitpoint),_filled);
          child2=new Rectangle(new PVector(_a.x,splitpoint),_b,_filled);
        }
      }
    } else {
      if(random(1)>0.5)
      {
        child1.split();
      } else {
        child2.split();
      }
      
    }
  }
    
    
}

float padding=3;
void setup()
{
  size(1100,850);
  stroke(0);
  noLoop();
  noFill();
  if (writeLinesToFile) {
    output=createWriter(LineFileName);
  }
}
void draw()
{
  background(255);
  Rectangle outer=new Rectangle(new PVector(padding,padding),new PVector(width-padding, height-padding),false);
  outer.draw();
 Rectangle root;
 root=new Rectangle(new PVector(padding+rings*pad,padding+rings*pad),new PVector(width-padding-rings*pad, height-padding-rings*pad),true);
  for (int i=0;i<splits;++i) {
    root.split();
  }
  root.draw();
    if (writeLinesToFile) {
    output.flush();
    output.close();
  }

}
