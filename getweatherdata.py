import urllib2
import datetime
from datetime import datetime
import numpy as np

print "This program draws cloudiness data from wunderground site based on the start date, end date and weather station input by the user"
print "  "
startdate=raw_input("Enter the starting year, month and day of the data in YYYY MM DD: " )
enddate=raw_input("Enter the ending year, month and day of the data in YYYY MM DD: " )
dayofmonth=[31,28,31,30,31,30,31,30,31,31,30,31,30,31]
getstart=str.split(startdate)
getend=str.split(enddate)
if int(getstart[0])!=int(getend[0]):
    monthsleft=12-int(getstart[1])
    monthsmore=int(getend[1])
    totalmonths=monthsleft+monthsmore
else:
    totalmonths=int(getend[1])-int(getstart[1])

#print getend[1], getend[2]
#print getstart[1], getstart[2]
daysleft=int(dayofmonth[int(getstart[1])-1])-int(getstart[2])
daysfinish=int(getend[2])
daysbetween=dayofmonth[(int(getstart[1])):(int(getend[1])-1)]
totaldays=[daysleft]+daysbetween+[daysfinish]
#print totaldays
days=sum(totaldays)
a=int(getstart[2])
b=int(getstart[2])+daysleft+1
c=int(getend[2])+1
startpart=np.arange(a,b)
endpart1=np.arange(1,c)
array=[]
array1=[]
endpart=[]
for count in range(len(daysbetween)):
    array1=np.arange(1,daysbetween[count]+1)
DD=[]
MM=[]
for count in range(len(array1)):
    if len(str(array1[count]))==1:
        ar='0'+str(array1[count])
    else:
        ar=str(array1[count])
    array.append(ar)
for count in range(len(endpart1)):
    if len(str(endpart1[count]))==1:
        end='0'+str(endpart1[count])
    else:
        end=str(endpart1[count])
    endpart.append(end)
DD1=list(startpart)+list(array)+list(endpart)
month1=[getstart[1]]*len(startpart)
month22=[int(getstart[1])+1]*len(array)
month2=[]
for count in range(len(month22)):
    month='0'+str(month22[count])
    month2.append(month)
month3=[getend[1]]*len(endpart)
MM1=list(month1)+list(month2)+list(month3)
for count in range(len(DD1)):
    day=str(DD1[count])
    mon=str(MM1[count])
    DD.append(day)
    MM.append(mon)
YYYY=[getstart[0]]*len(DD)
print "  "
print DD
print MM
print YYYY
print "The length of the day, month and year arrays are ", len(DD), len(MM),len(YYYY)
direc="C:\Users\chandrayee\Documents\NASA\ParsedData\\berkeleyweather\cloudinessraw"+"_"+startdate+'_'+enddate+".txt"
saveweather=open(direc,'a')
featureinput=raw_input("Enter if you want historical data or hourly data as history: ")
query=raw_input("Enter the city or the weather station name: ")
for i in range(len(DD)):
    YYYYMMDD=YYYY[i]+MM[i]+DD[i]
    features=featureinput+"_"+YYYYMMDD
    url="http://api.wunderground.com/api/46c535271ddf6901/"+features+"/q/"+query+".json"
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
                   save=x+'\t'+YYYY[i]+'\t'+MM[i]+'\t'+DD[i]+'\t'+y+'\t'+cloudiness[1]+'\n'
                   total.append(x+' '+y+' '+z+' '+cloudiness[1])
                   saveweather.write(save)
    #print "   "
    #print "  "
    #print total
saveweather.close()
               
    
           
        



