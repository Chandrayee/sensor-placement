import numpy as np
import scipy as sp
from scipy import stats
import time
from time import mktime, localtime, gmtime, strftime
import pdb


#get data

getdata1=open("C:\Users\chandrayee\Desktop\get\sdh_steam.txt")
getdata2=open("C:\Users\chandrayee\Desktop\get\sdh_oat.txt")

linelists=getdata1.readlines()
linelisto=getdata2.readlines()
count=0
datas=[]
datao=[]
time1=[]
date=[]
a=range(len(linelists))
#print len(linelists)
print 'starting'
p=0
m=0

for count in a:
    datums=linelists[count]
    datumo=linelisto[count]
    x=str.split(datums,'\t')
    y=str.split(datumo,'\t')
    if float(x[1])>0:
        k=0
        t=float(x[0])/1000
        s=float(x[1])
        o=float(y[1])
        time1.append(t)
        datas.append(s)
        datao.append(o)
    else:
        k=1
        #del x[0]
        #del x[1]
    p=p+k
    count +=1
print p

corrtime=open("C:/Users/chandrayee/Desktop/get/timecorr.txt",'a')
for count in range(len(time1)-1):
    diff=time1[count+1]-time1[count]
    if diff>7:
        n=1
        corr1=time.localtime(float(time1[count]))
        corr2=strftime("%a, %d %b %Y %H:%M:%S",corr1)
        corr3=time.localtime(float(time1[count+1]))
        corr4=strftime("%a, %d %b %Y %H:%M:%S",corr3)
        corr=corr2+'\t'+corr4+'\n'
        corrtime.write(corr)
    else:
        n=0
    m=m+n
    count +=1
print m
corrtime.close()

print len(linelists), len(time1), len(datas), len(datao)

utime=sp.array(time1)
zs=sp.array(datas)
zo=sp.array(datao)

##ttb=time.localtime(utime[0])
##tte=time.localtime(utime[1])
##print utime[0], utime[1]
##print strftime("%a, %d %b %Y %H:%M:%S",ttb), strftime("%a, %d %b %Y %H:%M:%S",tte)
pdb.set_trace()
#print max(z), min(z), np.mean(z)

##get time at 15 min
#newtime=[]
#start_time=utime[0]
#end_time=utime[-1]
#timeinterval=900
#time15=start_time+timeinterval
#while time15<end_time-timeinterval:
    #time15=time15+timeinterval
    #newtime.append(time15)

#print newtime[0],newtime[-1]


##set data at 15 min interval
b=179
interval=180
x=0
steamdata=[]
oatdata=[]
puttime=[]

trials=open("C:\Users\chandrayee\Desktop\get\steam.txt",'a')
trialo=open("C:\Users\chandrayee\Desktop\get\oat.txt",'a')
inter=len(datas)-interval
print inter
while x<=inter:
    #print ' '
    #print x
    tots=zs[x]
    toto=zo[x]
    #print tot
    for count in range(b):
        #print x+count+1
        tots=tots+zs[x+count+1]
        toto=toto+zo[x+count+1]
        #print tot
        times=utime[x+interval]
        count +=1
    avgs=str(tots/interval)
    avgo=str(toto/interval)
    #print ' '
    #print avg
    lines=avgs+'\n'
    lineo=avgo+'\n'
    trials.write(lines)
    trialo.write(lineo)
    steamdata.append(avgs)
    oatdata.append(avgo)
    puttime.append(times)
    x=x+interval
print len(steamdata), len(oatdata)
trials.close()
trialo.close()

pdb.set_trace()
#this is the code for a moving average that will lead to more smoothing than desired
##for x in range(inter):
##    print ' '
##    print x
##    tot=z[x]
##    print tot
##    for count in range(b):
##        print x+count+1
##        tot=tot+z[x+count+1]
##        print tot
##        times=utime[x+interval]
##        count +=1
##    else:
##        avg=str(tot/90)
##        print ' '
##        print avg
##        line=avg+'\n'
##        trial.write(line)
##        mindata.append(avg)
##        puttime.append(times)
##    x=x+interval
##print len(mindata), max(mindata)
##trial.close()


datac=sp.array(mindata)

#print max(datac), min(datac)

print len(puttime)

savedata=open("C:\Users\chandrayee\Desktop\savdatoat.txt",'a')

print 'ready to save'

timestr=[]
steamstr=[]

for count in range(len(mindata)):
    #t1=int(newtime[count])
    t1=int(puttime[count])
    t2=time.localtime(t1)
    t3=strftime("%a, %d %b %Y %H:%M:%S",t2)
    dat=puttime[count]
    steam1=mindata[count]
    line=t3+'\t'+str(dat)+'\t'+steam1+'\n'
    savedata.write(line)
    timestr.append(t3)
    steamstr.append(steam1)
    count +=1
else:
    savedata.close()
    
ste=sp.array(steamstr)

print max(ste), min(ste)
print 'done'
