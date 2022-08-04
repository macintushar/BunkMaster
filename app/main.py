from functools import total_ordering
from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3 as sql
from functions import CurrentLimit, CurrentPercentage, Edit_Limit

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    con=sql.connect("BunkMaster.db")
    con.row_factory=sql.Row
    cur=con.cursor()

    cur.execute("SELECT * FROM Lectures")
    data=cur.fetchall()
    
    cur.execute("SELECT totalHours FROM Lectures")
    total = cur.fetchall()

    cur.execute("SELECT bunkedHours FROM Lectures")
    bunked = cur.fetchall()

    limit = CurrentLimit()

    cur.execute("SELECT COUNT(*) FROM Lectures")
    count = cur.fetchone()
    count = int(count[0])
    
    bunkable = []

    for i in range(0,count):
        bunkable.append(int((((total[i])[0]) - ((total[i])[0]) * limit/100)-(bunked[i])[0]))

    current = CurrentPercentage()

    current = round(current,2)

    if current<limit:
        attStatus="danger"
    
    if current>limit:
        attStatus="success"

    return render_template("index.html",datas=data, limit=limit, bunk=bunkable, color=attStatus, percent = current) 
   
@app.route("/add",methods=['POST','GET'])
def add():
    if request.method=='POST':
        CourseID = request.form['course']
        Subject = request.form['subject']
        TotalHours = request.form['total']
        BunkedHours = request.form['bunked']

        con=sql.connect("BunkMaster.db")
        cur=con.cursor()

        cur.execute("INSERT INTO Lectures(CourseID,Subject,totalHours,bunkedHours) VALUES (?,?,?,?)",(CourseID,Subject,TotalHours,BunkedHours))
        con.commit()
        flash('Course Added','success')
        return redirect(url_for("index"))
    return render_template("add.html")

@app.route("/edit/<string:uid>",methods=['POST','GET'])
def edit(uid):
    if request.method=='POST':
        CourseID = request.form['course']
        Subject = request.form['subject']
        TotalHours = request.form['total']
        BunkedHours = request.form['bunked']

        con=sql.connect("BunkMaster.db")
        cur=con.cursor()

        cur.execute("UPDATE Lectures SET Subject=?, totalHours=?, bunkedHours=? WHERE CourseID=?",(Subject,TotalHours,BunkedHours, CourseID))
        con.commit()

        flash('Course Updated','success')
        return redirect(url_for("index"))
    
    con=sql.connect("BunkMaster.db")
    con.row_factory=sql.Row
    cur=con.cursor()

    print(uid)

    cur.execute("SELECT * FROM Lectures WHERE CourseID=?",(uid,))
    data=cur.fetchone()

    return render_template("edit.html",row=data)
    
@app.route("/delete/<string:uid>",methods=['GET'])
def delete(uid):
    con=sql.connect("BunkMaster.db")
    cur=con.cursor()
    cur.execute("DELETE FROM Lectures where CourseID=?",(uid,))
    con.commit()
    flash('Course Deleted','warning')
    return redirect(url_for("index"))

@app.route("/plusBunked/<string:uid>",methods=['GET'])
def plusHour(uid):
    con=sql.connect("BunkMaster.db")
    cur=con.cursor()
    cur.execute("UPDATE Lectures SET bunkedHours=bunkedHours+1 where CourseID=?",(uid,))
    con.commit()
    flash('Increased Bunked Hour','warning')
    return redirect(url_for("index"))

@app.route("/minusBunked/<string:uid>",methods=['GET'])
def minusHour(uid):
    con=sql.connect("BunkMaster.db")
    cur=con.cursor()
    cur.execute("UPDATE Lectures SET bunkedHours=bunkedHours-1 where CourseID=?",(uid,))
    con.commit()
    flash('Reduced Bunked Hour','warning')
    return redirect(url_for("index"))

@app.route("/plusConducted/<string:uid>",methods=['GET'])
def plusConducted(uid):
    con=sql.connect("BunkMaster.db")
    cur=con.cursor()
    cur.execute("UPDATE Lectures SET totalHours=totalHours+1 where CourseID=?",(uid,))
    con.commit()
    flash('Increased Total Hour','warning')
    return redirect(url_for("index"))

@app.route("/minusConducted/<string:uid>",methods=['GET'])
def minusConducted(uid):
    con=sql.connect("BunkMaster.db")
    cur=con.cursor()
    cur.execute("UPDATE Lectures SET totalHours=totalHours-1 where CourseID=?",(uid,))
    con.commit()
    flash('Reduced Total Hour','warning')
    return redirect(url_for("index"))

@app.route("/limit",methods=['POST','GET'])
def limit():
    con=sql.connect("BunkMaster.db")
    cur=con.cursor()
    if request.method=='POST':
        att = request.form['limit']
        Edit_Limit(newMinAttendance=att)
        flash('Minimum Attendance Changed','success')
        return redirect(url_for("index"))
    
    cur.execute("SELECT MinAttendance FROM AttLimit")
    data=cur.fetchone()

    return render_template("limit.html", datas=data)


if __name__=='__main__':
    app.secret_key='admin123'
    app.run(debug=True)