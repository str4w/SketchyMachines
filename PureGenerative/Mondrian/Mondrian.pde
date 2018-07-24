float pad=1.0;
int rings=3;
class Rectangle
{
  Rectangle(float x1, float y1, float x2, float y2)
  {
    _x1=x1;
    _y1=y1;
    _x2=x2;
    _y2=y2;
  }
  float _x1,_y1,_x2,_y2;
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
      for(int i=1;i<=rings;++i)
      {
        rect(_x1+pad,_y1+pad,_x2-_x1-2*pad,_y2-_y1-2*pad);
      }
    }
  }
  void split()
  {
    if (child1==null) {
      float xmin=_x1+4*pad*rings;
      float xmax=_x2-4*pad*rings;
      float ymin=_y1+4*pad*rings;
      float ymax=_y2-4*pad*rings;
      float xspace=max(0,xmax-xmin);
      float yspace=max(0,ymax-ymin);
      float totalspace=xspace+yspace;
      if (totalspace>0) {
        float splitpoint=random(totalspace);
        if (splitpoint<xspace)
        {
          child1=new Rectangle(_x1,_y1,_x1+xmin+splitpoint,_y2);
          child2=new Rectangle(_x1+xmin+splitpoint,_y1,_x2,_y2);
        } else {
          child1=new Rectangle(_x1,_y1,_x2,_y1+ymin+splitpoint-xspace);
          child2=new Rectangle(_x1,_y1+ymin+splitpoint-xspace,_x2,_y2);
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

Rectangle root;
float padding=3;
void setup()
{
  size(1100,850);
  stroke(0);
  root=new Rectangle(padding,padding,width-padding, height-padding);
  noLoop();
}
void draw()
{
  background(255);
  root.draw();
  
}
