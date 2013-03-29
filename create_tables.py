import sqlite3
from sqlite3 import dbapi2 as sqlite3

#Create a database data.db and connect to it
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

#Create one table per sensor for light measurement data
cursor.execute('''CREATE TABLE light1 (weekday string, day int, month int,
                year int, hour int, minute int, seconds int, light float)''')

cursor.execute('''CREATE TABLE light2 (weekday string, day int, month int,
                year int, hour int, minute int, seconds int, light float)''')

cursor.execute('''CREATE TABLE light3 (weekday string, day int, month int,
                year int, hour int, minute int, seconds int, light float)''')

cursor.execute('''CREATE TABLE light4 (weekday string, day int, month int,
                year int, hour int, minute int, seconds int, light float)''')

#Create one table for cloud measurement data
cursor.execute('''CREATE TABLE cloud (timezone string, year int, month int,
                day int, time string, cloudiness string)''')

#Save your changes
connection.commit()
