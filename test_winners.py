
from connect4 import FourInARowBoard
x = [1,2,3,3,3,4,4,4,2,5,4]

def test_vertical_win():
    s = FourInARowBoard()
    for i in range(4):
        print s.make_move(3)
        print s
        print s.make_move(7)
        print s

def test_horizontal_win():
    s = FourInARowBoard()
    for i in range(1,5):
        print s.make_move(i)
        print s
        print s.make_move(i)
        print s

def test_diagonal_win():
    s = FourInARowBoard()
    for i in x:
        #i = 8-i
        print s.make_move(i)
        print s

def test_yellow_win():
    s = FourInARowBoard()
    print s.make_move(1)
    for i in range(4):
        print s.make_move(3)
        print s
        print s.make_move(7)
        print s

def play_game(): 
    s = FourInARowBoard()
    print s
    while not s._winner:
        n = int(raw_input("Where would you like to place it?: "))
        print s.make_move(n)
        print s

#test_vertical_win()
#test_horizontal_win()
#test_diagonal_win()
#test_yellow_win()
#play_game()

