import numpy as np
from numpy import vstack
import scipy as sp
from scipy import stats
import urllib2
import datetime
from datetime import datetime,date
import time
from time import mktime, localtime, gmtime, strftime
import statsmodels as sm
import matplotlib as mpl
from matplotlib import pyplot as plt
import pytz
from pytz import timezone
import math
import pdb


import sqlite3
from sqlite3 import dbapi2 as sqlite3

#Data Extraction from TEMPERATURE DATA BEST lab
sens_no=input("Enter the sensor number: ")
sensors_dict = {2:"f862a13d-91ee-5696-b2b1-b97d81a47b5b",
                3:"b92ddaee-48de-5f37-82ed-fe1f0922b0e5",
                4:"8bb0b6a2-971f-54dc-9e19-14424b9a1764"}

sensorID = sensors_dict[sens_no]

table = "light" + str(sens_no)
#start_date=raw_input("Enter the start time in this format YYYY,MM,DD: ")
#end_date=raw_input("Enter the end time in this format YYYY,MM,DD: ")
#start_time = raw_input("Enter the start hour, minutes, seconds in this format HH,MM,SS: ")
#end_time = raw_input ("Enter the end hour, minutes, seconds in this format HH,MM,SS: ")


def make_unix_timestamp(date_string, time_string):
    date_string_split = date_string.split(",")
    current_date = date(int(date_string_split[0]), int(date_string_split[1]),int(date_string_split[2]))
    current_unix = mktime(current_date.timetuple())
    time_string_split = time_string.split(",")
    current_time = 1000*(3600*int(time_string_split[0]) + 60*int(time_string_split[1]) +
                    int(time_string_split[2]))
    return str(int(current_unix + current_time))


#start = make_unix_timestamp(start_date, start_time)
#end = make_unix_timestamp(end_date, end_time)
start = make_unix_timestamp("2012,07,27", "12,15,56")
end = make_unix_timestamp("2012,08,12", "10,00,26")

url = "http://new.openbms.org/backend/api/prev/uuid/" + sensorID + "?&start=" + start + "&end=" + end +"&limit=100000&"

timestamp=[]
reading=[]

timest=[]
temp=[]


def parse(url):
    webpage = urllib2.urlopen(url).read()
    page = str.split(webpage, '[')
    for count in range(len(page)):
        z1=str.split(page[count],',')
        temp.append(z1)
        count+=1
    print temp[1]
    getvar = temp[3:]
    for count in range(len(getvar)):
        t=float(getvar[count][0])/1000 #time in seconds
        ttb=time.localtime(t)
        tim=strftime("%a %d %m %Y %H %M %S",ttb) #returns time in string
        #%a = weekday, %d = day of month, %m = month, %Y = year, %H = hour, %M = minute, %S = seconds
        if (count == 0):
            print(tim) #Wed 21 11 2012 16 45 53
        timestamp.append(tim.split())
        read=str.split((getvar[count][1]),']')
        reading.append(float(read[0])) #appends the light measurement
        if (count == 0):
            print(float(read[0])) #37.851485925
        count+=1

parse(url)

# For debugging purposes:
def debug(length):
    print("Length of readings: " + str(len(reading)))
    print("Length of readings: " + str(len(timestamp)))
    for count in range(length):
        print("(" + str(reading[count]) + ",")
        print(timestamp[count])
        print(")")


#Create a database data.db and connect to it
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

#lat=raw_input("enter the latitude of the place (enter in degrees, minutes and seconds, north is positive):   ")
#lon=raw_input("enter the longitude of the place (put W for west and E for east at the end of the longitude):   ")
#timezon=raw_input("enter the name of the place as within quotes as country/city with spaces replaced by underscore:   ")

lat = "37 52 27.447"
lon = "122 15 33.3864 W"
timezon = "US/Pacific"

def getSunpos(lat, lon, year, month, day, hour, minute, seconds):
    splat=str.split(lat)
    splon=str.split(lon)
    latitude=float(splat[0])+float(splat[1])/60+float(splat[2])/3600
    if splon[3]=='W': # ASK ABOUT THIS
        longitude=-(float(splon[0])+float(splon[1])/60+float(splon[2])/3600)
    else:
        longitude=float(splon[0])+float(splon[1])/60+float(splon[2])/3600
    local = pytz.timezone(timezon)
    loctime = str(year) + '-' + str(month) + '-' + str(day) + ' ' + str(hour) + ':' + str(minute) + ':' + str(seconds)
    naive = datetime.strptime (loctime, "%Y-%m-%d %H:%M:%S")
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
    return [str(eldeg), str(azdeg)]
    #newline=datentime[0]+'\t'+datentime[1]+'\t'+datentime[2]+'\t'+datentime[3]+'\t'+datentime[4]+'\t'+datentime[5]+'\t'+str(eldeg)+'\t'+str(azdeg)+'\n'

#Add data from readings and timestamp into light table
for count in range(len(reading)):
    time = timestamp[count]
    sunpos = getSunpos(lat, lon, time[3], time[2], time[1], time[4], time[5], time[6])
    to_db = [time[0], time[1], time[2], time[3], time[4], time[5],
             time[6], reading[count], sunpos[0], sunpos[1]]
    cursor.execute('INSERT OR IGNORE INTO ' + table + ' VALUES (?,?,?,?,?,?,?,?,?,?)',
                   to_db)

#Save your changes
connection.commit()











