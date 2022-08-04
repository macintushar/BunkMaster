import sqlite3 as sql
import matplotlib.pyplot as plt
import numpy as np

def Add_Limit(minAttendance):
    conn = sql.connect(r'./BunkMaster.db')
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS Limit(MinAttendance INTEGER DEFAULT=75)")
    conn.commit()

    cursor.execute("INSERT INTO Limit VALUES (?)", (minAttendance))
    conn.commit()

def Edit_Limit(newMinAttendance):
    conn = sql.connect(r'./BunkMaster.db')
    cursor = conn.cursor()

    cursor.execute("UPDATE AttLimit SET MinAttendance = (?)", (newMinAttendance,))
    conn.commit()

def CurrentPercentage():
    conn = sql.connect(r'./BunkMaster.db')
    cur = conn.cursor()

    cur.execute("SELECT sum(totalHours) FROM Lectures")
    tot = cur.fetchone()
    total=tot[0]

    cur.execute("SELECT sum(bunkedHours) FROM Lectures")
    bunk = cur.fetchone()
    bunked = bunk[0]

    attended = total-bunked
    percentage=(attended/total)*100
    
    return(percentage)

def CurrentLimit():
    conn = sql.connect(r'./BunkMaster.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM AttLimit")
    lim = cursor.fetchone()
    lim = list(lim)

    return lim[0]