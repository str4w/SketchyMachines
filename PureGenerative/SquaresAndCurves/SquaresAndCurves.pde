// Inspired by
// https://twitter.com/RaminNasibov/status/1021208094754377728


int nbCorners=4;
int innerTick=0;
int outerTick=0;
int xgridsize=6;
int ygridsize=4;
int nbShapes=12;

float[] xcoords;
float[] ycoords;

float[][] xcurvecoords;
float[][] ycurvecoords;
float xcenter;
float ycenter;



void setup()
{
  size(750,500);
  xcoords = new float[nbCorners];
  ycoords = new float[nbCorners];
  xcurvecoords = new float[nbCorners][nbShapes+1];
  ycurvecoords = new float[nbCorners][nbShapes+1];
  //frameRate(5);
  frameRate(60);
}

void draw()
{
float xgridspacing=width/(xgridsize+1);
float ygridspacing=height/(ygridsize+1);
  switch(outerTick) {
    case 0:
    {
      println("spacing"+xgridspacing+" "+ygridspacing);
      background(128);
      ++outerTick;
      break;
    }
    case 1:
    {
      float yval=(innerTick+0.5)*ygridspacing;
      stroke(255);
      line(0,yval,width,yval);
      ++innerTick;
      if (innerTick>ygridsize) {
        innerTick=0;
        ++outerTick;
      }
      break;
    }
    case 2:
    {
      float xval=(innerTick+0.5)*xgridspacing;
      stroke(255);
      line(xval,0,xval,height);
      ++innerTick;
      if (innerTick>xgridsize) {
        innerTick=0;
        ++outerTick;
      }
      break;
    }
    case 3:
    {
      // row,col,square,side
      int side=innerTick%nbCorners;
      int shape=int(innerTick/nbCorners)%(nbShapes+1);
      int col=int(innerTick/nbCorners/(nbShapes+1))%xgridsize;
      int row=innerTick/nbCorners/(nbShapes+1)/xgridsize;
      if (row>=ygridsize) {
        innerTick=0;
        ++outerTick;
        break;
      }
      if (shape==0 && side==0) {
        // set up the frame
        if (row%2==col%2) {
          xcoords[0]=(col+0.5)*xgridspacing;
          ycoords[0]=(row+0.5)*ygridspacing;
          xcoords[1]=(col+1.5)*xgridspacing;
          ycoords[1]=(row+0.5)*ygridspacing;
          xcoords[2]=(col+1.5)*xgridspacing;
          ycoords[2]=(row+1.5)*ygridspacing;
          xcoords[3]=(col+0.5)*xgridspacing;
          ycoords[3]=(row+1.5)*ygridspacing;
        } else {
          xcoords[3]=(col+0.5)*xgridspacing;
          ycoords[3]=(row+0.5)*ygridspacing;
          xcoords[2]=(col+1.5)*xgridspacing;
          ycoords[2]=(row+0.5)*ygridspacing;
          xcoords[1]=(col+1.5)*xgridspacing;
          ycoords[1]=(row+1.5)*ygridspacing;
          xcoords[0]=(col+0.5)*xgridspacing;
          ycoords[0]=(row+1.5)*ygridspacing;
        }
        // first curve points are the corners
        xcenter=0;
        ycenter=0;
        for (int i=0;i<nbCorners;++i)
        {
          xcurvecoords[i][0]=xcoords[i];
          ycurvecoords[i][0]=ycoords[i];
          xcenter+=xcoords[i];
          ycenter+=ycoords[i];
        }
        xcenter/=nbCorners;
        ycenter/=nbCorners;
      }
      strokeWeight(1);
      stroke(0,0,255);
      int i=side;
      int j=(side+1)%nbCorners;
      float dx0=xcurvecoords[j][0]-xcurvecoords[i][0];
      float dy0=ycurvecoords[j][0]-ycurvecoords[i][0];
      float d0=sqrt(dx0*dx0+dy0*dy0);
      float dx=xcurvecoords[j][shape]-xcurvecoords[i][shape];
      float dy=ycurvecoords[j][shape]-ycurvecoords[i][shape];
      float d=sqrt(dx*dx+dy*dy);
      float ratio=3./nbShapes;//min(0.5,(d0*1.6/nbShapes)/d);
      if (shape<nbShapes)
      {
        xcurvecoords[j][shape+1]=lerp(xcurvecoords[j][shape],xcurvecoords[(j+1)%nbCorners][shape],ratio);
        ycurvecoords[j][shape+1]=lerp(ycurvecoords[j][shape],ycurvecoords[(j+1)%nbCorners][shape],ratio);
        line(xcurvecoords[i][shape],ycurvecoords[i][shape],xcurvecoords[j][shape+1],ycurvecoords[j][shape+1]);
        //lerp(xcoords[i],xcenter,0.1*(square+1)),lerp(ycoords[i],ycenter,0.1*(square+1)),
        //   lerp(xcoords[j],xcenter,0.1*(square+1)),lerp(ycoords[j],ycenter,0.1*(square+1)));
      } else {
        stroke(128,0,128);
        strokeWeight(3);
        noFill();
//        beginShape();
//        curveVertex(2*xcurvecoords[i][0]-xcurvecoords[j][0],2*ycurvecoords[i][0]-ycurvecoords[j][0]);
//        for(int k=0;k<=nbShapes;++k)
//        {
//          curveVertex(xcurvecoords[i][k],ycurvecoords[i][k]);
//        }
//        curveVertex(xcenter,ycenter);
//        curveVertex(xcurvecoords[(i+nbCorners-1)%nbCorners][nbShapes],ycurvecoords[(i+nbCorners-1)%nbCorners][nbShapes]);
//        endShape();
        curve(2*xcurvecoords[i][0]-xcurvecoords[j][0],2*ycurvecoords[i][0]-ycurvecoords[j][0],xcurvecoords[i][0],ycurvecoords[i][0],xcurvecoords[i][1],ycurvecoords[i][1],xcurvecoords[i][2],ycurvecoords[i][2]);
        for(int k=0;k<=(nbShapes-3);++k) {
        curve(xcurvecoords[i][k],ycurvecoords[i][k],xcurvecoords[i][k+1],ycurvecoords[i][k+1],xcurvecoords[i][k+2],ycurvecoords[i][k+2],xcurvecoords[i][k+3],ycurvecoords[i][k+3]);
        }
        curve(xcurvecoords[i][nbShapes-2],ycurvecoords[i][nbShapes-2],xcurvecoords[i][nbShapes-1],ycurvecoords[i][nbShapes-1],xcurvecoords[i][nbShapes],ycurvecoords[i][nbShapes],xcenter,ycenter);
        curve(xcurvecoords[i][nbShapes-1],ycurvecoords[i][nbShapes-1],xcurvecoords[i][nbShapes],ycurvecoords[i][nbShapes],xcenter,ycenter,xcurvecoords[(i+nbCorners-1)%nbCorners][nbShapes],ycurvecoords[(i+nbCorners-1)%nbCorners][nbShapes]);
        if ( false ) //side>nbCorners/2)
        {
        beginShape();
          curveVertex(xcurvecoords[i][nbShapes-1],ycurvecoords[i][nbShapes-1]);
          curveVertex(xcurvecoords[i][nbShapes],ycurvecoords[i][nbShapes]);
          curveVertex(lerp(xcurvecoords[j][shape],xcurvecoords[(j+1)%nbCorners][shape],2.5/nbShapes),
                      lerp(ycurvecoords[j][shape],ycurvecoords[(j+1)%nbCorners][shape],2.5/nbShapes));
          curveVertex(xcenter,ycenter);
          i=(side+nbCorners/2)%nbCorners;
          j=(i+1)%nbCorners;
          curveVertex(lerp(xcurvecoords[j][shape],xcurvecoords[(j+1)%nbCorners][shape],2.5/nbShapes),
                      lerp(ycurvecoords[j][shape],ycurvecoords[(j+1)%nbCorners][shape],2.5/nbShapes));
          curveVertex(xcurvecoords[i][nbShapes],ycurvecoords[i][nbShapes]);
          curveVertex(xcurvecoords[i][nbShapes-1],ycurvecoords[i][nbShapes-1]);
        endShape();
        }
      }
      ++innerTick;
      break;
    }
    default:
    noFill();
    stroke(0);
    rect(xgridspacing*0.25,ygridspacing*0.25,(xgridsize+0.5)*xgridspacing,(ygridsize+0.5)*ygridspacing);
    println("Drawing finished");
    noLoop();
  }

}
