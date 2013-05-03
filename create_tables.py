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
cursor.execute('''CREATE TABLE light1 (unixtime REAL, weekday TEXT,
                day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                azimuth REAL, cloudiness TEXT, x REAL, y REAL,
                PRIMARY KEY (unixtime))''')

cursor.execute('''CREATE TABLE light2 (unixtime REAL, weekday TEXT,
                day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                azimuth REAL, cloudiness TEXT, x REAL, y REAL,
                PRIMARY KEY (unixtime))''')

cursor.execute('''CREATE TABLE light3 (unixtime REAL, weekday TEXT,
                day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                azimuth REAL, cloudiness TEXT, x REAL, y REAL,
                PRIMARY KEY (unixtime))''')

cursor.execute('''CREATE TABLE light4 (unixtime REAL, weekday TEXT,
                day INTEGER, month INTEGER, year INTEGER, hour INTEGER,
                minute INTEGER, seconds INTEGER, light REAL, altitude REAL,
                azimuth REAL, cloudiness TEXT, x REAL, y REAL,
                PRIMARY KEY (unixtime))''')

#Create one table for cloud measurement data

cursor.execute('''CREATE TABLE cloud (timezone TEXT, year INTEGER, month
                INTEGER, day INTEGER, hour INTEGER, minute INTEGER, seconds
                INTEGER, unixtime REAL, cloudiness TEXT, PRIMARY KEY
                (year, month, day, hour, minute, seconds))''')

#Create one table for cloudiness value per day

cursor.execute('''CREATE TABLE daycloud (year INTEGER, month INTEGER, day
                INTEGER, clearcount INTEGER, PRIMARY KEY (year, month, day))''')

#Save your changes
connection.commit()
