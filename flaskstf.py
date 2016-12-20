from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__)
from connect4 import FourInARowBoard
SUBMIT = '<form action = "http://localhost:5000/move" method = "post"><p>Enter Number:</p><p><input type = "text" name = "nm" /></p><p><input type = "submit" value = "submit" /></p></form>'
s = FourInARowBoard()

@app.route('/board/<mov>')
def connect4_online(mov):
    mov = int(mov)
    return str(s.make_move(mov)) + '<br>' + SUBMIT + '<br>' + str(s)

@app.route('/move', methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('connect4_online',mov = user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('connect4_online',mov = user))