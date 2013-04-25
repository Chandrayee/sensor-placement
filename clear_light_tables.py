import sqlite3
from sqlite3 import dbapi2 as sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()
cursor.execute('DROP TABLE light1')
cursor.execute('DROP TABLE light2')
cursor.execute('DROP TABLE light3')
cursor.execute('DROP TABLE light4')
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


connection.commit()
