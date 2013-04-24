import sqlite3
from sqlite3 import dbapi2 as sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()
#cloud_val = unicode("Clear")
cloud_val = ('Clear',)
#cursor.execute('SELECT * FROM light1')
#print cursor.fetchone()
cursor.execute('SELECT * FROM light1 WHERE cloudiness=?', cloud_val)
#cursor.execute('SELECT * FROM light1')
for i in cursor.fetchmany(10):
    print i
