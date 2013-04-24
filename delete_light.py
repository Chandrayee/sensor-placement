import sqlite3
from sqlite3 import dbapi2 as sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()
cursor.execute('DROP TABLE light1')
cursor.execute('DROP TABLE light2')
cursor.execute('DROP TABLE light3')
cursor.execute('DROP TABLE light4')
cursor.execute('''CREATE TABLE light2 (unixtime float, weekday string,
                day int, month int, year int, hour int, minute int,
                seconds int, light float, altitude float, azimuth float,
                cloudiness string,
                PRIMARY KEY (unixtime))''')
cursor.execute('''CREATE TABLE light3 (unixtime float, weekday string,
                day int, month int, year int, hour int, minute int,
                seconds int, light float, altitude float, azimuth float,
                cloudiness string,
                PRIMARY KEY (unixtime))''')
cursor.execute('''CREATE TABLE light4 (unixtime float, weekday string,
                day int, month int, year int, hour int, minute int,
                seconds int, light float, altitude float, azimuth float,
                cloudiness string,
                PRIMARY KEY (unixtime))''')
cursor.execute('''CREATE TABLE light1 (unixtime float, weekday string,
                day int, month int, year int, hour int, minute int,
                seconds int, light float, altitude float, azimuth float,
                cloudiness string,
                PRIMARY KEY (unixtime))''')


