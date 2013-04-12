#THIS PROGRAM TAKES 4 INPUT FILES
#THIS MODULE FIRST CLASSIFIES THE WINDOW LIGHT AND INDOOR LIGHT (AT ONE SENSOR)
#BY CLOUDINESS (BINARY) AND THEN SUNANGLE (TILT) AND HOUR OF DAY (BINARY)
#CLOUDINESS IS CLOUDY OR SUNNY
#HOUR OF DAY IS AM OR PM
#THIS MODEL PERFORMS LINEAR REGRESSION BETWEEN INDIVIDUAL WORKPLANE LIGHT AND WINDOW LIGHT FOR BINS OF SUN TILT AND TIME OF DAY (LIKE am OR pm)

print "This program computes correlation between sun position and received light from a dataset labelled by cloudiness"
print "   "
print "It shows daylight data by sun position, time and cloudiness"

import numpy as np
import scipy as sp
from scipy import stats
from numpy import vstack
import scikits.statsmodels.api as sm
import time
import datetime
from datetime import date
import matplotlib as mpl
from matplotlib import pyplot as plt
from time import mktime, localtime, gmtime, strftime
import pdb


window="C:\Users\chandrayee\Documents\NASA\ParsedData\windowsensors\\model\\winmodeltrain_1128_0113parsedfinal"+".txt"
getsunpos=open("C:\Users\chandrayee\Documents\NASA\ParsedData\sunpos_1128_0113.txt")
getcloudiness=open("C:\Users\chandrayee\Documents\NASA\ParsedData\\berkeleyweather\\1128_0113.txt")
getdaylight=open(window)
linelist2=getdaylight.readlines()
linelist3=getsunpos.readlines()
linelist4=getcloudiness.readlines()
count=0
print "   "
print "The lengths of the datasets are ", len(linelist2),len(linelist3),len(linelist4)
#define local arrays
daytype=[]
datamorningsunny=[]
datamorningcloudy=[]
dataafternoonsunny=[]
dataafternooncloudy=[]
sunmornsunny=[]
sunmorncloudy=[]
sunaftersunny=[]
sunaftercloudy=[]
amsunny=[]
amcloudy=[]
pmsunny=[]
pmcloudy=[]
pm=[]
wstam=[]
wstpm=[]
dlttrail=[]
yr=[]
mon=[]
day=[]
data=[]
time=[]
a=len(linelist2)
print "  "
twelvehourtime=np.arange(1,12)
twentyfourhourtime=np.arange(13,24)
#arrange data in bins for hours of day, cloudiness into arrays 
for count in range(len(linelist4)):
    cloud=str.split(linelist4[count],'\t')
    hourly=str.split(cloud[3],':')
    #print hourly
    ampm=str.split(hourly[1])
    yr.append(cloud[2])
    mon.append(cloud[0])
    day.append(cloud[1])
    #convert time to hours minutes
    #print hourly[0]
    for j in range(len(twelvehourtime)):
        if ampm[1]=='PM' and float(hourly[0])==twelvehourtime[j]:
            #print cloud[1],'  ',cloud[0], ampm[1], hourly[0], twelvehourtime[j],twentyfourhourtime[j] 
            time.append(twentyfourhourtime[j])
        elif ampm[1]=='AM'and float(hourly[0])==twelvehourtime[j]:
            #print cloud[1],'  ',cloud[0], ampm[1], hourly[0], twelvehourtime[j],hourly[0]
            time.append(int(hourly[0]))
    if ampm[1]=='AM'and int(hourly[0])==12:
        #print cloud[1],'  ',cloud[0],ampm[1], hourly[0], '12', '0'
        time.append('0')
    elif ampm[1]=='PM'and int(hourly[0])==12:
        #print cloud[1],'  ',cloud[0],ampm[1], hourly[0], '12', '12'
        time.append('12')
    data.append(cloud[14])
print len(time),len(data)
#newfile=open("C:\Users\chandrayee\Documents\NASA\ParsedData\windowsensors\\model\\labelled_1128_0113.txt",'a')
#labels='year'+'\t'+'month'+'\t'+'day'+'\t'+'hour'+'\t'+'minute'+'\t'+'value'+'\t'+'altlabel'+'\t'+'azilabel'+'\t'+'cloudlabel'+'\n'
#newfile.write(labels)
#define lists
cloudylabel=[]
altitudelabel=[]
azimuthlabel=[]
lightvalue=[]
hourtime=[]
for count in range(a):
    dlt1=str.split(linelist2[count],'\t')
    dlt=str.split(dlt1[7],'\n')
    sun=str.split(linelist3[count],'\t')
    azimuth=str.split(sun[7],'\n')
    azi=azimuth[0]
    altitude=round(float(sun[6]),2)
    for count in range(len(time)):
        if int(dlt1[3])==int(time[count]):
            cloudlabel=data[count]
            #print int(dlt1[3]),'  ', int(time[count])
    #labels=sun[0]+'\t'+sun[1]+'\t'+sun[2]+'\t'+sun[3]+'\t'+sun[4]+'\t'+str(round(float(dlt[0]),2))+'\t'+str(altitude)+'\t'+azi+'\t'+cloudlabel+'\n'
    #newfile.write(labels)
    cloudylabel.append(cloudlabel)
    altitudelabel.append(altitude)
    azimuthlabel.append(azi)
    lightvalue.append(str(round(float(dlt[0]),2)))
    hourtime.append(sun[3]+':'+sun[4])
#newfile.close()
print "  "
print "This part will classify the data by cloudiness and perform regression between the sun altitude and the light level for each level of cloudiness"
cloudiness=['Clear','Partly','Scattered','Light','Mostly','Rain','Overcast','Heavy','Fog','Haze']
###perform OLS
labeledalt=dict()
labeledlight=dict()
coeff=dict()
constant=dict()
rvalue=dict()
for j in range(len(cloudiness)):
    labeledlight[j]=[]
    labeledalt[j]=[]
    coeff[j]=[]
    constant[j]=[]
    rvalue[j]=[]
    for count in range(len(cloudylabel)):
        if cloudylabel[count]==cloudiness[j]:
            labeledalt[j].append(float(altitudelabel[count]))
            labeledlight[j].append(float(lightvalue[count]))
    adata=vstack((labeledalt[j],labeledlight[j]))
    realadata=adata.transpose()
    y=realadata[:,0]
    x=realadata[:,1]
    X=sm.add_constant(x)
    model = sm.OLS(y, X)
    fitmorn=model.fit()
    coeff[j]=round(fitmorn.params[0],3)
    constant[j]=round(fitmorn.params[1],3)
    rvalue[j]=round(fitmorn.rsquared,3)
#close files after regression
getsunpos.close()
getcloudiness.close()
getdaylight.close()
print "   "
print coeff
print "    "
print "done"
