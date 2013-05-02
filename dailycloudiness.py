#THIS MODULE COMPUTES THE AVERAGE CLOUDINESS OF A DAY. IT TAKES THE DAY AND HOURLY CLOUDINESS FROM ONLINE WEATHER FILE AS INPUT
#CLOUDINESS HAS 8 STANDARD CATEGORIES MEASURED IN OKTAS
#THE MODULE FIRST CONVERTS THE CLOUDINESS INTO CORRESPONSING OKTAS AS CLEAR=0, PARTLY CLOUDY=2, SCATTERED CLOUDS=4, MOSTLT CLOUDY=6 OR 7 AND OVERCAST=8
#HAZE AND FOG ARE VISIBILITY ISSUES CAN BE CONVERTED TO OKTAS AS WELL, FOG=3,HAZE=6,LIGHT RAIN=, HEAVY RAIN=8
#THIS FILE CONVERTS WEATHER DATA INTO DAILY AVERAGE CLOUDINESS AND SAVES IT IN A FILE WHICH CAN NOW BE ACCESSED BY DATE FOR DATA CLASSIFICATION BY CLOUDINESS
#getcloudiness.close()
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
import math

#initiate a list of cloudiness from the column of cloudiness
#x1=[[] for i in range(int(max(sunmornarray))+abs(int(min(sunmornarray))))]
cloudinesstypes=[]
n=[]
k=[]
getcloudiness=open("C:\Users\chandrayee\Documents\NASA\ParsedData\\berkeleyweather\\cloudinessraw_2013 03 03_2013 03 18.txt")
get=open("C:\Users\chandrayee\Documents\NASA\ParsedData\\berkeleyweather\\cloudiness_0303_0318.txt",'a')
clouds=getcloudiness.readlines()
day=[]
mon=[]
data=[]
yr=[]
#cloudiness=['Clear','Partly Cloudy','Scattered Clouds','Light Rain','Mostly Cloudy','Rain','Overcast','Heavy Rain','Fog','Haze']
cloudiness=['Clear','Partly','Scattered','Light','Mostly','Rain','Overcast','Heavy','Fog','Haze']
values=[0,2,4,4,7,7,8,8,4,4]
for j in range(len(clouds)):
    cloud=str.split(clouds[j],'\t')
    getdata=str.split(cloud[5],'\n')
    yr.append(cloud[1])
    mon.append(cloud[2])
    day.append(cloud[3])
    data.append(getdata[0])
first=[]
total=[]
m=0
print "Following are the average daily cloudiness values"
for j in range(len(clouds)-1):
    if mon[j]==mon[j+1] and day[j]==day[j+1]:
        for i in range(len(cloudiness)):
            x='dict'+str(i)
            vars()[x]={cloudiness[i]:values[i]}
            if data[j]==cloudiness[i]:
                total.append(values[i])
                m+=1
                #print str(day[j])+' '+'ooo'+' '+str(values[i])
    else:
        first.append(str(np.mean(total)))
        print round(np.mean(total),2)
        if np.mean(total)>3.5:
            k="cloudy"
        else:
            k="sunny"
        eachline=day[j]+'\t'+mon[j]+'\t'+yr[j]+'\t'+str(round(np.mean(total),2))+'\t'+k+'\t'+'\n'
        get.write(eachline)
        total=[]
        m=0
getcloudiness.close()
get.close()

        
        
        
        



    
    
    
    
    
    
    


