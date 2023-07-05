import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from datetime import time
from datetime import timedelta
import xlrd
import numpy as np
import statistics as st
import pandas as pd 
import matplotlib.dates as mdates

def mean(someList):
    total = 0
    for a in someList:
        total += float(a)
    mean = total/len(someList)
    return mean
def standDev(someList):
    listMean = mean(someList)
    dev = 0.0
    for i in range(len(someList)):
        dev += (someList[i]-listMean)**2
    dev = dev**(1/2.0)
    return dev

def correlCo(someList1, someList2):

    # First establish the means and standard deviations for both lists.
    xMean = mean(someList1)
    yMean = mean(someList2)
    xStandDev = standDev(someList1)
    yStandDev = standDev(someList2)
    # r numerator
    rNum = 0.0
    for i in range(len(someList2)):
        rNum += (someList1[i]-xMean)*(someList2[i]-yMean)

    # r denominator
    rDen = xStandDev * yStandDev

    r =  rNum/rDen
    return r
    
def pos_reader(finame,fixE,fixN,fixH):
    f = open(finame,"r")
    data = f.readlines()
    for i in range(150):
        if data[i].split()[0] ==  "FIN":
            break
    del data[:i]
    f.close()
    
    i=0
    deasting =[]
    dnorthing =[]
    dheight=[]
    dhor=[]
    epok=[]
   
    while i<(len(data)):
        deasting.append(round(float(data[i].split()[24])-fixE,3)*100)
        dnorthing.append(round(float(data[i].split()[25])-fixN,3)*100)
        dheight.append(round(float(data[i].split()[22])-fixH,3)*100)
        dhor.append(round((float(deasting[i])**2+float(dnorthing[i])**2)**(0.5),3))
        epok.append(datetime.strptime(str((str(data[i].split()[4])+" "+str(data[i].split()[5]))),"%Y-%m-%d %H:%M:%S.%f"))
        i+=1
    return deasting, dnorthing, dheight, dhor, epok

def leap_sec(data):
    epok = []
    for i in range(len(data)):
        epok.append(data[i] - timedelta(seconds = 18))
    return epok
    
def cumu_sms(data):
    cumu = []
    cumu.append(0)
    i = 1
    while i < (len(data)):
        cumu.append(data[i]+data[i-1])
        i+=1
    return cumu
    
def disp2vel(data):
    vel = []
    vel.append(0)
    i = 1
    while i < (len(data)):
        vel.append((data[i]-data[i-1]))
        i+=1
    return vel

def vel2acc(data):
    acc = []
    acc.append(0)
    i = 1
    while i < (len(data)):
        acc.append((data[i]-data[i-1]))
        i+=1
    return acc
def acc2vel(data):
    vel = []
    vel.append(0)
    i = 1
    while i < (len(data)):
        vel.append((vel[i-1]+data[i]*0.01))
        i+=1
    return vel

def vel2disp(data):
    disp = []
    disp.append(0)
    i = 1
    while i < (len(data)):
        disp.append((disp[i-1]+data[i]*0.01))
        i+=1
    return disp
    
def disp2vel_SGM(data,epok):
    vel = []
    vel.append(0)
    i = 1
    while i < (len(epok)):
        vel.append((data[epok[i]]-data[epok[i-1]]))
        i+=1
    return vel  
       
def graph_sum(epoch,epokhız,var1,var2,var3,Svar1,Svar2,Svar3,Tvar1,Tvar2,Tvar3,finame,event_time,magnitude,location):
    
    f,ax = plt.subplots(3,3,sharex=True, sharey=False)
    plt.gcf().set_size_inches(10,6,forward=True)
    plt.suptitle(finame+" Accelerometer Station\n",fontsize=20)
    
    print("Displacement maks:", max([max(Tvar1),max(Tvar2),max(Tvar3)])," min:",min([min(Tvar1),min(Tvar2),min(Tvar3)]))
    print("Hız maks:", max([max(var1),max(var2),max(var3)])," min:",min([min(var1),min(var2),min(var3)]))
    print("İvme maks:", max([max(Svar1),max(Svar2),max(Svar3)])," min:",min([min(Svar1),min(Svar2),min(Svar3)]))
    
    # set_ylim values for plot
    dis_ymin = -250
    dis_ymaks = 250
    
    hız_ymin = -150
    hız_ymaks = 150
    
    ivme_ymin = -600
    ivme_ymaks = 600
    
    #yer değiştirme -- displacement
    ax[0][0].set_title("Displacements (cm)",fontsize=10)
    #ax[0][0].plot(GNSSepok,GNSSdE,marker="o",color="skyblue" ,markersize = 0.5,label="GNSS")
    ax[0][0].plot(epoch,Tvar1,marker="o",color="darkorange", markersize = 0.5,label="SMS")
    #ax[0][0].text(0.87, 0.05, str("Corr. :"+"{:.2f}".format(CdispdE)), horizontalalignment='center', verticalalignment='center', transform=ax[0][0].transAxes,fontsize=8)
    ax[0][0].grid(linestyle='--', linewidth=0.25)
    ax[0][0].set_ylabel('E -- W',fontsize = 7, labelpad = 0.05)

    ax[0][0].set_ylim(dis_ymin,dis_ymaks)
    ax[0][0].set_yticks(np.arange(dis_ymin,dis_ymaks+0.01, dis_ymaks/2))
    ax[0][0].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    ax[0][0].xaxis.set_major_locator(mdates.SecondLocator(interval = 30))
    ax[0][0].axvline(x = event_time,linestyle="--",linewidth=1 ,color="r")
    ax[0][0].grid(True, linestyle='--',linewidth=0.25)
    ax[0][0].tick_params(labelsize=8)
    
    #ax[1][0].plot(GNSSepok,GNSSdN,marker="o",color="skyblue" ,markersize =0.5,label="GNSS")
    ax[1][0].plot(epoch,Tvar2,marker="o", color="darkorange", markersize = 0.5,label="SGMS")
    #ax[1][0].text(0.87, 0.05, str("Corr. :"+"{:.2f}".format(CdispdN)), horizontalalignment='center', verticalalignment='center', transform=ax[1][0].transAxes,fontsize=8)
    
    ax[1][0].grid(linestyle='--', linewidth=0.25)
    ax[1][0].set_ylabel('N -- S',fontsize = 7, labelpad = 0.05)
    ax[1][0].axvline(x = event_time,linestyle="--",linewidth=1 ,color="r")
    #ax[1].set_ylim(-0.2,0.2) 
    ax[1][0].set_ylim(dis_ymin,dis_ymaks)
    ax[1][0].set_yticks(np.arange(dis_ymin,dis_ymaks+0.01, dis_ymaks/2))
    ax[1][0].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    ax[1][0].xaxis.set_major_locator(mdates.SecondLocator(interval = 30))
    ax[1][0].grid(True, linestyle='--',linewidth=0.25)
    #plt.xlim(datetime.strptime("2020-10-30 11:51:00","%Y-%m-%d %H:%M:%S"), datetime.strptime("2020-10-30 11:53:00","%Y-%m-%d %H:%M:%S"))
    ax[1][0].tick_params(labelsize=8)
    
    #ax[2][0].plot(GNSSepok,GNSSdH,marker="o", color="skyblue" ,markersize =0.5,label="GNSS")
    ax[2][0].plot(epoch,Tvar3,marker="o", color="darkorange", markersize = 0.5,label="SGMS")
    #ax[2][0].text(0.87, 0.05, str("Corr. :"+"{:.2f}".format(CdispdH)), horizontalalignment='center', verticalalignment='center', transform=ax[2][0].transAxes,fontsize=8)
    
    ax[2][0].grid(linestyle='--', linewidth=0.25)
    ax[2][0].set_ylabel('Up',fontsize = 7, labelpad = 0.05)
    ax[2][0].axvline(x = event_time,linestyle="--",linewidth=1 ,color="r")
    #ax[1].set_ylim(-0.2,0.2) 
    ax[2][0].set_ylim(dis_ymin,dis_ymaks)
    ax[2][0].set_yticks(np.arange(dis_ymin,dis_ymaks+0.01, dis_ymaks/2))
    ax[2][0].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    ax[2][0].xaxis.set_major_locator(mdates.SecondLocator(interval = 30))
    ax[2][0].grid(True, linestyle='--',linewidth=0.25)
    #plt.xlim(datetime.strptime("2020-10-30 11:51:00","%Y-%m-%d %H:%M:%S"), datetime.strptime("2020-10-30 11:53:00","%Y-%m-%d %H:%M:%S"))
    ax[2][0].tick_params(labelsize=8)

    #HIZ -- velocity
    ax[0][1].set_title("Velocity (cm/sec)",fontsize=10)
    #ax[0][1].plot(GNSSepok,GNSSdEvel,marker="o",color="skyblue" ,markersize = 0.5,label="GNSS")
    ax[0][1].plot(epokhız,var1,marker="o",color="darkorange", markersize = 0.5,label="SMS")
    #ax[0][1].text(0.87, 0.05, str("Corr. :"+"{:.2f}".format(CveldE)), horizontalalignment='center', verticalalignment='center', transform=ax[0][1].transAxes,fontsize=8)
    
    ax[0][1].grid(linestyle='--', linewidth=0.25)
    #ax[0][1].legend(loc = 1,fontsize = 'x-small',ncol = 3,markerscale=2)
    ax[0][1].set_ylabel('E -- W',fontsize = 7, labelpad = 0.05)
    #ax[0].set_ylim(-0.3,0.3)
    ax[0][1].set_ylim(hız_ymin,hız_ymaks)
    ax[0][1].set_yticks(np.arange(hız_ymin,hız_ymaks+0.01, hız_ymaks/2))
    
    ax[0][1].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    ax[0][1].xaxis.set_major_locator(mdates.SecondLocator(interval = 30))
    ax[0][1].axvline(x =event_time,linestyle="--",linewidth=1 ,color="r")
    ax[0][1].grid(True, linestyle='--',linewidth=0.25) 
    #plt.xlim(datetime.strptime("2020-10-30 11:51:00","%Y-%m-%d %H:%M:%S"), datetime.strptime("2020-10-30 11:53:00","%Y-%m-%d %H:%M:%S"))
    ax[0][1].tick_params(labelsize=8)
    
    #ax[1][1].plot(GNSSepok,GNSSdNvel,marker="o", color="skyblue" ,markersize =0.5,label="GNSS")
    ax[1][1].plot(epokhız,var2,marker="o", color="darkorange", markersize =0.5,label="SMS")
    #ax[1][1].text(0.87, 0.05, str("Corr. :"+"{:.2f}".format(CveldN)), horizontalalignment='center', verticalalignment='center', transform=ax[1][1].transAxes,fontsize=8)
    
    ax[1][1].grid(linestyle='--', linewidth=0.25)
    ax[1][1].set_ylabel('N -- S',fontsize = 7, labelpad = 0.05)
    ax[1][1].axvline(x = event_time,linestyle="--",linewidth=1 ,color="r")
    #ax[1].set_ylim(-0.2,0.2) 
    ax[1][1].set_ylim(hız_ymin,hız_ymaks)
    ax[1][1].set_yticks(np.arange(hız_ymin,hız_ymaks+0.01, hız_ymaks/2))
    ax[1][1].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    ax[1][1].xaxis.set_major_locator(mdates.SecondLocator(interval = 30))
    ax[1][1].grid(True, linestyle='--',linewidth=0.25)
    #plt.xlim(datetime.strptime("2020-10-30 11:51:00","%Y-%m-%d %H:%M:%S"), datetime.strptime("2020-10-30 11:53:00","%Y-%m-%d %H:%M:%S"))
    ax[1][1].tick_params(axis='y',labelsize=8)
    f.text(0.5,0.5 , 'BM ITU GEOMATICS',
        fontsize=40, color='gray', alpha=0.5,
        ha='center', va='center', rotation = 30)
    
    #ax[2][1].plot(GNSSepok,GNSSdHvel,marker="o", color="skyblue" ,markersize = 0.5,label="GNSS")
    ax[2][1].plot(epokhız,var3,marker="o", color="darkorange", markersize = 0.5,label="SMS")
    #ax[2][1].text(0.87, 0.05, str("Corr. :"+"{:.2f}".format(CveldH)), horizontalalignment='center', verticalalignment='center', transform=ax[2][1].transAxes,fontsize=8)
    
    ax[2][1].grid(linestyle='--', linewidth=0.25)
    ax[2][1].set_ylabel('Up',fontsize = 7, labelpad = 0.05)
    ax[2][1].axvline(x = event_time,linestyle="--",linewidth=1 ,color="r")
    #ax[1].set_ylim(-0.2,0.2) 
    ax[2][1].set_ylim(hız_ymin,hız_ymaks)
    ax[2][1].set_yticks(np.arange(hız_ymin,hız_ymaks+0.01, hız_ymaks/2))
    ax[2][1].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    ax[2][1].xaxis.set_major_locator(mdates.SecondLocator(interval = 15))
    ax[2][1].grid(True, linestyle='--',linewidth=0.25)
    #plt.xlim(datetime.strptime("2020-10-30 11:51:00","%Y-%m-%d %H:%M:%S"), datetime.strptime("2020-10-30 11:53:00","%Y-%m-%d %H:%M:%S"))
    ax[2][1].tick_params(axis='y',labelsize=8)
    ax[2][1].tick_params(axis='x',labelsize=8)
    
    #ivme -- acceleration
    ax[0][2].set_title("Acceleration (cm/sec\N{SUPERSCRIPT TWO})",fontsize=10)
    #ax[0][2].plot(GNSSepok,GNSSdEacc,marker="o",color="skyblue" ,markersize = 0.5,label="GNSS")
    ax[0][2].plot(epokhız,Svar1,marker="o",color="darkorange", markersize = 0.5,label="SGMS")
    #ax[0][2].text(0.87, 0.05, str("Corr. :"+"{:.2f}".format(CaccdE)), horizontalalignment='center', verticalalignment='center', transform=ax[0][2].transAxes,fontsize=8)
    
    ax[0][2].grid(linestyle='--', linewidth=0.25)
    ax[0][2].legend(loc = 1,fontsize = 'x-small',ncol = 3,markerscale=2)
    ax[0][2].set_ylabel('E -- W',fontsize = 7, labelpad = 0.05)
    ax[0][2].set_ylim(ivme_ymin,ivme_ymaks)
    ax[0][2].set_yticks(np.arange(ivme_ymin,ivme_ymaks+0.01, ivme_ymaks/2))
    ax[0][2].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    ax[0][2].xaxis.set_major_locator(mdates.SecondLocator(interval = 30))
    ax[0][2].axvline(x =event_time,linestyle="--",linewidth=1 ,color="r")
    ax[0][2].grid(True, linestyle='--',linewidth=0.25) 
    ax[0][2].tick_params(axis='y',labelsize=8)
    
    #ax[1][2].plot(GNSSepok,GNSSdNacc,marker="o",color="skyblue" ,markersize =0.5,label="GNSS")
    ax[1][2].plot(epokhız,Svar2,marker="o",color="darkorange", markersize = 0.5,label="SMS")
    #ax[1][2].text(0.87, 0.05, str("Corr. :"+"{:.2f}".format(CaccdN)), horizontalalignment='center', verticalalignment='center', transform=ax[1][2].transAxes,fontsize=8)
    
    ax[1][2].grid(linestyle='--', linewidth=0.25)
    ax[1][2].set_ylabel('N -- S',fontsize = 7, labelpad = 0.05)
    ax[1][2].axvline(x = event_time,linestyle="--",linewidth=1 ,color="r")
    ax[1][2].set_ylim(ivme_ymin,ivme_ymaks)
    ax[1][2].set_yticks(np.arange(ivme_ymin,ivme_ymaks+0.01, ivme_ymaks/2))
    ax[1][2].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    ax[1][2].xaxis.set_major_locator(mdates.SecondLocator(interval = 30))
    ax[1][2].grid(True, linestyle='--',linewidth=0.25)
    ax[1][2].tick_params(axis='y',labelsize=8)

    #ax[2][2].plot(GNSSepok,GNSSdHacc,marker="o", color="skyblue" ,markersize =0.5,label="GNSS")
    ax[2][2].plot(epokhız,Svar3,marker="o", color="darkorange", markersize = 0.5,label="SMS")
    #ax[2][2].text(0.87, 0.05, str("Corr. :"+"{:.2f}".format(CaccdH)), horizontalalignment='center', verticalalignment='center', transform=ax[2][2].transAxes,fontsize=8)
    
    ax[2][2].grid(linestyle='--', linewidth=0.25)
    ax[2][2].set_ylabel('Up',fontsize = 7, labelpad = 0.05)
    ax[2][2].axvline(x = event_time,linestyle="--",linewidth=1 ,color="r")
    ax[2][2].set_ylim(ivme_ymin,ivme_ymaks)
    ax[2][2].set_yticks(np.arange(ivme_ymin,ivme_ymaks+0.01, ivme_ymaks/2))
    ax[2][2].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    ax[2][2].xaxis.set_major_locator(mdates.SecondLocator(interval = 30))
    ax[2][2].grid(True, linestyle='--',linewidth=0.25)

    plt.xlim(datetime.strptime("2023-02-06 01:17:00","%Y-%m-%d %H:%M:%S"), datetime.strptime("2023-02-06 01:19:00","%Y-%m-%d %H:%M:%S"))
    ax[2][2].tick_params(axis='x',labelsize=8)
    ax[2][2].tick_params(axis='y',labelsize=8)
    f.text(0.5, 0.005, 'Time (hh:mm:ss)', ha='center')
    plt.tick_params(axis='both',  labelsize=8)
    f.autofmt_xdate()
    plt.tight_layout()

    f.text(0.34,0.9,str(event_time.strftime("%d.%m.%Y %H:%M:%S")+" (UTC) "+location+" Earthquake MW "+ str(magnitude) + " (AFAD - TADAS)"),fontsize=10 , ha='center', va='center')
    plt.savefig(finame+"_ENH.png", dpi=300, pad_inches = 0.02) # bbox_inches = 'tight',

    plt.close('all')
    
def reader(fname):
    filex = open(fname,"r")
    data = filex.readlines()
    filex.close()
    
    i = 0
    while i<(len(data)):
        if data[i].split()[0] == "DATE_TIME_FIRST_SAMPLE_YYYYMMDD_HHMMSS:":
            print(str(data[i].split()[1])+" "+str(data[i].split()[2]))
            start = datetime.strptime(str(data[i].split()[1])+" "+str(data[i].split()[2]),"%Y/%m/%d %H:%M:%S.%f")
        elif data[i].split()[0] == "EVENT_TIME_HHMMSS:" :
            event_time = datetime.strptime(str(data[i-1].split()[1])+" "+str(data[i].split()[1]),"%Y/%m/%d %H:%M:%S.%f")
        elif data[i].split()[0] == "SAMPLING_INTERVAL_S:" :
            sampling_rate = float(data[i].split()[1])
        elif data[i].split()[0] == "MAGNITUDE_W:" :
            magnitude = float(data[i].split()[1])
        elif data[i].split()[0] == "LOCATION:" :
            location = str(data[i].split()[1].split("_")[0]+" "+data[i].split()[1].split("_")[1])
        if data[i].split()[0] == "USER5:":
            i+=1
            break
        i+=1

    del data[:i]
    
    end = start+ timedelta(seconds = len(data)*0.01)
    ddata = []

    for i in range(len(data)):
        ddata.append(float(data[i].split()[0]))

    return start, end, ddata, event_time,sampling_rate,magnitude,location


    
start, end, cesmeivmeE,event_time,sampling_rate,magnitude,location = reader("data/"+[f for f in os.listdir("data/") if f.endswith("E.asc")][0])
start, end, cesmeivmeN,event_time,sampling_rate,magnitude,location = reader("data/"+[f for f in os.listdir("data/") if f.endswith("N.asc")][0])
start, end, cesmeivmeU,event_time,sampling_rate,magnitude,location = reader("data/"+[f for f in os.listdir("data/") if f.endswith("U.asc")][0])

cesmehızE = acc2vel(cesmeivmeE)
cesmehızN = acc2vel(cesmeivmeN)
cesmehızU = acc2vel(cesmeivmeU)

print(event_time)
cesmedispE = vel2disp(cesmehızE)
cesmedispN = vel2disp(cesmehızN)
cesmedispU = vel2disp(cesmehızU)


epok2 = []
epok2.append(start)
i = 1
while i < (len(cesmeivmeE)):
    epok2.append(epok2[i-1]+ timedelta(seconds = sampling_rate))
    i += 1
print(end , epok2[-1])

graph_sum(epok2, epok2, cesmehızE ,cesmehızN ,cesmehızU ,cesmeivmeE,cesmeivmeN,cesmeivmeU,cesmedispE,cesmedispN,cesmedispU,"Pazarcık",event_time,magnitude,location)