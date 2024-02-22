import sqlite3 as sql

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/create_table')
def createTable():
    try:
        with sql.connect('database.db') as con:
            con.execute("CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)")
    except:
        print("Table exists")
    finally:
        con.close()
        return render_template('student.html')
    
@app.route('/add_new')
def new_student():
    return render_template('student.html')

@app.route('/add_rec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['addr']
            city = request.form['city']
            pin = request.form['pin']

            with sql.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO students VALUES (?,?,?,?)",(nm,addr,city,pin))
                con.commit()
                msg = "Record successfully added"

        except:
            con.rollback()
            msg = "Error in adding record"
        
        finally:
            con.close()
            return render_template("result.html", msg = msg)
        
@app.route('/list')
def list():
    con = sql.connect('database.db')
    con.row_factory = sql.Row
    
    cur = con.cursor()
    cur.execute("SELECT * FROM students")

    rows = cur.fetchall()
    return render_template("list.html", rows = rows)

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)