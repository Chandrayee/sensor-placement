import sqlite3
from sqlite3 import dbapi2 as sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

cloud_val = ("Clear",) #Insert whatever cloudiness value you want
cloud = cursor.execute('SELECT * FROM light1 WHERE cloudiness = ?', cloud_val)

#Print values
for i in cursor.fetchmany(10):
    print i
