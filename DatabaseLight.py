"""Code for extracting data from smap url's and adding the data to the
light tables of data.db. In addition to adding the raw data from the smap
url's, we also create sunposition data (altitude and azimuth) and add the
values as the 10th and 11th attributes of a light table.

The light tables (light1, light2, light3, etc.) have the following 11
attributes (column names and types):

unixtime float, weekday string, day int, month int, year int, hour int,
    minute int, seconds int,light float, altitude float, azimuth float
"""

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

#Dictionary that maps each BEST lab sensor number to its sensor ID.
sensors_dict = {2:"f862a13d-91ee-5696-b2b1-b97d81a47b5b",
                3:"b92ddaee-48de-5f37-82ed-fe1f0922b0e5",
                4:"8bb0b6a2-971f-54dc-9e19-14424b9a1764"}

def make_unix_timestamp(date_string, time_string):
    """Returns the unix time stamp of a given date, date_string (format
    YYYY,MM,DD), and a given time, time_string (format HH,MM,SS)."""
    date_string_split = date_string.split(",")
    current_date = date(int(date_string_split[0]),
                        int(date_string_split[1]),
                        int(date_string_split[2]))
    current_unix = mktime(current_date.timetuple())
    time_string_split = time_string.split(",")
    current_time = 1000*(3600*int(time_string_split[0]) +
                    60*int(time_string_split[1]) +
                    int(time_string_split[2]))
    return str(int(current_unix + current_time))

def parse(url):
    """Returns a list of the timestamps, readings, and unixtimes of each
    entry from the raw data provided by the input url."""
    timestamp=[]
    reading=[]
    timest=[]
    temp=[]
    unixtime=[]
    webpage = urllib2.urlopen(url).read()
    page = str.split(webpage, '[')
    for count in range(len(page)):
        z1=str.split(page[count],',')
        temp.append(z1)
        count+=1
    print temp[1]
    getvar = temp[3:]
    for count in range(len(getvar)):
        t=float(getvar[count][0])/1000
        unixtime.append(getvar[count][0])
        ttb=time.localtime(t)
        #Returns time in string format: "Wed 21 11 2012 16 45 53"
        tim=strftime("%a %d %m %Y %H %M %S",ttb)
        #For debugging:
        if (count == 0):
            print(tim)
        timestamp.append(tim.split())
        read=str.split((getvar[count][1]),']')
        reading.append(float(read[0]))
        #For debugging:
        if (count == 0):
            print(float(read[0])) #37.851485925
        count+=1
    return [timestamp, reading, unixtime]

def getSunpos(lat, lon, timezon, year, month, day, hour, minute, seconds):
    """Returns a list containing the altitude and the azimuth given the
    latitude LAT, longitude LON, timezone TIMEZON, year YEAR, month MONTH,
    minute MINUTE, and seconds SECONDS."""
    splat = str.split(lat)
    splon = str.split(lon)
    latitude = float(splat[0]) + float(splat[1])/60 + float(splat[2])/3600
    if splon[3] == 'W':
        longitude = -(float(splon[0]) + float(splon[1])/60 +
                      float(splon[2])/3600)
    else:
        longitude = float(splon[0]) + float(splon[1])/60 +\
        float(splon[2])/3600
    local = pytz.timezone(timezon)
    loctime = str(year) + '-' + str(month) + '-' + str(day) + ' ' +\
                str(hour) + ':' + str(minute) + ':' + str(seconds)
    naive = datetime.strptime(loctime, "%Y-%m-%d %H:%M:%S")
    local_dt = local.localize(naive, is_dst=None)
    utc_dt = local_dt.astimezone(pytz.utc)
    utc_dt.strftime("%Y-%m-%d %H:%M:%S")
    utcsplit = str.split(str(utc_dt))
    utcdt = str.split(utcsplit[0],'-')
    utctime = str.split(utcsplit[1],'+')
    utctimefinal = str.split(utctime[0],':')
    year = utcdt[0]
    month = utcdt[1]
    day = utcdt[2]
    hour = utctimefinal[0]
    minute = utctimefinal[1]
    second = utctimefinal[2]
    #+1 for e and -1 for w for dst
    houronly = float(hour) + float(minute)/60 + float(second)/3600
    delta = int(year)-1949
    leap = int(delta/4)
    doy = [31,28,31,30,31,30,31,31,30,31,30,31]
    if int(year)%4 == 0:
        doy[1] = 29
    dayofyear = sum(doy[0:(int(month)-1)]) + int(day)
    jd = 2432916.5 + delta*365 + dayofyear + leap + houronly/24
    actime = jd - 2451545
    pi = 3.1415926535897931
    rad = pi/180
    
    #mean longitude in degrees between 0 and 360
    L = (280.46 + 0.9856474*actime)%360
    if L < 0:
        L+=360
    #mean anomaly in radians
    g = (357.528 + 0.9856003*actime) % 360
    if g < 0:
        g+=360
    g = g*rad
    #ecliptic longitude in radians
    eclong = (L + 1.915*math.sin(g) + 0.02*math.sin(2*g)) % 360
    if eclong < 0:
        eclong+=360
    eclong = eclong*rad
    #ecliptic obliquity in radians
    ep = (23.439 - 0.0000004*actime)*rad
    #get right ascension in radians between 0 and 2 pi
    num = math.cos(ep)*math.sin(eclong)
    den = math.cos(eclong)
    ra = math.atan(num/den)
    if den < 0:
        ra+=pi
    elif den > 0 and num < 0:
        ra+=2*pi
    #get declination in radians
    dec = math.asin(math.sin(ep)*math.sin(eclong))
    #get greenwich mean sidereal time
    gmst = (6.697375 + 0.0657098242*actime + houronly) % 24
    if gmst < 0:
        gmst+=24
    #get local mean sidereal time in radians
    lmst=(gmst + longitude/15) % 24
    if lmst < 0:
        lmst+=24
    lmst = lmst*15*rad
    #get hour angle in radians between -pi and pi
    ha = lmst - ra
    if ha < -pi:
        ha+=2*pi
    elif ha > pi:
        ha = ha - 2*pi
    #change latitude to radians
    latrad = latitude*rad
    #calculate elevation and azimuth in degrees
    el=math.asin(math.sin(dec)*math.sin(latrad) +
                 math.cos(dec)*math.cos(latrad)*math.cos(ha))
    az=math.asin(-math.cos(dec)*math.sin(ha)/math.cos(el*rad))
    #approximation for azimuth
    #if az==90, elcrit=math.degrees(math.asin(math.sin(dec)/math.sin(latitude)))
    if math.sin(dec) - math.sin(el)/math.sin(latrad) >= 0 and\
        math.sin(az) < 0:
        az+=2*pi
    elif math.sin(dec) - math.sin(el)/math.sin(latrad) < 0:
        az = pi-az
    eldeg = round(math.degrees(el),2)
    azdeg = round(math.degrees(az),2)
    if eldeg > -0.56:
        refrac = 3.51561*(0.1594 + 0.0196*eldeg + 0.00002*math.pow(eldeg,2))\
                    /(1 + 0.505*eldeg + 0.0845*math.pow(eldeg,2))
    else:
        refrac = 0.56
    eldeg=eldeg+refrac
    #print eldeg,azdeg
    #data is saved for future reference
    return [str(eldeg), str(azdeg)]

def createLightData(sens_no, start, end, lat = "37 52 27.447",
               lon = "122 15 33.3864 W", timezon = "US/Pacific"):
    """This function adds data for BEST lab sensor SENS_NO into its
    respective light table starting from unix timestamp (in milliseconds)
    START and ending at unix timestamp (in milliseconds) END. It generates
    sunposition data using the given LAT, LON, and TIMEZON. If these are
    not specified, createData resorts to the default LAT, LON, and TIMEZON
    values, which are the values for the BEST Lab in Berkeley, CA. LAT
    format is "degrees minutes seconds" (north is positive). LON format is
    "degrees minutes seconds W|E" (W for west and E for east). TIMEZON
    choices can be looked up. Must be compatible with python utc timezones.
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    sensorID = sensors_dict[sens_no]
    table = "light" + str(sens_no)
    url = "http://new.openbms.org/backend/api/prev/uuid/" + sensorID +\
          "?&start=" + start + "&end=" + end + "&limit=100000&"
    timestamp, reading, unixtime = parse(url)
    for count in range(len(reading)):
        time = timestamp[count]
        sunpos = getSunpos(lat, lon, timezon, time[3], time[2],
                           time[1], time[4], time[5], time[6])
        cloud = cursor.execute('SELECT cloudiness FROM cloud WHERE day = ' +
                               str(time[1]) + ' AND month = ' + str(time[2]) +
                               ' AND year = ' + str(time[3]) + ' AND hour = ' +
                               str(time[4]))
        cloudiness = cloud.fetchone()
        if cloudiness is not None:
            to_db = [unixtime[count], time[0], time[1], time[2], time[3],
                     time[4], time[5],time[6], reading[count], sunpos[0],
                     sunpos[1], str(cloudiness[0])]
        else:
            to_db = [unixtime[count], time[0], time[1], time[2], time[3],
                     time[4], time[5],time[6], reading[count], sunpos[0],
                     sunpos[1], "Null"]
        cursor.execute('INSERT OR IGNORE INTO ' + table +
                        ' VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                        to_db)
            
            
    connection.commit()

def createAllLightData(lat = "37 52 27.447", lon = "122 15 33.3864 W",
               timezon = "US/Pacific"):
    """Adds all the data starting from the beginning of data collection
    until the current time for BEST lab sensors 2, 3, and 4."""
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    createLightData(2, "1349478489000", str(int(time.time())*1000), lat, lon,
               timezon)
    createLightData(3, "1353545153000", str(int(time.time())*1000), lat, lon,
               timezon)
    createLightData(4, "1353545237000", str(int(time.time())*1000), lat, lon,
               timezon)
    #Save your changes
    connection.commit()

def updateAllData():
    """Updates all the data in BEST lab sensors 2, 3, and 4 by calling
    updateData on each sensor."""
    updateData(2)
    updateData(3)
    updateData(4)

def updateData(sens_no, lat = "37 52 27.447", lon = "122 15 33.3864 W",
               timezon = "US/Pacific"):
    """Updates all the data starting from the time of the latest entry of
    each time table until the current time for BEST lab sensor number
    SENS_NO. It generates sunposition data using the given LAT, LON, and
    TIMEZON. If these are not specified, createData resorts to the default
    LAT, LON, and TIMEZON values, which are the values for the BEST Lab
    in Berkeley, CA. LAT format is "degrees minutes seconds" (north is
    positive). LON format is "degrees minutes seconds W|E" (W for west and
    E for east). TIMEZON choices can be looked up. Must be compatible with
    python utc timezones.
    """
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    sensorID = sensors_dict[sens_no]
    table = "light" + str(sens_no)
    cursor.execute('SELECT MAX(unixtime) FROM ' + table)
    start = int(cursor.fetchone()[0])
    end = int(time.time())*1000
    limit = (end - start)/300000
    print("limit is:" + str(limit))
    print("Start is:" + str(start))
    print("End is:" + str(end))
    url = "http://new.openbms.org/backend/api/prev/uuid/" + sensorID +\
          "?&start=" + str(start) + "&end=" + str(end) + "&limit=" +\
          str(limit) + "&"
    timestamp, reading, unixtime = parse(url)
    print(len(reading))
    for count in range(len(reading)):
        t = timestamp[count]
        sunpos = getSunpos(lat, lon, timezon, t[3], t[2], t[1], t[4],
                           t[5], t[6])
        to_db = [unixtime[count], t[0], t[1], t[2], t[3], t[4], t[5],
                 t[6], reading[count], sunpos[0], sunpos[1]]
        cursor.execute('INSERT OR IGNORE into ' + table +
                       ' VALUES (?,?,?,?,?,?,?,?,?,?,?)',
                       to_db)
    #Save your changes
    connection.commit()
