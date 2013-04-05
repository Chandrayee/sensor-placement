#Using sqlite3 in Python

import sqlite3
from sqlite3 import dbapi2 as sqlite3

#Create a database data.db and connect to it
connection = sqlite3.connect('data.db')
cursor = connection.cursor()

#Create one table for cloudiness data
#If you created the table previously, comment this out
cursor.execute('''CREATE TABLE cloudiness (day int, month int, year int,
                    level float, cloudiness text)''')
					
cursor.execute('INSERT INTO cloudiness VALUES (?,?,?,?,?)', to_db)

#Selects rows from cloudiness table where level < 3.3 (indicates sunny) and
#prints each row
for row in cursor.execute('SELECT * FROM cloudiness WHERE level>3.3'):
    print(row)
	
#To retrieve data AFTER executing a SELECT statement, you can use the iterator method like above, or use fetchone() or fetchall()

cursor.execute('SELECT * FROM cloudiness WHERE level>3.3')
print cursor.fetchone() #Prints first row of the table
print cursor.fetchmany(5) #Prints 5 rows of the table in a list format
print cursor.fetchall() #Prints every row of the table

#Close the database connection
connection.close()
