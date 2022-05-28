import sys
from turtle import color
from matplotlib.axis import Axis
import numpy as np
from btkTools import *
from btk import *
import matplotlib.pyplot as plt
from tabulate import tabulate
def lectura(file1):
    acq=smartReader(file1)
    a=0
    right=get_events(acq,'Right')
    left=get_events(acq,'Left')
    c=getAngleNames(acq)
    rodder=acq.GetPoint('RKneeAngles__py').GetValues()
    rodiz=acq.GetPoint('LKneeAngles__py').GetValues()
    cadder=acq.GetPoint('RHipAngles__py').GetValues()
    cadiz=acq.GetPoint('LHipAngles__py').GetValues()
    heelr=acq.GetPoint('RHEE').GetValues()
    heell=acq.GetPoint('LHEE').GetValues()
    point_freq=acq.GetPointFrequency()
    f=acq.GetFirstFrame()
    return right,left,acq,f,rodder,rodiz,cadder,cadiz,point_freq,heelr,heell
def datos(xheelr,xheell,Fsr,For,Fsl,Fol,point_freq):
    zancada=[]
    tapoyo=[]
    tvuelo=[]
    lpasor=[]
    if Fsr[0]>For[0]:
        For.pop(0)
    if Fsr[-1]<For[-1]:
        For.pop(-1)
    if Fsl[0]>Fol[0]:
        Fol.pop(0)
    if Fsl[-1]<Fol[-1]:
        Fol.pop(-1)
    for i in range(0,len(Fsr)-1):
        uno=np.linalg.norm(xheelr[Fsr[i+1]]-xheelr[Fsr[i]])
        zan=uno/10
        zancada.append(round(zan,2))
        tap=(For[i]-Fsr[i])*(1/point_freq)
        tvu=(Fsr[i+1]-For[i])*(1/point_freq)
        tapoyo.append(round(tap,2))
        tvuelo.append(round(tvu,2))
        try:
            if Fsr[0]<Fsl[0]:
                uno=np.linalg.norm(xheell[Fsl[i]]-xheelr[Fsr[i]])
            else:
                uno=np.linalg.norm(xheell[Fsl[i+1]]-xheelr[Fsr[i]])
            lpas=uno/10
            lpasor.append(round(lpas,2))
        except:
            pass
    pzanr=round(np.mean(zancada),2)
    papoyor=round(np.mean(tapoyo),2)
    pvuelor=round(np.mean(tvuelo),2)
    plpasr=round(np.mean(lpasor),2)
    zancada=[]
    tapoyo=[]
    tvuelo=[]
    lpasol=[]
    for i in range(0,len(Fsl)-1):
        uno=np.linalg.norm(xheell[Fsl[i+1]]-xheell[Fsl[i]])
        zan=uno/10
        zancada.append(round(zan,2))
        tap=(Fol[i]-Fsl[i])*(1/point_freq)
        tvu=(Fsl[i+1]-Fol[i])*(1/point_freq)
        tapoyo.append(round(tap,2))
        tvuelo.append(round(tvu,2))
        try:
            if Fsl[0]<Fsr[0]:
                uno=np.linalg.norm(xheelr[Fsr[i]]-xheell[Fsl[i]])
            else:
                uno=np.linalg.norm(xheelr[Fsr[i+1]]-xheell[Fsl[i]])
            lpas=uno/10
            lpasol.append(round(lpas,2))
        except:
            pass
    pzanl=round(np.mean(zancada),2)
    papoyol=round(np.mean(tapoyo),2)
    pvuelol=round(np.mean(tvuelo),2)
    plpasl=round(np.mean(lpasol),2)
    pciclor=papoyor+pvuelor
    pciclol=papoyol+pvuelol
    despeguer=round((papoyor*100)/pciclor)
    despeguel=round((papoyol*100)/pciclol)
    print('\nZancada derecha: '+str(pzanr)+' cm\nTiempo de apoyo derecha: '+
        str(papoyor)+' s\nTiempo de vuelo derecha: '+str(pvuelor)+' s\nTiempo de ciclo derecha: '+str(pciclor)+
        ' s\nLongitud de paso derecha: '+str(plpasr)+' cm\n\nZancada izquierda: '+str(pzanl)+
        ' cm\nTiempo de apoyo izquierda: '+str(papoyol)+' s\nTiempo de vuelo izquierda: '+str(pvuelol)+
        ' s\nTiempo de ciclo izquierda: '+str(pciclol)+' s\nLongitud de paso izquierda: '+str(plpasl)+' cm')
    return despeguel,despeguer
def ajustarframes(right,left):
    for m in range(len(right)):
        for i in range(len(right[m])):
            right[m][i]=right[m][i]-f
        for i in range(len(left[m])):
            left[m][i]=left[m][i]-f
    return right,left
def diferenciar_angulos(right,left):
    rd1,rd2,rd3,cd1,cd2,cd3,ri1,ri2,ri3,ci1,ci2,ci3=[],[],[],[],[],[],[],[],[],[],[],[]
    for i in range(len(right[0])-1):
        rd=rodder[right[0][i]:right[0][i+1]]
        rd1.append(rd[:,0])
        rd2.append(rd[:,1])
        rd3.append(rd[:,2])
        cd=cadder[right[0][i]:right[0][i+1]]
        cd1.append(cd[:,0])
        cd2.append(cd[:,1])
        cd3.append(cd[:,2])
    for i in range(len(left[0])-1):
        ri=rodiz[left[0][i]:left[0][i+1]]
        ri1.append(ri[:,0])
        ri2.append(ri[:,1])
        ri3.append(ri[:,2])
        ci=cadiz[left[0][i]:left[0][i+1]]
        ci1.append(ci[:,0])
        ci2.append(ci[:,1])
        ci3.append(ci[:,2])
    return rd1,rd2,rd3,cd1,cd2,cd3,ri1,ri2,ri3,ci1,ci2,ci3
def promediar(rd1,rd2,rd3,cd1,cd2,cd3,ri1,ri2,ri3,ci1,ci2,ci3):
    resul=[[],[],[],[],[],[],[],[],[],[],[],[]]
    l=list('000000000000')
    x=list('000000000000')
    f=list('000000000000')
    for a in range(0,2):
        l[0]=101/len(ri1[a])
        l[1]=101/len(ri2[a])
        l[2]=101/len(ri3[a])
        l[3]=101/len(rd1[a])
        l[4]=101/len(rd2[a])
        l[5]=101/len(rd3[a])
        l[6]=101/len(ci1[a])
        l[7]=101/len(ci2[a])
        l[8]=101/len(ci3[a])
        l[9]=101/len(cd1[a])
        l[10]=101/len(cd2[a])
        l[11]=101/len(cd3[a])
        for i in range(len(l)):
            x[i]=np.arange(0,101,l[i])
        o=np.arange(0,101)
        f[0]=np.interp(o,x[0],ri1[a])
        f[1]=np.interp(o,x[3],rd1[a])
        f[2]=np.interp(o,x[1],ri2[a])
        f[3]=np.interp(o,x[4],rd2[a])
        f[4]=np.interp(o,x[2],ri3[a])
        f[5]=np.interp(o,x[5],rd3[a])
        f[6]=np.interp(o,x[6],ci1[a])
        f[7]=np.interp(o,x[9],cd1[a])
        f[8]=np.interp(o,x[7],ci2[a])
        f[9]=np.interp(o,x[10],cd2[a])
        f[10]=np.interp(o,x[8],ci3[a])
        f[11]=np.interp(o,x[11],cd3[a])
        for a in range(len(f)):
            resul[a].append((f[a]))
    fri1=np.mean(resul[0],axis=0)
    frd1=np.mean(resul[1],axis=0)
    fri2=np.mean(resul[2],axis=0)
    frd2=np.mean(resul[3],axis=0)
    fri3=np.mean(resul[4],axis=0)
    frd3=np.mean(resul[5],axis=0)
    fci1=np.mean(resul[6],axis=0)
    fcd1=np.mean(resul[7],axis=0)
    fci2=np.mean(resul[8],axis=0)
    fcd2=np.mean(resul[9],axis=0)
    fci3=np.mean(resul[10],axis=0)
    fcd3=np.mean(resul[11],axis=0)
    return fri1,frd1,fri2,frd2,fri3,frd3,fci1,fcd1,fci2,fcd2,fci3,fcd3
def graficar(fri1,frd1,fri2,frd2,fri3,frd3,fci1,fcd1,fci2,fcd2,fci3,fcd3,despeguel,despeguer):
    plt.figure(figsize=(3,2))
    plt.suptitle('Ángulos en un ciclo de marcha')
    plt.subplot(321)
    plt.title('Rodilla')
    plt.ylabel('Flexión/extensión')
    plt.plot(despeguer,frd1[despeguer],marker='o')
    plt.plot(despeguel,fri1[despeguel],marker='o')
    plt.plot(fri1)
    plt.plot(frd1)
    plt.legend(['Despegue D','Despegue I','Izquierda','Derecha'])
    plt.subplot(322)
    plt.title('Cadera')
    plt.ylabel('Flexión/extensión')
    plt.plot(despeguer,fcd1[despeguer],marker='o')
    plt.plot(despeguel,fci1[despeguel],marker='o')
    plt.plot(fci1)
    plt.plot(fcd1)
    plt.legend(['Despegue D','Despegue I','Izquierda','Derecha'])
    plt.subplot(323)
    plt.ylabel('Abducción/aducción')
    plt.plot(despeguer,frd2[despeguer],marker='o')
    plt.plot(despeguel,fri2[despeguel],marker='o')
    plt.plot(fri2)
    plt.plot(frd2)
    plt.legend(['Despegue D','Despegue I','Izquierda','Derecha'])
    plt.subplot(324)
    plt.ylabel('Abducción/aducción')
    plt.plot(despeguer,fcd2[despeguer],marker='o')
    plt.plot(despeguel,fci2[despeguel],marker='o')
    plt.plot(fci2)
    plt.plot(fcd2)
    plt.legend(['Despegue D','Despegue I','Izquierda','Derecha'])
    plt.subplot(325)
    plt.ylabel('Rotación')
    plt.xlabel('Gait cycle (%)')
    plt.plot(despeguer,frd3[despeguer],marker='o')
    plt.plot(despeguel,fri3[despeguel],marker='o')
    plt.plot(fri3)
    plt.plot(frd3)
    plt.legend(['Despegue D','Despegue I','Izquierda','Derecha'])
    plt.subplot(326)
    plt.ylabel('Rotación')
    plt.xlabel('Gait cycle (%)')
    plt.plot(despeguer,fcd3[despeguer],marker='o')
    plt.plot(despeguel,fci3[despeguel],marker='o')
    plt.plot(fci3)
    plt.plot(fcd3)
    plt.legend(['Despegue D','Despegue I','Izquierda','Derecha'])
    plt.show()
try:
    registro=str(sys.argv[1])
except:
    registro='Subject02_01.c3d'
right,left,acq,f,rodder,rodiz,cadder,cadiz,point_freq,heelr,heell=lectura(registro)
right,left=ajustarframes(right,left)
rd1,rd2,rd3,cd1,cd2,cd3,ri1,ri2,ri3,ci1,ci2,ci3=diferenciar_angulos(right,left)
fri1,frd1,fri2,frd2,fri3,frd3,fci1,fcd1,fci2,fcd2,fci3,fcd3=promediar(rd1,rd2,rd3,cd1,cd2,cd3,ri1,ri2,ri3,ci1,ci2,ci3)
despeguel,despeguer=datos(heelr,heell,right[0],right[1],left[0],left[1],point_freq)
graficar(fri1,frd1,fri2,frd2,fri3,frd3,fci1,fcd1,fci2,fcd2,fci3,fcd3,despeguel,despeguer)
