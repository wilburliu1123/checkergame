'''
Wilbur Liu
CS5001 FALL 2020
Project
Class game
This class is to create a game board and its pieces that represent different
state of the game. State of the game will be used to evaluate wether user has
won or not. There will also be functions that determine if a move is valid
or not.
'''
NUM_SQUARES = 8  # The number of squares on each row.
ROW = 3  # we need three rows of pieces for each player
PIECE_COLORS = ("king", "black", "red")
BLACK = 1
RED = 2
BLACK_KING = 3
RED_KING = 4


class GAME():

    def __init__(self):
        '''
            Constructor -- creates a new game board for
                future operation (draw pieces, validate move, etc.)
            Attributes:
                self -- current game object
                board -- 8X8 matrix that represent checker board
                playerturn -- Represent whose turn on current game
                black_piece -- number of black piece in current game
                red_piece -- number of red piece in current game
                move_success -- True if player successfully moved the piece
            Returns:
                No returns since we are initializing game board for this game
        '''
        self.board = self.init_board()
        self.player_turn = BLACK
        self.black_piece = 12
        self.red_piece = 12
        self.move_success = False
        self.possible_capture_move = False

    def init_board(self):
        '''
            Function init_board:
                This function will initialize the game board
            Parameters:
                self -- current game object
            Returns:
                an initialized game board
        '''
        board = []
        for i in range(NUM_SQUARES):
            cur_row = []
            for j in range(NUM_SQUARES):
                if (i < ROW and (i+j) % 2 == 1):
                    cur_row.append(BLACK)
                elif (i >= NUM_SQUARES - ROW) and (i+j) % 2 == 1:
                    cur_row.append(RED)
                else:
                    cur_row.append(0)
            board.append(cur_row)
        return board

    def switch_turn(self):
        '''
            Function switch_turn
                This function will change turns based on current state. If
                Player is playing black piece and finished move, switch to red
                Vise versa.
            Parameters:
                self -- self is pointing to current game object
            Returns:
                None. Change the player_turn attribute for current game object
        '''
        if (self.player_turn == BLACK):
            self.player_turn = RED
        else:
            self.player_turn = BLACK

    def player_can_continue(self):
        '''
            Function player_can_continue:
                This function will return true if current player has potential
                move available. False otherwise
            Parameters:
                self -- current game obejct
            Returns:
                Ture if current player still has moves available
                False if no moves available for current player
        '''
        potential_move = self.possible_move()
        if (len(potential_move) == 0):
            return False
        else:
            return True

    def get_player_turn(self):
        '''
            Function get_player_turn:
                This function will return who turn is it for current game
            Parameters:
                self -- current game
            Returns:
                player turn for current game
        '''
        return self.player_turn

    def move(self, old_x, old_y, x, y):
        '''
            Function move:
                This function will move piece from old position to new position
                and update the board
            Parameters:
                self -- current game object
                old_x -- current row index
                old_y -- current col index
                x -- destination row index
                y -- destination col index
            Returns:
                None. Update the game board
        '''
        if not self.is_valid_move(old_x, old_y, x, y):
            self.move_success = False
            return
        if not [old_x, old_y, x, y] in self.possible_move():
            print("not possible move: " + str([old_x, old_y, x, y]))
            self.move_success = False
            return
        self.board[x][y] = self.board[old_x][old_y]
        self.board[old_x][old_y] = 0
        # check if it is king upgrade
        if x == NUM_SQUARES-1 and self.board[x][y] == BLACK:
            self.board[x][y] = BLACK_KING
        if x == 0 and self.board[x][y] == RED:
            self.board[x][y] = RED_KING
        self.move_success = True
        # if it is a capture move, remove captured piece
        if abs(x - old_x) == 2:
            piece = self.board[(old_x + x) // 2][(old_y + y) // 2]
            self.board[(old_x + x) // 2][(old_y + y) // 2] = 0
            if piece == BLACK or piece == BLACK_KING:
                self.black_piece -= 1
            elif piece == RED or piece == RED_KING:
                self.red_piece -= 1
            self.check_possible_capture_move(x, y)

    def check_possible_capture_move(self, x, y):
        '''
            Method check_possible_capture_move:
                This method will check giving x and y position on the board,
                if there is another capture_move possible, then it will return
                the possible capture move.
            Paramerters:
                self -- current game object
                x -- x position of current piece
                y -- y position of current piece
            Returns:
                A list of possible move of current piece, [] if there is no
                capture move possible
        '''
        black_cap_dir = [[2, -2], [2, 2]]
        red_cap_dir = [[-2, -2], [-2, 2]]
        cap_move = []
        if self.board[x][y] == BLACK_KING:
            black_cap_dir.append(red_cap_dir[0])
            black_cap_dir.append(red_cap_dir[1])
        if self.board[x][y] == RED_KING:
            red_cap_dir.append(black_cap_dir[0])
            red_cap_dir.append(black_cap_dir[1])
        if self.board[x][y] == BLACK or self.board[x][y] == BLACK_KING:
            for dir in black_cap_dir:
                if (self.is_valid_move(x, y, x + dir[0], y + dir[1])):
                    cap_move.append([x, y, x + dir[0], y + dir[1]])
        if self.board[x][y] == RED or self.board[x][y] == RED_KING:
            for dir in red_cap_dir:
                if (self.is_valid_move(x, y, x + dir[0], y + dir[1])):
                    cap_move.append([x, y, x + dir[0], y + dir[1]])
        if cap_move:
            self.possible_capture_move = True
        else:
            self.possible_capture_move = False
        return cap_move

    def possible_move(self):
        '''
            Function possible_move:
                This function will return a list of all possible move from
                from current player
            Parameters:
                self -- current game board
            Returns:
                return a list of all possible moves for current player
        '''
        positions = self.get_pieces_pos()
        if (len(positions) == 0):
            return []
        if self.player_turn == BLACK:
            reg_direction = [[1, -1], [1, 1]]
            capture_direction = [[2, -2], [2, 2]]
        else:
            reg_direction = [[-1, -1], [-1, 1]]
            capture_direction = [[-2, -2], [-2, 2]]
        reg_moves = []
        capture_moves = []
        for pos in positions:
            pos_x = pos[0]
            pos_y = pos[1]
            # if it is a black king or red king, append additional moves
            if self.board[pos_x][pos_y] == BLACK_KING:
                reg_direction.append([-1, -1])
                reg_direction.append([-1, 1])
                capture_direction.append([-2, -2])
                capture_direction.append([-2, 2])
            if self.board[pos_x][pos_y] == RED_KING:
                reg_direction.append([1, -1])
                reg_direction.append([1, 1])
                capture_direction.append([2, -2])
                capture_direction.append([2, 2])
            for dir in reg_direction:
                if self.is_valid_move(pos_x, pos_y, pos_x+dir[0],
                                      pos_y+dir[1]):
                    reg_moves.append([pos_x, pos_y,
                                      pos_x+dir[0], pos_y+dir[1]])
            for dir in capture_direction:
                if self.is_valid_move(pos_x, pos_y, pos_x+dir[0],
                                      pos_y+dir[1]):
                    capture_moves.append([pos_x, pos_y, pos_x+dir[0],
                                          pos_y + dir[1]])
        if capture_moves:
            print("A capture is possible, and it must be made!")
            print("capture_moves:")
            for cap_move in capture_moves:
                print("from [{},{}], to [{},{}]: ".format(
                    cap_move[0], cap_move[1], cap_move[2], cap_move[3]))
            self.possible_capture_move = True
            return capture_moves
        else:
            print("reg_moves:")
            for reg_move in reg_moves:
                print("from [{},{}], to [{},{}]: ".format(
                    reg_move[0], reg_move[1], reg_move[2], reg_move[3]))
            self.possible_capture_move = False
            return reg_moves

    def is_valid_move(self, old_x, old_y, x, y):
        '''
            Method is_valid_move:
                This method is to check given current position of a piece,
                check wether the future position (x and y) is a valid move
            Paramters:
                self -- current game object
                old_x -- current x position of the piece
                old_y -- current y position of the piece
                x -- x position where the piece is going
                y -- y position where the piece is going
            Returns:
                True if the piece can move to the position. False otherwise
        '''
        dir_x = x - old_x
        dir_y = y - old_y
        if (x < 0 or x > NUM_SQUARES-1) or (y < 0 or y > NUM_SQUARES - 1):
            return False
        if self.board[x][y] != 0:
            return False
        # if it is regular move
        if dir_x == 1:
            return (self.board[old_x][old_y] == BLACK or
                    self.board[old_x][old_y] == BLACK_KING or
                    self.board[old_x][old_y] == RED_KING) and abs(dir_y) == 1
        if dir_x == -1:
            return (self.board[old_x][old_y] == RED or
                    self.board[old_x][old_y] == RED_KING or
                    self.board[old_x][old_y] == BLACK_KING) and abs(dir_y) == 1
        # if it is a capture move, check if it is a valid capture move
        elif dir_x == 2:
            # upward capture move, if it is a red king, check if it is valid
            if self.board[old_x][old_y] == RED_KING:
                return (dir_y == -2 and
                        self.board[old_x + 1][old_y - 1] == BLACK)\
                    or (dir_y == 2 and
                        self.board[old_x + 1][old_y + 1] == BLACK)\
                    or (dir_y == -2 and
                        self.board[old_x + 1][old_y - 1] == BLACK_KING)\
                    or (dir_y == 2 and
                        self.board[old_x + 1][old_y + 1] == BLACK_KING)
            # else, it is a regular black capture move, check if it is valid
            elif self.board[old_x][old_y] == BLACK_KING or \
                    self.board[old_x][old_y] == BLACK:
                return (dir_y == -2 and
                        self.board[old_x + 1][old_y - 1] == RED) or\
                        (dir_y == 2 and
                            self.board[old_x + 1][old_y + 1] == RED) or\
                        (dir_y == -2 and
                            self.board[old_x + 1][old_y - 1] == RED_KING) or\
                        (dir_y == 2 and
                            self.board[old_x + 1][old_y + 1] == RED_KING)
        # if it is a downward capture move, check if it is a valid one
        elif dir_x == -2:
            # if it is a black king, check if it is valid
            if self.board[old_x][old_y] == BLACK_KING:
                return (dir_y == -2 and
                        self.board[old_x - 1][old_y - 1] == RED) or\
                        (dir_y == 2 and
                            self.board[old_x - 1][old_y + 1] == RED) or\
                        (dir_y == -2 and
                            self.board[old_x-1][old_y-1] == RED_KING) or\
                        (dir_y == 2 and
                            self.board[old_x-1][old_y+1] == RED_KING)
            # if it is a reg red capture move, check if it is valid
            elif self.board[old_x][old_y] == RED_KING or\
                    self.board[old_x][old_y] == RED:
                return (dir_y == -2 and
                        self.board[old_x - 1][old_y - 1] == BLACK) or\
                        (dir_y == 2 and
                            self.board[old_x-1][old_y+1] == BLACK) or\
                        (dir_y == -2 and
                            self.board[old_x-1][old_y-1] == BLACK_KING) or\
                        (dir_y == 2 and
                            self.board[old_x-1][old_y+1] == BLACK_KING)
        else:
            return False

    def get_pieces_pos(self):
        '''
            Method get_pieces_pos:
                This method is to get all current play's piece and return x y
                position as a list
            Parameters:
                self -- current game object
            Returns:
                A list of current piece position
        '''
        value = self.player_turn
        if (value == BLACK):
            King = BLACK_KING
        else:
            King = RED_KING
        pos = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == value or self.board[i][j] == King:
                    pos.append([i, j])
        return pos
