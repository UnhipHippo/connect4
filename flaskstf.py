from flask import Flask, session, redirect, url_for, request, render_template
import psycopg2
from BoardStore import BoardStore
app = Flask(__name__)
app.secret_key = 'rxPysSdh asdjasDFdSK'


board_store = BoardStore()

class NotYourTurn(Exception):
    pass

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
            try:
                if request.form['username'] == x[1] and \
                request.form['password'] == x[2]:
                    session['username'] = x[1]
                    board_store.join_game(session['username'])
                    board_index = board_store.index
                    session['board_index'] = board_index
                    return redirect(url_for('hub'))
                error = 'Invalid username or password. Please try again!'
            except TypeError:
                error = 'You didn\'t input your password or username'
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
            try:
                if request.form['username'] == x[1]:
                    return 'Invalid Username!' + '<br>' + render_template('register.html')
                else:
                    x = cursor.fetchone()
            except TypeError:
                error = "You didn't enter a password or username"
                return render_template('register.html', error = error)
        cursor.execute(
            "INSERT INTO logindata (username, password) VALUES (%s, %s)",
            (str(request.form['username']), str(request.form['password']))
        )
        conn.commit()
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
        return render_template('table.html', result = board.listify(), board = board)
    if board.game_won():
        return 'Game Over: %s has won!' %(board.game_won()) + '<br>' + render_template('game_over.html', result = board.listify(), board = board)
    if not board.is_current_player(session['username']):
        raise NotYourTurn()
    else:
        board.make_move(move)
        return str(board.current_turn_string()) + '<br>' + render_template('wait.html', result = board.listify(), board = board)

@app.route('/wait/', methods=['POST', 'GET'])
def wait():
    board = board_store.get_board(session['board_index'])
    if board.game_won():
        return 'Game Over: %s has won!' %(board.game_won()) + '<br>' + render_template('game_over.html', result = board.listify(), board = board)
    if board.is_current_player(session['username']):
        return render_template('table.html', result = board.listify(), board = board)
    else:
        return str(board.current_turn_string()) + '<br>' + render_template('wait.html', result = board.listify(), board = board)

@app.route('/hub/')
def hub():
    board = board_store.get_board(session['board_index'])
    if board.has_both_players():
        if board.is_current_player(session['username']):
            return redirect(url_for('connect4_online', move = 0))
        else:
            return redirect(url_for('wait'))
    else:
        return render_template('hub.html')

@app.route('/newgame')
def new_game():
    board_store.join_game(session['username'])
    board_index = board_store.index
    session['board_index'] = board_index
    return redirect(url_for('hub'))
