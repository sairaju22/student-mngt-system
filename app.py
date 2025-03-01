from flask import Flask,render_template,request,url_for,redirect,session,flash

import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash,check_password_hash
app = Flask(__name__)
app.secret_key="pip1234"#secret key is for session mgmt

#mysql db connection configure
db_config={
    'host':'localhost',
    'user':'root',
    'password':'root',
    'database':'student'
}
#helper function to get a db
def get_db_connection():
    try:
        connection=mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print("Error while connecting to mysql",e)
        return None
@app.route("/")
def dashboard():
    if 'username' in session:
        return render_template('homepage.html',username=session['username'])
    else:
        flash("please log in first","Warning")
        return redirect(url_for('login'))
    
@app.route("/login",methods=['GET','POST'])
def login():
    if request.method =="POST":
        username=request.form['username']
        password=request.form['password']

        conn=get_db_connection()
        if conn:
            cursor=conn.cursor()
            cursor.execute("SELECT* FROM users WHERE username=%s",(username,))
            user=cursor.fetchone()
            conn.close()

            if user and check_password_hash(user[4],password):
                session['username']=username
                flash('Login successful','success')
                return redirect(url_for('dashboard'))
            else:
                print("Invalid username or password")
    return render_template('login.html')


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=="POST":
        username=request.form['username']
        address=request.form['address']
        student_id=request.form['student_id']
        password=request.form['password']
        email=request.form['email']
        print(password)
        print(email)
        hash_password=generate_password_hash(password)
        print(hash_password)
        #connect to db
        conn=get_db_connection()
        if conn:
            cursor=conn.cursor()
            cursor.execute("SELECT* FROM users WHERE username=%s",(username,))
            existing_user=cursor.fetchone()
            if existing_user:
                print("Username already exists.please choose another one.")
                conn.close()
                return redirect(url_for('register'))
            cursor.execute("insert into users(username,address,student_id,password,email) values(%s,%s,%s,%s,%s)",(username,address,student_id,hash_password,email))
            conn.commit()
            cursor.close()
            conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')
@app.route('/std_reg',methods=['GET','POST'])
def student_register():
    if request.method=="POST":
        name=request.form['name']
        address=request.form['address']
        age=request.form['age']
        email=request.form['email']
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute("Insert into students (name,address,age,email) values(%s,%s,%s,%s)",(name,address,age,email))
        conn.commit()
        conn.close()
        flash("student registered successfully!","success")
    return render_template('student_register.html')

@app.route('/student_list')
def student_list():
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("select * from students")
    students=cursor.fetchall()
    print(students)
    conn.close()
    return render_template('student_list.html',students=students)

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit_student(id):
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("select* from students Where id=%s",(id,))
    student=cursor.fetchone()
    print(student)
    if request.method=="POST":
        name=request.form['name']
        address=request.form['address']
        age=request.form['age']
        email=request.form['email']
        cursor.execute("UPDATE students SET name=%s,address=%s,age=%s,email=%s where id=%s",(name,address,age,email,id))
        conn.commit()
        conn.close()
        flash("student details updated successfully!","success")
    return render_template('student_update.html',student=student)
@app.route('/delete/<int:id>',methods=['GET','POST'])
def delete_student(id):
    if request.method=="POST":
        conn=get_db_connection()
        cursor=conn.cursor()
        cursor.execute("Delete From students\
        WHERE id=%s",(id,))
        conn.commit()
        conn.close()
        flash("Student deleted sucessfully","success")
        return redirect(url_for('student_list'))
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)
    cursor.execute("SELECT *FROM students where id=%s",(id,))
    student=cursor.fetchone()
    conn.close()
    return render_template('delete_conformation.html',student=student)

#dynamic routing
#string route(defauly type)
@app.route('/user/<string:username>')
def show_user(username):
    return f"Hello,{username}"

@app.route('/user_id/<int:user_id>')
def show_user_by_id(user_id):
    return f'user id is {user_id}'

@app.route('/price/<float:price>')
def show_price(price):
    return f'The price is{price}'

@app.route('/path/<path:subpath>')
def show_path(subpath):
    return f"The path is {subpath}"


@app.route('/uuid/<uuid:item_id>')
def show_uuid(item_id):
    return f"The uuid is {item_id}"

@app.route('/logout')
def logout():
    session.pop('username',None)
    flash("You've been logedout")
    return redirect(url_for('login'))

app.run(debug=True)
