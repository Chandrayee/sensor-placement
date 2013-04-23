"""Code for extracting data from wunderground API and adding the data to the
cloud table of data.db.

The cloud table has the following 6 attributes (column names and types):

timezone string, year int, month int, day int, time string, cloudiness string
"""

import urllib2
import datetime
from datetime import datetime
import numpy as np
import sqlite3


def isLeapYear( year):
      if (year % 400 == 0) :
          return True
      if (year % 100 == 0) :
          return False
      if (year % 4 == 0):
          return True
      else:
          return False              
  

def daysInMonth(month,year):
      if (month == 2):
          if (isLeapYear(year)):
              return 29;
          else:
              return 28
      elif (month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12):
          return 31
      else :
          return 30
 
def dayInYear(month, day, year):
    current = 1
    numberOfDays = day
    while (current < month):
        numberOfDays = numberOfDays + daysInMonth(current, year)
        current = current + 1
    return numberOfDays

def difference(month1, day1, year1, month2, day2, year2):
    daycounter = 0;  
    if (year1 == year2):
        return (dayInYear(month1, day1, year1) - dayInYear(month2, day2,year2))
    elif (isLeapYear(year2)):
        daycounter = daycounter + (366 - dayInYear(month2, day2, year2))
    else:
        daycounter = daycounter + (365 - dayInYear(month2, day2, year2))
    daycounter = daycounter + dayInYear(month1, day1, year1)
    current = year2 + 1
    while (current < year1):
        if (isLeapYear(current)):
            daycounter = daycounter + 366
            current = current + 1
        else:
            daycounter = daycounter + 365
            current = current + 1
    return daycounter


def arrayofdaysmonthsyears(month1,day1,year1,month2,day2,year2):
    if daysInMonth(month2, year2) == day2:
          daysleftinmonth2 = daysInMonth(month2, year2) - day2 + 1
    else:
          daysleftinmonth2= daysInMonth(month2, year2) - day2 + 2 #to include start and end
    if year1 == year2:
            if month1 == month2:
                monthsinbetween = 0
            else:
              monthsinbetween= month1 - month2 - 1
    else:
        monthsleftinyear2 = 12 - month2 - 1
        monthsinbetween = monthsleftinyear2 + (12 *(year1 - (year2+1))) + month1
    dayarray = []
    montharray = []
    yeararray= []
    if month2 == month1:
      currentdays = day1 - day2 + 1
    else:
      currentdays = daysleftinmonth2
    currentday = day2
    currentmonth = month2
    currentyear = year2
    while currentdays > 0:
        dayarray.append(currentday)
        montharray.append(currentmonth)
        yeararray.append(currentyear)
        currentdays = currentdays - 1
        currentday = currentday + 1
    fullmonths = monthsinbetween
    currentmonth = month2 + 1
    while fullmonths > 0:
        if currentmonth > 12:
              currentmonth = 1
              currentyear = currentyear + 1
        daystoadd = daysInMonth(currentmonth, currentyear)
        currentdaytoadd = 1
        while daystoadd > 0:
            dayarray.append(currentdaytoadd)
            montharray.append(currentmonth)
            yeararray.append(currentyear)
            currentdaytoadd = currentdaytoadd + 1
            daystoadd = daystoadd - 1
        currentmonth = currentmonth + 1
        fullmonths = fullmonths - 1
    daysinday1 = day1
    finaldaytoadd = 1
    if month2 != month1 or year1 != year2:
          while daysinday1 > 0:
              dayarray.append(finaldaytoadd)
              montharray.append(month1)
              yeararray.append(year1)
              finaldaytoadd = finaldaytoadd + 1
              daysinday1 = daysinday1 - 1
    return [dayarray, montharray, yeararray]

def arrayofdays(month1,day1,year1,month2,day2,year2):
      return (arrayofdaysmonthsyears(month1,day1,year1,month2,day2,year2))[0]

def arrayofmonths(month1,day1,year1,month2,day2,year2):
      return (arrayofdaysmonthsyears(month1,day1,year1,month2,day2,year2))[1]

def arrayofyears(month1,day1,year1,month2,day2,year2):
      return (arrayofdaysmonthsyears(month1,day1,year1,month2,day2,year2))[2]

def createData(end, start = "2012 11 01", feature = "history", station = "KOAK"):
    """Adds all the wunderground data to the cloud data starting from start
    date START until end date END. You can specify the feature FEATURE to pull
    either historical data or hourly data. You also must specify the weather
    station STATION. Default values are above."""
    #Connect to the database data.db
    """connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    cursor.execute('DROP TABLE cloud')
    cursor.execute('''CREATE TABLE cloud (timezone string, year int, month int,
                day int, hour int, minute int, seconds int,
                cloudiness string, PRIMARY KEY (year, month, day, hour,
                minute, seconds))''')"""

    start_split = start.split()
    end_split = end.split()
    startyear = int(start_split[0])
    endyear = int(end_split[0])
    startmonth = int(start_split[1])
    endmonth = int(end_split[1])
    startday = int(start_split[2])
    endday = int(end_split[2])

    DD = arrayofdays(endmonth,endday,endyear,startmonth,startday,startyear)
    MM = arrayofmonths(endmonth,endday,endyear,startmonth,startday,startyear)
    YYYY = arrayofyears(endmonth,endday,endyear,startmonth,startday,startyear)

    cloudDict = {"Clear":"", "Partly":" Cloudy", "Mostly":" Cloudy", "Scattered":" Clouds",
                 "Small":" Hail", "Funnel":" Cloud", "Patches":" of Fog", "Shallow":" Fog",
                 "Partial":" Fog", "Overcast":"", "Squalls":"","Unknown":"","Haze":"",
                 "Drizzle":"", "Rain":"", "Snow":"", "Ice":"", "Hail":"", "Mist":"",
                 "Fog":"", "Smoke":"", "Volcanic":" Ash", "Widespread":" Dust", "Sand":"",
                 "Spray":"", "Dust":" Whirls", "Sandstorm":"", "Low":" Drifting Snow/Dust/Sand",
                 "Blowing":" Snow/Dust/Sand", "Thunderstorms":"", "Freezing":" Drizzle/Rain/Fog"}
    
    for i in range(len(DD)):
        day = str(DD[i])
        if (DD[i] < 10):
            day = "0" + str(DD[i])
        YYYYMMDD=str(YYYY[i])+str(MM[i])+day
        features=feature+"_"+YYYYMMDD
        url="http://api.wunderground.com/api/f2983417df06de3a/"+features+"/q/"+station+".json"
        print(url)
        data=urllib2.urlopen(url).read()
        getdata=data.split(",")
        for count in range(len(getdata)):
            if '"tzname":' in getdata[count]:
                if '"tzname": "UTC"' not in getdata[count]:
                    minute = getdata[count-1].split(":")
                    y2 = minute[1].strip().replace("\"","")
                    if (y2 == "53"):
                        timezone = getdata[count].split(":")
                        x = timezone[1].replace("\"","").replace("}","").strip()
                        hour = getdata[count-2].split(":")
                        y1 = hour[1].strip().replace("\"","")
                        clouds = getdata[count+30].split(":")
                        cloudiness = clouds[1].replace("\"","")
                        to_db = [x, YYYY[i], MM[i], DD[i], int(y1), int(y2), 0, cloudiness]
                        print(to_db)
                        """cursor.execute('INSERT OR IGNORE INTO cloud VALUES (?,?,?,?,?,?,?,?)',
                               to_db)"""
    #Save your changes
    #connection.commit()

#def updateData():
"""for count in range(len(getdata)):
    if '"tzname":' in getdata[count]:
        if '"tzname": "UTC"' not in getdata[count]:
            minute = getdata[count-1].split(":")
            y2 = minute[1].strip().replace("\"","")
            if (y2 == "53"):
                print(count)
                break"""
#164

                
