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

#month1, day1, year1 - enddate
#month2, day2,year2 - startdate

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
      return (arraryofdaysmonthsyears(month1,day1,year1,month2,day2,year2))[2]

print "This program draws cloudiness data from wunderground site based on the start date, end date and weather station input by the user"
print "  "
startdate=raw_input("Enter the starting year, month and day of the data in YYYY MM DD: " )
enddate=raw_input("Enter the ending year, month and day of the data in YYYY MM DD: " )

start_date_split = startdate.split()
end_date_split = enddate.split()
startyear = int(start_date_split[0])
endyear = int(end_date_split[0])
startmonth = int(start_date_split[1])
endmonth = int(end_date_split[1])
startday = int(start_date_split[2])
endday = int(end_date_split[2])

DD = arrayofdays(endmonth,endday,endyear,startmonth,startday,startyear)
MM = arrayofmonths(endmonth,endday,endyear,startmonth,startday,startyear)
YYYY = arrayofyears(endmonth,endday,endyear,startmonth,startday,startyear)
    
featureinput=raw_input("Enter if you want historical data or hourly data as history: ")
query=raw_input("Enter the city or the weather station name: ")

#Connect to the database data.db
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

"""
for i in range(len(DD)):
    YYYYMMDD=YYYY[i]+MM[i]+DD[i]
    features=featureinput+"_"+str(YYYYMMDD)
    url="http://api.wunderground.com/api/46c535271ddf6901/"+features+"/q/"+query+".json"
    #features: history
    #weather station name: KOAK
    data=urllib2.urlopen(url).read()
    getdata=str.split(data)
    timezone=[]
    date=[]
    time=[]
    condis=[]
    total=[]
    for count in range(len(getdata)-35):
        if getdata[count]=='"tzname":':
            if getdata[count+1]!='"UTC"':
                x1=str.split(getdata[count+1],'"')
                x=x1[1]
                y1=str.split(getdata[count-3],'"')
                y2=str.split(getdata[count-1],'"')
                y=y1[1]+":"+y2[1]+":00"
                #print y2
                z1=str.split(getdata[count-9],'"')
                z2=str.split(getdata[count-7],'"')
                z3=str.split(getdata[count-5],'"')
                z=z1[1]+"/"+z2[1]+"/"+z3[1]
                timezone.append(x)
                time.append(y)
                date.append(z)
                condition=str.split(getdata[count+35],',')
                if len(condition)>1:
                    clouds=str.split(condition[1],":")
                    #print clouds[1]
                    cloudiness=str.split(clouds[1],'"')
                    condis.append(cloudiness[1])
                    to_db = [x, YYYY[i], MM[i], DD[i], y, cloudiness[1]]
                    cursor.execute('INSERT INTO light VALUES (?,?,?,?,?,?)',
                       to_db)
                    save=x+'\t'+str(YYYY[i])+'\t'+str(MM[i])+'\t'+str(DD[i])+'\t'+y+'\t'+cloudiness[1]+'\n'
                    print(save)
                    total.append(x+' '+y+' '+z+' '+cloudiness[1])
"""

#Save your changes
connection.commit()
