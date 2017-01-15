from flask import Flask, redirect, url_for, request, render_template, flash
import psycopg2
app = Flask(__name__)
from connect4 import FourInARowBoard
app.secret_key = 'random string'

s = FourInARowBoard()


@app.route('/')
def index():
   return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
   error = None
   conn = psycopg2.connect("dbname=userinfo user=sam")
   cursor = conn.cursor()
   cursor.execute('select * from logindata')
   x= []
   if request.method == 'POST':
        while x != None:
            x = cursor.fetchone()
            if request.form['username'] == x[1] and \
            request.form['password'] == x[2]:
                flash('You were successfully logged in')
                return render_template('table.html')
        error = 'Invalid username or password. Please try again!'
   return render_template('login.html', error = error)

@app.route('/register', methods = ['Get', 'POST'])
def register():
    error = None
    conn = psycopg2.connect("dbname=userinfo user=sam")
    cursor = conn.cursor()
    cursor.execute('select * from logindata')
    x = cursor.fetchone()
    if request.method == 'POST':
        while x != None:
            if request.form['username'] == x[1]:
                return 'Invalid Username!' + '<br>' + render_template('register.html')
            else:
                x = cursor.fetchone()
        cursor.execute(
            "INSERT INTO logindata (username, password) VALUES (%s, %s)",
            (str(request.form['username']), str(request.form['password']))
        )
        conn.commit()
        flash('You have been registered')
        return render_template('table.html')
    return render_template('register.html', error = error)

@app.route('/menu')
def menu():


@app.route('/board/<mov>')
def connect4_online(mov):
    mov = int(mov)
    while s._winner:
        return "END!!!"
    return str(s.make_move(mov)) + '<br>' + render_template('table.html', result = s.listify())


@app.route('/move', methods=['POST', 'GET'])
def move():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('connect4_online', mov=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('connect4_online', mov=user))
