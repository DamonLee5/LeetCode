import sys,getopt
from numpy import linalg as LA
import numpy as np
import math
try:
        options,args = getopt.getopt(sys.argv[1:],"hp:i:",["help","envir="])
except getopt.GetoptError:
        sys.exit()



envir_para=90

def iscontained(cx,cy,r,point,num):
        tt=True
        for i in range(3):
                if LA.norm([cx[i]-point[0],cy[i]-point[1]])>r[i]+0.001:
                        tt=False
        return tt


def Trilateration_3D_rec(r,cx,cy):
        num=3
        xi=[float(qq) for qq in range(num*2)]
        xi=np.array(xi)
        yi=[float(qq) for qq in range(num*2)]
        yi=np.array(yi)
        d=[float(qq) for qq in range(num*num)]
        d=np.array(d)
        d=d.reshape((num,num))
        kx=1
        l=range(3)
        for i in l[0:num-1]:
                for j in l[i+1:num]:
                        d[i,j]=LA.norm([cx[i]-cx[j],cy[i]-cy[j]])
                        if d[i,j]>=r[i]+r[j] or d[i,j]<=abs(r[i]-r[j]):
                                range(3)
                        else:
                                a=(r[i]**2-r[j]**2+d[i,j]**2)/(2*d[i,j])
                                h=math.sqrt(r[i]**2-a**2)
                                x0=cx[i]+a*(cx[j]-cx[i])/d[i,j]
                                y0=cy[i]+a*(cy[j]-cy[i])/d[i,j]
                                rx=-(cy[j]-cy[i])*(h/d[i,j])
                                ry=-(cx[j]-cx[i])*(h/d[i,j])  
                                xi[kx*2-1]=x0+rx             
                                yi[kx*2-1]=y0-ry             
                                xi[kx*2]=x0-rx
                                yi[kx*2]=y0+ry               
                                kx=kx+1   
        x1=1000
        x2=-1000
        y1=1000
        y2=-1000
        for ii in range(2*(kx-1)):
                if xi[ii]<x1 and iscontained(cx,cy,r,[xi[ii],yi[ii]],num):
                        x1=xi[ii]
                if xi[ii]>x2 and iscontained(cx,cy,r,[xi[ii],yi[ii]],num):
                        x2=xi[ii]
                if yi[ii]<y1 and iscontained(cx,cy,r,[xi[ii],yi[ii]],num):
                        y1=yi[ii]
                if yi[ii]>y2 and iscontained(cx,cy,r,[xi[ii],yi[ii]],num):
                        y2=yi[ii]

        for kk in range(num):
                if (cx[kk]-r[kk]<x1) and iscontained(cx,cy,r,[cx[kk]-r[kk],cy[kk]],num):
                        x1=cx[kk]-r[kk]
                if (cx[kk]+r[kk]>x2) and iscontained(cx,cy,r,[cx[kk]+r[kk],cy[kk]],num):
                        x2=cx[kk]+r[kk]
                if (cy[kk]-r[kk]<y1) and iscontained(cx,cy,r,[cx[kk],cy[kk]-r[kk]],num):
                        y1=cy[kk]-r[kk]
                if (cy[kk]+r[kk]>y2) and iscontained(cx,cy,r,[cx[kk],cy[kk]+r[kk]],num):
                        y2=cy[kk]+r[kk]

        x_rec=(x1+x2)/2;
        y_rec=(y1+y2)/2;
        return x_rec,y_rec
for name,value in options:
        if name in ("-h","--help"):
                print("help")
        if name in ("-e","--envir"):
                envir_para=value

tx=[float(qq) for qq in range(3)]
ty=[float(qq) for qq in range(3)]
rssi=[float(qq) for qq in range(3)]


dist=[float(qq) for qq in range(3)]
nn=range(3)
for i in nn:
        tx[i]=float(args[i*3])
        ty[i]=float(args[i*3+1])
        rssi[i]=float(args[i*3+2])


#rssi_i=sorted(range(3),key=lambda k:rssi[k])
#print rssi_i

print tx,ty,rssi

dist[0]=10**((float(envir_para)-float(rssi[0]))/20)
dist[1]=10**((float(envir_para)-float(rssi[1]))/20)
dist[2]=10**((float(envir_para)-float(rssi[2]))/20)

#print dist
dev=[float(qq) for qq in range(3)]

dev[0]=(dist[1]+dist[2])/LA.norm([tx[1]-tx[2],ty[1]-ty[2]])
dev[1]=(dist[2]+dist[0])/LA.norm([tx[2]-tx[0],ty[2]-ty[0]])
dev[2]=(dist[1]+dist[0])/LA.norm([tx[1]-tx[0],ty[1]-ty[0]])

dev_i=sorted(range(3),key=lambda k:dev[k])
dist=[dd*1.1/dev[dev_i[0]] for dd in dist]

#print dist

dist_sorted=sorted(dist)
dist_index=sorted(range(3),key=lambda k:dist[k])

tx_s=[tx[dist_index[txx]] for txx in range(3)]
ty_s=[ty[dist_index[tyy]] for tyy in range(3)]
Axrec,Ayrec= Trilateration_3D_rec(dist_sorted,tx_s,ty_s)
print "x:",Axrec,"y=",Ayrec
