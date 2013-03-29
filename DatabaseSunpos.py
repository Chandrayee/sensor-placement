#THIS MODEL CALCULATES THE SUN AZIMUTH AND ALTITUDE AT ANY PLACE AND ANY TIME OF THE DAY
#THE SUN POSITION ALGORITHM IS TAKEN FROM J.K. MICHALSKY
#Inputs: latitude, longitude, time zone, time of the year (in day, month, year, hours, minutes and seconds)
#Output:Local time (day, month, year, hours, minutes, seconds), Azimuth and Altitude 

import numpy as np
from numpy import vstack
import scipy as sp
from scipy import stats
import time
import scikits.statsmodels.api as sm
import matplotlib as mpl
from matplotlib import pyplot as plt
import datetime
from time import mktime, localtime, gmtime, strftime
import pytz
from pytz import timezone
import math
import pdb


#user inputs
#def sunpos(lat,lon,timezon):
lat=raw_input("enter the latitude of the place (enter in degrees, minutes and seconds, north is positive):   ")
lon=raw_input("enter the longitude of the place (put W for west and E for east at the end of the longitude):   ")
timezon=raw_input("enter the name of the place as within quotes as country/city with spaces replaced by underscore:   ")
splat=str.split(lat)
splon=str.split(lon)
latitude=float(splat[0])+float(splat[1])/60+float(splat[2])/3600
if splon[3]=='W':
    longitude=-(float(splon[0])+float(splon[1])/60+float(splon[2])/3600)
else:
    longitude=float(splon[0])+float(splon[1])/60+float(splon[2])/3600
local = pytz.timezone (timezon)
#time matching with sensed data: this part takes time input from the raw data file and outputs the corresponding values
timedata=open("C:\Users\chandrayee\Documents\NASA\ParsedData\windowsensors\model\winmodeltrain_1128_0113parsedfinal.txt")
savesunpos=open("C:\Users\chandrayee\Documents\NASA\ParsedData\sunpos_1128_0113.txt",'a')
getdatetime=timedata.readlines()
i=0
elevation=[]
azimuth=[]
data=[]
for i in range(len(getdatetime)):
#convert local time to universal time
    datentime=str.split(getdatetime[i])
    loctime=datentime[0]+'-'+datentime[1]+'-'+datentime[2]+' '+datentime[3]+':'+datentime[4]+':'+datentime[5]
    naive = datetime.datetime.strptime (loctime, "%Y-%m-%d %H:%M:%S")
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone (pytz.utc)
    utc_dt.strftime ("%Y-%m-%d %H:%M:%S")
    utcsplit=str.split(str(utc_dt))
    utcdt=str.split(utcsplit[0],'-')
    utctime=str.split(utcsplit[1],'+')
    utctimefinal=str.split(utctime[0],':')
    year=utcdt[0]
    month=utcdt[1]
    day=utcdt[2]
    hour=utctimefinal[0]
    minute=utctimefinal[1]
    second=utctimefinal[2]
    #+1 for e and -1 for w for dst
    houronly=float(hour)+float(minute)/60+float(second)/3600
    delta=int(year)-1949
    leap=int(delta/4)
    doy=[31,28,31,30,31,30,31,31,30,31,30,31]
    if int(year)%4==0:
        doy[1]=29
    dayofyear=sum(doy[0:(int(month)-1)])+int(day)
    jd=2432916.5+delta*365+dayofyear+leap+houronly/24
    actime=jd-2451545
    pi=3.1415926535897931
    rad=pi/180
    
    #mean longitude in degrees between 0 and 360
    L=(280.46+0.9856474*actime)%360
    if L<0:
        L+=360
    #mean anomaly in radians
    g=(357.528+0.9856003*actime)%360
    if g<0:
        g+=360
    g=g*rad
    #ecliptic longitude in radians
    eclong=(L+1.915*math.sin(g)+0.02*math.sin(2*g))%360
    if eclong<0:
        eclong+=360
    eclong=eclong*rad
    #ecliptic obliquity in radians
    ep=(23.439-0.0000004*actime)*rad
    #get right ascension in radians between 0 and 2 pi
    num=math.cos(ep)*math.sin(eclong)
    den=math.cos(eclong)
    ra=math.atan(num/den)
    if den<0:
        ra+=pi
    elif den>0 and num<0:
        ra+=2*pi
    #get declination in radians
    dec=math.asin(math.sin(ep)*math.sin(eclong))
    #get greenwich mean sidereal time
    gmst=(6.697375 + 0.0657098242*actime+houronly)%24
    if gmst<0:
        gmst+=24
    #get local mean sidereal time in radians
    lmst=(gmst+longitude/15)%24
    if lmst<0:
        lmst+=24
    lmst=lmst*15*rad
    #get hour angle in radians between -pi and pi
    ha=lmst-ra
    if ha<-pi:
        ha+=2*pi
    elif ha>pi:
        ha=ha-2*pi
    #change latitude to radians
    latrad=latitude*rad
    #calculate elevation and azimuth in degrees
    el=math.asin(math.sin(dec)*math.sin(latrad)+math.cos(dec)*math.cos(latrad)*math.cos(ha))
    az=math.asin(-math.cos(dec)*math.sin(ha)/math.cos(el*rad))
    #approximation for azimuth
    #if az==90, elcrit=math.degrees(math.asin(math.sin(dec)/math.sin(latitude)))
    if math.sin(dec)-math.sin(el)/math.sin(latrad)>=0 and math.sin(az)<0:
        az+=2*pi
    elif math.sin(dec)-math.sin(el)/math.sin(latrad)<0:
        az=pi-az
    eldeg=round(math.degrees(el),2)
    azdeg=round(math.degrees(az),2)
    if eldeg>-0.56:
        refrac = 3.51561*(0.1594+0.0196*eldeg+0.00002*math.pow(eldeg,2))/(1+0.505*eldeg+0.0845*math.pow(eldeg,2))
    else:
        refrac = 0.56
    eldeg=eldeg+refrac
    #print eldeg,azdeg
#data is saved for future reference
    newline=datentime[0]+'\t'+datentime[1]+'\t'+datentime[2]+'\t'+datentime[3]+'\t'+datentime[4]+'\t'+datentime[5]+'\t'+str(eldeg)+'\t'+str(azdeg)+'\n'
    savesunpos.write(newline)
    elevation.append(eldeg)
    azimuth.append(azdeg)
    data.append(float(datentime[7]))
savesunpos.close()
elevationnum=sp.array(elevation)
azimuthnum=sp.array(azimuth)
datanum=sp.array(data)
print "  "
print "done"
##    gradient, intercept, r_value, p_value, std_err = stats.linregress(elevation,data)
##    print [gradient,intercept,r_value,p_value,std_err]
##    scatter=plt.plot(elevation, data,'bo')
##    plt.xlabel('Sun Elevation (deg)')
##    plt.ylabel('Illumination@sensor9 (lux)')
##    plt.title('Scatter plot of sun elevation vs. Illumination')
##    plt.show()
    #return elevationnum, azimuthnum




