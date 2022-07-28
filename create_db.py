import sqlite3 as sql

con = sql.connect('BunkMaster.db')
cur = con.cursor()


cur.execute("DROP TABLE IF EXISTS Lectures")
cur.execute("CREATE TABLE Lectures (CourseID INTEGER PRIMARY KEY, Subject TEXT, totalHours INTEGER, bunkedHours INTEGER)")
cur.execute("INSERT INTO Lectures VALUES(0, 'Test', 1,0)")

cur.execute("DROP TABLE IF EXISTS AttLimit")
cur.execute("CREATE TABLE AttLimit(MinAttendance INTEGER)")
cur.execute("INSERT INTO AttLimit VALUES(75)")

#commit changes
con.commit()

#close the connection
con.close()