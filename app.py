from flask import Flask,render_template,request,redirect,session
import mysql.connector


app = Flask(__name__)
app.secret_key = "randomsdasd"
db_connection = mysql.connector.connect(
     host="localhost",
     user="root",
     password="",
     database="quick"
)
#CRUD

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about_page():
    return "THIS IS ABOUT PAGE"

@app.route('/login')
def login_page():
    session['log'] =""
    return render_template('login.html',message=session['message'])
@app.route('/login',methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    db_cursor = db_connection.cursor(dictionary=True)
    query = f"Select username,password from users where username = '{username}'"
    db_cursor.execute(query)
    result = db_cursor.fetchone()
    if result:
        if result['password'] == password:
            session['log'] = "SET"
            return redirect('/dashboard')
        else:
            session['message'] = "Invalid Password"
            return redirect('/login')
    else:
        session['message'] = "Invalid Username"
        return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if(session['log'] == "SET"):
        return render_template('dashboard.html')
    else:
        return redirect('/login')
@app.route('/CRUD')
def CRUD_page():
    db_cursor = db_connection.cursor(dictionary=True)
    query = "Select * from users"
    db_cursor.execute(query)
    result = db_cursor.fetchall()
    print(result)
    return render_template('CRUD.html',users=result)

@app.route('/CRUD',methods=['POST'])
def insert_data():
    firstname = request.form.get('firstname')
    middlename = request.form.get('middlename')
    lastname = request.form.get('lastname')
    username = request.form.get('username')
    password = request.form.get('password')
    query = f"INSERT INTO users (first_name,middle_name,last_name,username,password) VALUES ('{firstname}','{middlename}','{lastname}','{username}','{password}')"
    db_cursor = db_connection.cursor()
    db_cursor.execute(query)
    db_connection.commit()
    return redirect('/CRUD')

@app.route('/CRUD/<id>',methods=['DELETE','GET'])
def delete_data(id):
    query = f"Delete from users where id = {id}"
    db_cursor = db_connection.cursor()
    db_cursor.execute(query)
    db_connection.commit()
    return redirect('/CRUD')
if(__name__ == "__main__"):
    app.run(debug=True)

