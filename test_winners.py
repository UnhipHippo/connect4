
from connect4 import FourInARowBoard
x = [1,2,3,3,3,4,4,4,2,5,4]

def test_vertical_win():
    s = FourInARowBoard()
    for i in range(3):
        print s.make_move(3)
        print s
        print s.make_move(7)
        print s
    print s.make_move(2)
    print s
    print s.make_move(7)
    print s

def test_horizontal_win():
    s = FourInARowBoard()
    for i in range(1,4):
        print s.make_move(i)
        print s
        print s.make_move(i)
        print s
    if s._winner is not True:
        raise exception

def test_diagonal_win():
    s = FourInARowBoard()
    #y = [i+1 for i in x]
    for i in x:
        print s.make_move(i)
        print s

#test_vertical_win()
test_horizontal_win()
#test_diagonal_win()
#test_red_win()
#test_yellow_win()


