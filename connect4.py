
NUM_COL = 8
NUM_ROW = 7
EMPTY = " "
SIDE_EDGE = "\n"

DIRECTIONS = [NUM_COL, +1, NUM_COL-1, NUM_COL+1]

class InvalidMove(Exception):
    pass

class FourInARowBoard(object):

    def __init__(self):
        self._setup_board()
        self._winner = None
        self._player = None
        self._red = None
        self._yellow = None

    def make_move(self, column):
        try:
            self._update_board(column, self._player)
        except InvalidMove:
            return 'Invalid Move'
        if self._winner:
            return 'Woo %s has won' % self._winner
        self._swap_player()
       
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

    def listify(self):
        newlist = []
        for row in range(1,NUM_ROW):
            lst = []
            for column in range(NUM_COL-1,0,-1):
                lst.append(self._board[(row-1)*NUM_COL+column-1])
            newlist.append(lst)
        return newlist

    def set_first_player(self, username):
        self._red = username
        self._player = username

    def set_second_player(self, username):
        self._yellow = username

    def has_both_players(self):
        return self._red is not None and self._yellow is not None

    def is_current_player(self, username):
        return username == self._player

    def is_red(self, username):
        return username is self._red

    def is_yellow(self, username):
        return username is self._yellow

    def game_won(self):
        return self._winner


    def _swap_player(self):
        if self._player == self._red:
            self._player = self._yellow
        else:
            self._player = self._red

    def current_turn_string(self):
        return '%s\'s turn' % (self._player)

    def _all_squares(self):
        start = NUM_COL * NUM_ROW -1
        return range(start,-1,-1)

    def _check_winner(self):
        for index in self._all_squares():
            if self._board[index] == self._player:
                self._check_index_winner(index)
                
    def _check_index_winner(self, index):
        for direction in DIRECTIONS:               
            for distance in range(4):
                if self._board[index + direction*distance] != self._board[index]:
                    break
            else:
                self._winner = self._board[index]
