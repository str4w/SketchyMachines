import processing.pdf.*;
PImage InputImage;
PGraphics TheBuffer;
PrintWriter output;
static abstract class Mode
{
static final int RENDER_HALFTONE=0;
static final int RENDER_LINE=1;
static final int RENDER_LINE2=2;
static final int RENDER_SQUIGGLE=3;
static final int RENDER_VDCIRCLE=4;
static final int RENDER_CIRCLES=5;
};
int theMode=Mode.RENDER_LINE2;
boolean makePDF=false;
boolean writeLinesToFile=true;

// stained glass
float line2_alwaysOff =130;
float line2_alwaysOn =30;
float line2_fineSpacing=4;//2;
float line2_Spacing=16;//16;//12.0;

float line2_angle=45.*PI/180.;
String InputFileName="../../SourceMaterial/stained_glass_darkblue_threshold.png";
String LineFileName="stained_glass_darkblue.lines";

//float line2_angle=-45.*PI/180.;
//String InputFileName="../../SourceMaterial/stained_glass_lightblue_threshold.png";
//String LineFileName="stained_glass_lightblue.lines";

//float line2_angle=25.*PI/180.;
//String InputFileName="../../SourceMaterial/stained_glass_darkgreen_threshold.png";
//String LineFileName="stained_glass_darkgreen.lines";

//float line2_angle=35.*PI/180.;
//String InputFileName="../../SourceMaterial/stained_glass_lightgreen_threshold.png";
//String LineFileName="stained_glass_lightgreen.lines";

//float line2_angle=60.*PI/180.;
//String InputFileName="../../SourceMaterial/stained_glass_yellow_threshold.png";
//String LineFileName="stained_glass_yellow.lines";

//float line2_angle=-30.*PI/180.;
//String InputFileName="../../SourceMaterial/stained_glass_pink_threshold.png";
//String LineFileName="stained_glass_pink.lines";

//float line2_angle=10.*PI/180.;
//String InputFileName="../../SourceMaterial/stained_glass_red_threshold.png";
//String LineFileName="stained_glass_red.lines";

//float line2_angle=0.*PI/180.;
//String InputFileName="../../SourceMaterial/stained_glass_blackfill_threshold.png";
//String LineFileName="stained_glass_blackfill.lines";

//String InputFileName="../../SourceMaterial/xi_cropped.png";
//String LineFileName="xi.lines";
//String InputFileName="../../SourceMaterial/conway_cropped.png";
//String LineFileName="conway.lines";
//String InputFileName="../../SourceMaterial/roses_red.png";
//String LineFileName="roses_red.lines";
//String InputFileName="../../SourceMaterial/trump.jpeg";
//String LineFileName="Trump.lines";
  //PImage InputImage=loadImage("../../SourceMaterial/groseille1.png");
//String LineFileName="conway.lines";
  //PImage InputImage=loadImage("../../SourceMaterial/Che_Guevara.png");
//String LineFileName="conway.lines";
//String InputFileName="../../SourceMaterial/Alan_Turing.jpg";
//String LineFileName="turing.lines";
  //PImage InputImage=loadImage("../../data/raccoon.png");
//String LineFileName="conway.lines";
//String InputFileName="../../SourceMaterial/raccoon_mod.png";
//String LineFileName="raccoon.lines";
  // raccoon originally from https://www.photo-elsoar.com/raccoon-free-pictures.html
String PDFFileName="output.pdf";
// Halftone parameters
float halftone_minRadius =0.0;
float halftone_maxRadius =2.0;
// Render_line parameters
float line_minRadius =-0.5;
float line_maxRadius =2.0;
float line_angle=45.*PI/180.;
// Render_line2 parameters
//float line2_alwaysOff =130;
//float line2_alwaysOn =30;
//float line2_fineSpacing=8;//4;//2;
//float line2_Spacing=32;//16;//12.0;
//float line2_angle=45.*PI/180.;

//float line2_alwaysOff =180;
//float line2_alwaysOn =50;
//float line2_fineSpacing=1;
//float line2_Spacing=12.0;
//float line2_angle=-45.*PI/180.;

//xi
//float line2_alwaysOff =120;
//float line2_alwaysOn =50;
//float line2_fineSpacing=3;
//float line2_Spacing=16.0;
//float line2_angle=-45.*PI/180.;

//Che
//float line2_alwaysOff =120;
//float line2_alwaysOn =50;
//float line2_fineSpacing=2;
//float line2_Spacing=12.0;
//float line2_angle=45.*PI/180.;

void setup()
{
  PImage InputImage=loadImage(InputFileName);
  InputImage.loadPixels();
  
  size(1000,1000);
  TheBuffer=createGraphics(InputImage.width,InputImage.height);
  TheBuffer.beginDraw();
  TheBuffer.background(255);
  TheBuffer.image(InputImage,0,0);
  TheBuffer.endDraw();
  //frameRate(24);
  if (writeLinesToFile) {
    output=createWriter(LineFileName);
  }
  noLoop();
}

void draw()
{  
   if (makePDF) {
     beginRecord(PDF, PDFFileName); 
   }

   PImage dasImage=TheBuffer.get(0,0,TheBuffer.width,TheBuffer.height);
   dasImage.loadPixels();
   float hscale=1.;//float(width)/float(dasImage.width);
   float vscale=1.;//float(height)/float(dasImage.height);
   float scale = (abs(1-hscale)<abs(1-vscale))?hscale:vscale;
   float xoffset=0;//(width-dasImage.width*scale)/2;
   float yoffset=0;//(height-dasImage.height*scale)/2;
   //image(dasImage,0,0);
   
   switch(theMode){
   case Mode.RENDER_HALFTONE:
   {
     // halftone
     noStroke();
     fill(0);
     ellipseMode(RADIUS);
     float minRadius =halftone_minRadius;
     float maxRadius =halftone_maxRadius;
     float Spacing=3*maxRadius+1;
   
     int initialStep=int(Spacing/2+1);
     float radiusRange=maxRadius-minRadius;
     println("Scale"+str(scale));
     for (int x=initialStep;x<width-initialStep;x+=Spacing)
     {
       for (int y=initialStep;y<width-initialStep;y+=Spacing)
       {
         int newy=int((y-yoffset)/scale);
         int newx=int((x-xoffset)/scale);
         if(newy<dasImage.height && newx<dasImage.width && newy>=0 && newx>= 0) 
         {
           int linearIndex=newy*dasImage.width+newx;
           int greyval=dasImage.pixels[linearIndex] & 0xFF;
           float radius=minRadius+radiusRange*((255-greyval)/255.);
           if (radius>0) 
           {
               ellipse(x,y,radius,radius);
           }
         }
       }  
     }
     for (int x=initialStep+int(Spacing/2);x<width-(initialStep+Spacing/2);x+=Spacing)
     {
       for (int y=initialStep+int(Spacing/2);y<width-(initialStep+Spacing/2);y+=Spacing)
       {
         int newy=int((y-yoffset)/scale);
         int newx=int((x-xoffset)/scale);
         if(newy<dasImage.height && newx<dasImage.width && newy>=0 && newx>= 0) 
         {
           int linearIndex=newy*dasImage.width+ newx;
           int greyval=dasImage.pixels[linearIndex] & 0xFF;
           float radius=minRadius+radiusRange*((255-greyval)/255.);
           if (radius>0) 
           {
               ellipse(x,y,radius,radius);
           }
         }
       }  
     }
   }
   break;
   case Mode.RENDER_LINE:
   {
     // variable density line
     noStroke();
     fill(0);
     ellipseMode(RADIUS);
     float minRadius = line_minRadius;
     float maxRadius = line_maxRadius;
     float angle= line_angle;
     float Spacing=3.0*maxRadius+1;
     float initialStep=Spacing;
     float dx=cos(angle);
     float dy=sin(angle);
     float radiusRange=maxRadius-minRadius;
     int nSteps=int(width/dx);
     float[] xVertices=new float[nSteps*2]; 
     float[] yVertices=new float[nSteps*2]; 
     for(int y=-height;y<2*height;y+=Spacing) 
     {
       for(int step=0;step<nSteps;++step)
       {
          float curx=step*dx;
          float cury=y+step*dy;
          float radius=0;
          int newy=int((cury-yoffset)/scale);
          int newx=int((curx-xoffset)/scale);
          if(newy<dasImage.height && newx<dasImage.width && newy>=0 && newx>= 0) 
          {
             int linearIndex=newy*dasImage.width+newx;
             int greyval=dasImage.pixels[linearIndex] & 0xFF;
             radius=max(minRadius+radiusRange*((255-greyval)/255.),0);
          }
  
          
          
          xVertices[step]=curx-dy*radius;
          yVertices[step]=cury+dx*radius;
          xVertices[2*nSteps-1-step]=curx+dy*radius;
          yVertices[2*nSteps-1-step]=cury-dx*radius;
        }
        beginShape();
        for(int step=0;step<nSteps*2;++step)
        {
         vertex(xVertices[step],yVertices[step]);
         if (writeLinesToFile) { output.print(xVertices[step]); output.print(" "); output.print(-1*yVertices[step]); output.print(" "); }
         //println("Vertices: "+str(xVertices[step])+", "+str(yVertices[step]));
        }
        endShape(CLOSE);
        if (writeLinesToFile) { output.print(xVertices[0]); output.print(" "); output.println(-1*yVertices[0]); }
     }
   }
   break;
   case Mode.RENDER_LINE2:
   {
     // variable density line
     background(255);
     stroke(0);
     noFill();
     //fill(0);
     //ellipseMode(RADIUS);
     float alwaysOff =line2_alwaysOff;
     float alwaysOn =line2_alwaysOn;
     float fineSpacing=line2_fineSpacing;
     float Spacing=line2_Spacing;
     float angle=line2_angle;
     float centerx=width/2;
     float centery=height/2;

     
     float initialStep=Spacing;
     float dx=cos(angle);
     float dy=sin(angle);
     int nSteps=int(width/dx);
     for(float y=-height;y<2*height;y+=fineSpacing) 
     {
       float[] xVertices=new float[nSteps]; 
       float[] yVertices=new float[nSteps]; 
       boolean[] drawIt=new boolean[nSteps];
       float criterion=alwaysOn+(1.0-abs(cos(PI*(y-Spacing/2)/Spacing)))*(alwaysOff-alwaysOn);
       for(int step=0;step<nSteps;++step)
       {
          float curx=step*dx;
          float cury=y+step*dy;
          int newy=int((cury-yoffset)/scale);
          int newx=int((curx-xoffset)/scale);
           drawIt[step]=false;
          if(newy<dasImage.height && newx<dasImage.width && newy>=0 && newx>= 0) 
          {
             int linearIndex=newy*dasImage.width+newx;
             int greyval=dasImage.pixels[linearIndex] & 0xFF;
             drawIt[step]=greyval<criterion;
          }
          xVertices[step]=curx;
          yVertices[step]=cury;
        }
        int step=0;
        while(step<nSteps)
        {
           while(step<nSteps && !drawIt[step])
           {
             ++step;
           }
           beginShape();
           int count=0;
           float lastx=0,lasty=0;
           while(step<nSteps && drawIt[step])
           {
             if(count==0) 
             {
             vertex(xVertices[step],yVertices[step]);
             if (writeLinesToFile) { output.print(xVertices[step]); output.print(" "); output.print(-1*yVertices[step]); output.print(" "); }

       //          output.print("<path d=\"m "+
        //       str(xVertices[step]) +","+str(yVertices[step])+" ");
             }
             else
             {
                lastx=xVertices[step];
                lasty=yVertices[step];

      //         output.print(str(xVertices[step]-xVertices[step-1]) +","+str(yVertices[step]-yVertices[step-1])+" ");
             }
              ++step;
              ++count;
           }
           if(count>1)
           {
             vertex(lastx,lasty);
             if (writeLinesToFile) { output.print(lastx); output.print(" "); output.println(-1*lasty); }
      //         output.println("\" style=\"stroke: #000000; fill:none;\"/>");
  
           }
           else
           {
             if(writeLinesToFile) {output.println("");}
           }
           endShape();
        }
     
  //   output.println("</svg>");
    // output.flush();
    // output.close();

     }
   }
   break;
   case Mode.RENDER_SQUIGGLE:
   {
     // variable density line
     stroke(0);
     noFill();
     float Spacing=3.0;
     float maxOffset=-7.0;
     float angle=0;//45.*PI/180.;
     float initialStep=Spacing;
     float dx=cos(angle);
     float dy=sin(angle);
     int nSteps=int(width/dx);
     float[] xVertices=new float[nSteps]; 
     float[] yVertices=new float[nSteps]; 
     for(int y=-height;y<2*height;y+=Spacing) 
     {
       for(int step=0;step<nSteps;++step)
       {
          float curx=step*dx;
          float cury=y+step*dy;
          float radius=0;
          int newy=int((cury-yoffset)/scale);
          int newx=int((curx-xoffset)/scale);
          if(newy<dasImage.height && newx<dasImage.width && newy>=0 && newx>= 0) 
          {
             int linearIndex=newy*dasImage.width+newx;
             int greyval=dasImage.pixels[linearIndex] & 0xFF;
             radius=maxOffset*((128-greyval)/255.);
          }
  
          
          
          xVertices[step]=curx-dy*radius;
          yVertices[step]=cury+dx*radius;
        }
        beginShape();
        for(int step=0;step<nSteps;++step)
        {
         vertex(xVertices[step],yVertices[step]);
         //println("Vertices: "+str(xVertices[step])+", "+str(yVertices[step]));
        }
        endShape();
     }
   }
   break;
   case Mode.RENDER_VDCIRCLE:
   {
     // variable density circles
     noStroke();
     //stroke(0);
     //noFill();
     fill(0);
     ellipseMode(RADIUS);
     float minRadius =0.;
     float maxRadius =4.0;
     float Spacing=3.0*maxRadius+1;
     float initialStep=Spacing;
     float radiusRange=maxRadius-minRadius;
     float centerx=width/2;
     float centery=height/2;
     for(float r=Spacing;r<sqrt(centerx*centerx+centery*centery);r+=Spacing) 
     {
       int nSteps=int(r*TWO_PI+0.5);
       float[] xVertices=new float[nSteps*2]; 
       float[] yVertices=new float[nSteps*2]; 
       for(int step=0;step<nSteps;++step)
       {
          float angle=float(step)/float(nSteps)*TWO_PI;
          float dx=cos(angle);
          float dy=sin(angle);
          float curx=r*dx+centerx;
          float cury=r*dy+centery;
          float radius=0;
          int newy=int((cury-yoffset)/scale);
          int newx=int((curx-xoffset)/scale);
          if(newy<dasImage.height && newx<dasImage.width && newy>=0 && newx>= 0) 
          {
             int linearIndex=newy*dasImage.width+newx;
             int greyval=dasImage.pixels[linearIndex] & 0xFF;
             radius=max(minRadius+radiusRange*((255-greyval)/255.),0);
          }
          
          xVertices[step]=curx+dx*radius;
          yVertices[step]=cury+dy*radius;
          xVertices[2*nSteps-1-step]=curx-dx*radius;
          yVertices[2*nSteps-1-step]=cury-dy*radius;
        }
        beginShape();
        // repeat this one to avoid the notch
        vertex(xVertices[nSteps-1],yVertices[nSteps-1]);
        for(int step=0;step<nSteps*2;++step)
        {
         vertex(xVertices[step],yVertices[step]);
         //println("Vertices: "+str(xVertices[step])+", "+str(yVertices[step]));
        }
        // repeat this one to avoid the notch
        vertex(xVertices[nSteps],yVertices[nSteps]);
        endShape(CLOSE);
     }
   }
   break;
   case Mode.RENDER_CIRCLES:
   {
     // fine line circles
     //noStroke();
     background(255);
     stroke(0);
     noFill();
     //fill(0);
     //ellipseMode(RADIUS);
     float alwaysOff =200;
     float alwaysOn =50;
     //float fineSpacing=0.5;
     //float Spacing=6.0;
     float fineSpacing=5;
     float Spacing=24.0;
     float centerx=width/2;
     float centery=height/2;
     //beginRecord(PDF,"render1.pdf");
     //PrintWriter output=createWriter("render1.svg");
     //output.println("<svg  xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\">");
  
     for(float r=.5;r<sqrt(centerx*centerx+centery*centery);r+=fineSpacing) 
     {
       int nSteps=int(r*TWO_PI+0.5);
       float[] xVertices=new float[nSteps]; 
       float[] yVertices=new float[nSteps]; 
       boolean[] drawIt=new boolean[nSteps];
       float criterion=alwaysOn+(1.0-abs(cos(PI*(r-Spacing/2)/Spacing)))*(alwaysOff-alwaysOn);
       for(int step=0;step<nSteps;++step)
       {
          float angle=float(step)/float(nSteps)*TWO_PI;
          float dx=cos(angle);
          float dy=sin(angle);
          float curx=r*dx+centerx;
          float cury=r*dy+centery;
          int newy=int((cury-yoffset)/scale);
          int newx=int((curx-xoffset)/scale);
          drawIt[step]=false;
          if(newy<dasImage.height && newx<dasImage.width && newy>=0 && newx>= 0) 
          {
             int linearIndex=newy*dasImage.width+newx;
             int greyval=dasImage.pixels[linearIndex] & 0xFF;
             drawIt[step]=greyval<criterion;
          }
          xVertices[step]=curx;
          yVertices[step]=cury;
        }
        
        int step=0;
        while(step<nSteps)
        {
           while(step<nSteps && !drawIt[step])
           {
             ++step;
           }
           beginShape();
           int count=0;
           while(step<nSteps && drawIt[step])
           {
             //if(count==0) 
             //{
              //   output.print("<path d=\"m "+
              // str(xVertices[step]) +","+str(yVertices[step])+" ");
            // }
             //else
             //{
               //output.print(str(xVertices[step]-xVertices[step-1]) +","+str(yVertices[step]-yVertices[step-1])+" ");
               if (writeLinesToFile) { output.print(xVertices[step]); output.print(" "); output.print(-1*yVertices[step]); output.print(" "); }
             //}
             vertex(xVertices[step],yVertices[step]);
              ++step;
              ++count;
           }
           if(count>0)
           {
               //output.println("\" style=\"stroke: #000000; fill:none;\"/>");
               if (writeLinesToFile) { output.println(); }
           }
           endShape();
        }
     
     //output.println("</svg>");
     //output.flush();
     //output.close();
     }
   }
  }
  if (writeLinesToFile) {
    output.flush();
    output.close();
  }
  if(makePDF) {endRecord();}
}
