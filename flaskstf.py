from flask import Flask, session, redirect, url_for, request, render_template, flash
from flask_socketio import SocketIO, emit
import psycopg2
from connect4 import FourInARowBoard
from BoardStore import BoardStore
app = Flask(__name__)
app.secret_key = 'random string'
#added in
async_mode= None
socketio = SocketIO(app, async_mode=async_mode)
thread = None


board_store = BoardStore()

class NotYourTurn(Exception):
    pass

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(100)
        count += 1
        socketio.emit('my_response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')
#look into this!
#this way probably won't work
def reload():
    board = board_store.get_board(session['board_index'])
    while True:
        socketio.sleep(1000)
        return render_template('wait.html', result = session['board_index'].listify(), board = board)

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
                session['username'] = x[1]
                board_store.join_game(session['username'])
                board_index = board_store.index
                session['board_index'] = board_index
                board = board_store.get_board(board_index)
                if board.is_current_player(session['username']):
                    return redirect(url_for('connect4_online', move = 0))
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
        return redirect(url_for('index'))
    return render_template('register.html', error = error)

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/board/<move>/')
def connect4_online(move):
    move = int(move)
    board = board_store.get_board(session['board_index'])
    if move == 0:
        return board.current_turn_string() + '<br>' + render_template('table.html', result = board.listify(), board = board)
    #if session['board_index']._winner:
    #    return "END!!!" #TODO redirect to end pagw
    if board.is_current_player(session['username']):
        raise NotYourTurn()
    else:
        board.make_move(move)
        return str(board.current_turn_string()) + '<br>' + render_template('wait.html', result = board.listify(), board = board)


@app.route('/move', methods=['POST', 'GET'])
def move():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('connect4_online', move=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('connect4_online', move=user))

@app.route('/wait/', methods=['POST', 'GET'])
def wait():
    board = board_store.get_board(session['board_index'])
    if board.is_current_player(session['username']):
        return render_template('table.html', result = board.listify(), board = board)
    else:
        return render_template('wait.html', result = board.listify(), board = board)

#added in
"""@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('s.make_move(movel)',
         {'data': message['data']})"""


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


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)