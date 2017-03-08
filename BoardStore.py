from connect4 import FourInARowBoard

class BoardStore(object):
    def __init__(self):
        self.boards = {}
        self.index = 0

    def latest_board(self):
        return self.boards[self.index]

    def join_game(self, username):
        colour = 'yellow'
        if self.index ==0 or self.boards[self.index].has_both_players():
            self.generate_new_board(username)
            colour = 'red'
        else:
            self.latest_board().set_second_player(username)
        return self.index, colour

    def generate_new_board(self, username):
        self.index += 1
        board = FourInARowBoard()
        board.set_first_player(username)
        self.boards[self.index] = board

    def get_board(self, index):
        return self.boards[index]