from flask import Flask, session, redirect, url_for, request, render_template, flash
import psycopg2
app = Flask(__name__)
from connect4 import FourInARowBoard
app.secret_key = 'random string'

s = FourInARowBoard()
red = None
yellow = None

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
   player = ["", ""]
   if request.method == 'POST':
        while x != None:
            x = cursor.fetchone()
            if request.form['username'] == x[1] and \
            request.form['password'] == x[2]:
                if request.form['colour'] == 'red':
                    player[0] = x[0]
                elif request.form['colour'] == 'yellow':
                    player[1] = x[0]
                else:
                    return 'URRRRRRRRRRG!!!'
                if player[0] == x[0]:
                    return 'R players\' turn' + render_template('table.html', player = player, self = x[0], result = s.listify())
                else:
                    return redirect(url_for('wait'))
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
        return render_template('table.html', player = x[1])
    return render_template('register.html', error = error)

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/board/<player>/<self>/<mov>/')
def connect4_online(player, self, mov):
    mov = int(mov)
    while s._winner:
        return "END!!!"
    if (s._player == 'R' and player[0] == self) or (s._player =='Y' and player[1] == self)
        return str(s.make_move(mov)) + '<br>' + render_template('table.html', player = player, self = self, result = s.listify())
    else:
        return redirect(url_for('wait'))


@app.route('/move', methods=['POST', 'GET'])
def move():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('connect4_online', mov=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('connect4_online', mov=user))

@app.route('/wait', methods=['POST', 'GET'])
def wait():
    return render_template('wait.html', result = s.listify())

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
#session keys and long polling