
NUM_COL = 8
NUM_ROW = 7
EMPTY = ' '
RED = 'R'
YELLOW = 'Y'
SIDE_EDGE = '\n'

DIRECTIONS = [NUM_COL, +1, NUM_COL-1, NUM_COL+1]

class InvalidMove(Exception):
    pass

class FourInARowBoard(object):

    def __init__(self):
        self._setup_board()
        self._winner = None
        self._player = RED

    def make_move(self, column):
        try:
            self._update_board(column, self._player)
        except InvalidMove:
            return 'Invalid Move'
        if self._winner:
            return 'Woo %s has won' % self._winner
        return self._swap_player()
       
    def _setup_board(self):
        self._board = [EMPTY] * (NUM_COL * NUM_ROW)
        for column in range(NUM_COL):
          self._board[NUM_ROW * NUM_COL - column - 1] = str(column)
        for row in range(NUM_ROW):
            self._board[(row + 1) * NUM_COL - 1] = SIDE_EDGE
      
    def __str__(self):
        return '|' + '|'.join(self._board)

    def _update_board(self, column, player):
        if column <= 0 or column >= NUM_COL:
            raise InvalidMove()
        start = NUM_COL * NUM_ROW - 1 - column
        for index in range(start, -1, -NUM_COL):
            if self._board[index] == EMPTY:
                self._board[index] = player
                self._check_winner()
                break
        else:
            raise InvalidMove()

    def _swap_player(self):
        if self._player == RED:
            self._player = YELLOW
        else:
             self._player = RED
        return '%s players\' turn' % (self._player)


    @property
    def _all_squares(self):
        start = NUM_COL * NUM_ROW -1
        return range(start,-1,-1)

    def _check_winner(self):
        for index in self._all_squares: 
            if self._board[index] == self._player:
                self._check_index_winner(index)
                
    def _check_index_winner(self, index):
        for direction in DIRECTIONS:               
            for distance in range(4):
                #print index+direction*distance, self._board[index+direction*distance]
                if self._board[index + direction*distance] != self._board[index]:
                    #print 'break'
                    break
            else:
                self._winner = self._board[index]
    
