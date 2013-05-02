#THIS PROGRAM COMPUTES THE CORRELATION BETWEEN LIGHT LEVEL AND SUN ANGLE FOR 8 LEVELS OF CLOUDINESS AND TIME OF DAY (MORNING AND AFTERNOON)
#STEP#1:CLASSIFY DATA (BOTH SUN ANGLE AND LIGHT LEVEL) BY TIME OF DAY AND 8 CLOUDINESS LEVELS IN SEPARATE BINS
#STEP#2:PERFORM REGRESSION FOR EACH OF THE SIXTEEN BINS THUS CREATED


print "This program computes correlation between sun position and received light from a dataset labelled by cloudiness and time of day, it does not scale for multiple windows"
print "It first checks the number of one degree sun angle interval in database for a given cloudiness level and calls light levels for each degree angle"
print "It then computes the correlation between daylight and indoor light for each cloudiness level and sun angle"

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
import DatabaseLight
import sqlite3
#Find the point biggest step change in daylight which will give the facade orientation for a given day from sun azimuth
#From the facade orientation it will be possible to find out how long the sun will be in this direction
#We will 4 consecutive clear days and compute the rate of change of illuminance and pick the time corresponding to majority days
#We then record the azimuth for this hour and assume this is the facade orientation
#This part of code is yet to be finished
connection=sqlite3.connect('data.db')
cursor=connection.cursor()
#define dicts to save data
win_daylight=dict()
win_sunangle=dict()
win_hours=dict()
newwin_daylight=dict()
sensors=raw_input('Enter the number of sensors you want to draw the relationship for:  ')
cloudy=["Clear",'Partly Cloudy','Scattered Clouds','Light Rain','Mostly Cloudy','Rain','Overcast','Heavy Rain','Fog','Haze'] #number of cloudiness could be user defined'''
#get values for each sensor in the room
for sensor in range(2,int(sensors)+2,1): 
    table='light'+str(sensor)
    daylight=dict()
    sunangle=dict()
    hours=dict()
    newdaylight=dict()
    newsunangle=dict()
    coeffam=dict()
    constantam=dict()
    rvalueam=dict()
    sunangles=dict()
    sunanglerange=dict()
    for clouds in range(len(cloudy)):
        win_daylight[clouds]=[]
        win_sunangle[clouds]=[]
        win_hours[clouds]=[]
        hours[clouds]=[]
        newwin_daylight[clouds]=[]
        newdaylight[clouds]=[]
        newsunangle[clouds]=[]
        daylight[clouds]=[]
        sunangle[clouds]=[]
        sunanglerange[clouds]=[]
        coeffam[clouds]=[]
        constantam[clouds]=[]
        rvalueam[clouds]=[]
        sunangles[clouds]=[]
        clouded=cloudy[clouds]
        cursor.execute('SELECT altitude, hour FROM light1 WHERE hour>=12 AND cloudiness="%s"' %(clouded))
        y1=cursor.fetchall()
        for count in y1:
            altitude=float(count[0])
            hour=int(count[1])
            if altitude>=0:
                win_sunangle[clouds].append(altitude)
                win_hours[clouds].append(hour)
        cursor.execute('SELECT altitude, hour FROM %s WHERE hour>=12 AND cloudiness="%s"' % (table, clouded))
        y2=cursor.fetchall()
        for count in y2:
            altitude=float(count[0])
            hour=int(count[1])
            if altitude>=0:
                sunangle[clouds].append(altitude)
                hours[clouds].append(hour)
        if len(sunangle[clouds])>len(win_sunangle[clouds]):
            datalength=len(win_sunangle[clouds])
        else:
            datalength=len(sunangle[clouds])
        for count in range(datalength):
            if int(win_sunangle[clouds][count])==int(sunangle[clouds][count]) and int(win_hours[clouds][count])==int(hours[clouds][count]):
                data=win_sunangle[clouds][count]
                newsunangle[clouds].append(data)
        #print newsunangle[clouds], clouded
        if len(newsunangle[clouds])>1:
            sunanglerange[clouds]=max(newsunangle[clouds])-min(newsunangle[clouds])
            #print sunanglerange[clouds],clouded
            #print newsunangle[clouds], clouded
            bins=1 #usually each sun angle bin is one degree, users can increase the bin size
            no_bins=sunanglerange[clouds]/bins
            #print no_bins
            sunangles[clouds]=np.arange(min(newsunangle[clouds]),max(newsunangle[clouds]),1)
            #print sunangles[clouds], clouded
            for angle in newsunangle[clouds]:
                cursor.execute('SELECT light FROM light1 WHERE hour>=12 AND cloudiness="%s" AND altitude="%s"' % (clouded,angle))
                y3=cursor.fetchall()
                #print y3,angle,clouded
                for count in y3:
                    actualdaylight=round(float(count[0]),2)
                    if actualdaylight>1:
                        win_daylight[clouds].append(actualdaylight)
                print len(win_sunangle[clouds]), len(sunangle[clouds]),len(win_daylight[clouds]), angle, clouded
            #print win_daylight[clouds]
##            cursor.execute('SELECT light FROM %s WHERE hour>=12 AND cloudiness="%s" AND altitude="%s"' % (table, clouded, angle))
##            y4=cursor.fetchall()
##            for count in y4:
##                daylight=round(float(count[0]),2)
##                if float(daylight)>1:
##                    daylight[clouds].append(daylight)
##            #print len(win_daylight[clouds],len(daylight[clouds])
##            if len(daylight[clouds])>5: 
##                adata=vstack((win_daylight[clouds],daylight[clouds]))
##                realadata=adata.transpose()
##                x=realadata[:,0]
##                y=realadata[:,1]
##                X=sm.add_constant(x)
##                model = sm.OLS(y, X).fit()
##                coeffam[clouds]=round(model.params[0],3)
##                constantam[clouds]=round(model.params[1],3)
##                rvalueam[clouds]=round(model.rsquared,3)
##                #print model.summary()
##                print "The coeff, constant and rvalue are", coeffam[clouds], constantam[clouds], rvalueam[clouds], "for", cloudy[clouds]

            

'''connection=sqlite3.connect('data.db')
cursor=connection.cursor()
#define dicts to save data
win_daylight=dict()
win_sunangle=dict()
#sensors=raw_input('Enter the number of sensors you want to draw the relationship for  ')
cloudy=["Clear",'Partly Cloudy','Scattered Clouds','Light Rain','Mostly Cloudy','Rain','Overcast','Heavy Rain','Fog','Haze'] ''''number of cloudiness could be user defined''''
for sensor in range(2,sensors+2,1):
    table='light'+sensor
    daylight=dict()
    sunangle=dict()
    azimuth=dict()
    azirange=dict()
    coeffam=dict()
    constantam=dict()
    rvalueam=dict()
    for clouds in range(len(cloudy)):
        win_daylight[clouds]=[]
        win_sunangle[clouds]=[]
        ''''win_azimuth[clouds]=[]''''
        daylight[clouds]=[]
        sunangle[clouds]=[]
        coeffam[clouds]=[]
        constantam[clouds]=[]
        rvalueam[clouds]=[]
        clouded=cloudy[clouds]
#get data from window sensor and store in arrays
        cursor.execute('SELECT light,altitude,hour FROM light1 WHERE hour>=12 AND cloudiness="%s"' %(clouded))
        y1=cursor.fetchall()
        for count in y1:
            light=round(float(count[0]),2)
            altitude=round(float(count[1]),2)
            hour=int(count[2])
            if altitude>=0 and light>1:
                win_daylight[clouds].append(light)
                win_sunangle[clouds].append(altitude)
#get data from any light sensor and store in arrays
        cursor.execute('SELECT light,altitude,hour FROM %s WHERE hour>=12 AND cloudiness="%s"' % table,(clouded))
        y2=cursor.fetchall()
        for count in y2:
            light=round(float(count[0]),2)
            altitude=round(float(count[1]),2)
            hour=int(count[2])
            if altitude>=0 and light>1:
                daylight[clouds].append(light)
                sunangle[clouds].append(altitude)
        if len(sunangle[clouds])>len(win_sunangle[clouds]):
            datalength=len(win_sunangle[clouds])
        else:
            datalength=len(sunangle[clouds])
        for count in range(datalength):
            if int(win_sunangle[clouds][count])=int(sunangle[clouds][count]) and int(win_hour[clouds][count])=int(hour[clouds][count]):
                newwin_daylight[clouds].append(win_daylight[clouds][count])
                newdaylight[clouds].append(daylight[clouds][count])
                newsunangle[clouds].append(win_sunangle[clouds][count])
        sunanglerange[clouds]=max(newsunangle[clouds])-min(newsunangle[clouds])
        bins=1 ''''usually each sun angle bin is one degree, users can increase the bin size''''
        no_bins=sunanglerange[clouds]/1
        sunangles=arange(min(newsunangle[clouds],max(newsunangle],1))
        for count in sunangles:
            
                
##perform OLS
        if len(daylight[clouds])>5:
            adata=vstack((sunangle[clouds],daylight[clouds]))
            realadata=adata.transpose()
            x=realadata[:,0]
            y=realadata[:,1]
            X=sm.add_constant(x)
            model = sm.OLS(y, X).fit()
            coeffam[clouds]=round(model.params[0],3)
            constantam[clouds]=round(model.params[1],3)
            rvalueam[clouds]=round(model.rsquared,3)
            print model.summary()
            print "The coeff, constant and rvalue are", coeffam[clouds], constantam[clouds], rvalueam[clouds], "for", cloudy[clouds]
print "   "
print "done"

'''
