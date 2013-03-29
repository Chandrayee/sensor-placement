class py2java:
    def __init__(self, read):
        self.r=read
        #self.ti=timstm
import numpy as np
import scipy as sp
import urllib2
import datetime
from datetime import datetime,date
import time
from time import mktime, localtime, gmtime, strftime

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


#Add data from readings and timestamp into light table
for count in range(len(reading)):
    time = timestamp[count]
    to_db = [time[0], time[1], time[2], time[3], time[4], time[5],
             time[6], reading[count]]
    cursor.execute('INSERT INTO ' + table + ' VALUES (?,?,?,?,?,?,?,?)',
                   to_db)


#Save your changes
connection.commit()











