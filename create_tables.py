"""Code for creating the database data.db and for creating the tables of
the database: light1,...,light4 (light measurement tables for each BEST lab
sensor number) and cloud (weather data from Wunderground).
"""

import sqlite3
from sqlite3 import dbapi2 as sqlite3

#Create a database data.db and connect to it
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

#Create one table per sensor for light measurement data
cursor.execute('''CREATE TABLE light1 (unixtime float, weekday string,
                day int, month int, year int, hour int, minute int,
                seconds int, light float, altitude float, azimuth float, cloudiness string,
                PRIMARY KEY (unixtime))''')

cursor.execute('''CREATE TABLE light2 (unixtime float, weekday string,
                day int, month int, year int, hour int, minute int,
                seconds int, light float, altitude float, azimuth float, cloudiness string,
                PRIMARY KEY (unixtime))''')

cursor.execute('''CREATE TABLE light3 (unixtime float, weekday string,
                day int, month int, year int, hour int, minute int,
                seconds int, light float, altitude float, azimuth float, cloudiness string,
                PRIMARY KEY (unixtime))''')

cursor.execute('''CREATE TABLE light4 (unixtime float, weekday string,
                day int, month int, year int, hour int, minute int,
                seconds int, light float, altitude float, azimuth float, cloudiness string,
                PRIMARY KEY (unixtime))''')

#Create one table for cloud measurement data
#cursor.execute('''CREATE TABLE cloud (timezone string, year int, month int,
 #               day int, time string, cloudiness string)''')

"""cursor.execute('''CREATE TABLE cloud (timezone string, year int, month int,
                day int, hour int, minute int, seconds int,
                cloudiness string, PRIMARY KEY (year, month, day, hour,
                minute, seconds))''')"""

#Save your changes
connection.commit()
