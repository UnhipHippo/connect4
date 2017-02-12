from flask import Flask, session, redirect, url_for, request, render_template, flash
#added in
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

import psycopg2
app = Flask(__name__)
from connect4 import FourInARowBoard
app.secret_key = 'random string'
#added in
async_mode= None
socketio = SocketIO(app, async_mode=async_mode)
thread = None

s = FourInARowBoard()
red = None
yellow = None

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')
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
    if (s._player == 'R' and player[0] == self) or (s._player =='Y' and player[1] == self):
        return '<br>' + render_template('table.html', player = player, self = self, result = s.listify())
    else:
        return str(s.make_move(mov)) + '<br>' + render_template('wait.html', result = s.listify())
        #return redirect(url_for('wait'))


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
    #if s._player == 'Y':
    #    return 'wads'
    #else:
    return render_template('wait.html', result = s.listify())

#added in
@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    session['number'] = session.get('data', 0)
    if session['number'] == '1':
        emit('my_response',
            {'data': message['fuck yeah'], 'count': session['receive_count']})
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)

@socketio.on('my_ping', namespace='/test')
def ping_pong():
    emit('my_pong')


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})




app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

#session keys and long polling and https://blog.miguelgrinberg.com/post/easy-websockets-with-flask-and-gevent
#help me!

if __name__ == '__main__':
    socketio.run(app, debug=True)