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
from game_UI import *
NUM_SQUARES = 8 # The number of squares on each row.
ROW = 3 # we need three rows of pieces for each player
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
        self.UI = Game_UI(self)


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
    
    def game_over(self):
        if self.black_piece == 0 or self.red_piece == 0:
            return True
        else:
            return self.player_can_continue()

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
    


    def get_board(self):
        '''
            Function get_board:
                This function will return current game board
            Parameters:
                self -- current game object
            Returns:
                returns the game board
        '''
        print(self.board)
        return self.board
    


    

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
        print(old_x, old_y, x, y)
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
            if piece == BLACK:
                self.black_piece -= 1
            elif piece == RED:
                self.red_piece -= 1
            self.possible_move()
    


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
        print(positions)
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
                print(reg_direction)
                if self.is_valid_move(pos_x, pos_y, pos_x+dir[0], pos_y+dir[1]):
                    reg_moves.append([pos_x, pos_y, pos_x+dir[0],pos_y+dir[1]])
            for dir in capture_direction:
                if self.is_valid_move(pos_x, pos_y, pos_x+dir[0], pos_y+dir[1]):
                    capture_moves.append([pos_x, pos_y, pos_x+dir[0], \
                        pos_y + dir[1]])
        if capture_moves:
            print("A capture is possible, and it must be made!")
            print("capture_moves:" + str(capture_moves))
            self.possible_capture_move = True
            return capture_moves
        else:
            print("reg_moves:" + str(reg_moves))
            self.possible_capture_move = False
            return reg_moves

            

    def is_valid_move(self, old_x, old_y, x, y):
        dir_x = x - old_x
        dir_y = y - old_y
        if (x < 0 or x > NUM_SQUARES-1) or (y < 0 or y > NUM_SQUARES - 1):
            return False
        if self.board[x][y] != 0:
            return False
        # if it is regular move
        if dir_x == 1:
            return (self.board[old_x][old_y] == BLACK or\
                self.board[old_x][old_y] == BLACK_KING\
                or self.board[old_x][old_y] == RED_KING) and abs(dir_y) == 1
        if (dir_x == -1):
            return (self.board[old_x][old_y] == RED or\
                self.board[old_x][old_y] == RED_KING\
                or self.board[x][y] == BLACK_KING) and abs(dir_y) == 1
        # if it is a capture move, check if it is a valid capture move
        elif dir_x == 2:
            # upward capture move, if it is a red king, check if it is valid
            if self.board[old_x][old_y] == RED_KING:
                return (dir_y == -2 and\
                    self.board[old_x + 1][old_y - 1] == BLACK)\
                or (dir_y == 2 and self.board[old_x + 1][old_y + 1] == BLACK)
            # else, it is a regular black capture move, check if it is valid
            elif self.board[old_x][old_y] == BLACK_KING or\
                self.board[old_x][old_y] == BLACK:
                return (dir_y == -2 and\
                    self.board[old_x + 1][old_y - 1] == RED) or\
                        (dir_y == 2 and\
                            self.board[old_x + 1][old_y + 1] == RED)
            
        # if it is a downward capture move, check if it is a valid one
        elif dir_x == -2:
            # if it is a black king, check if it is valid
            if self.board[old_x][old_y] == BLACK_KING:
                return (dir_y == -2 and\
                    self.board[old_x - 1][old_y - 1] == RED)\
                or (dir_y == 2 and self.board[old_x - 1][old_y + 1] == RED)
            # if it is a reg red capture move, check if it is valid
            elif self.board[old_x][old_y] == RED_KING or\
                self.board[old_x][old_y] == RED:
                return (dir_y == -2 and\
                    self.board[old_x - 1][old_y - 1] == BLACK) or\
                        (dir_y == 2 and self.board[old_x-1][old_y+1] == BLACK)
        else:
            return False

    def get_pieces_pos(self):
        '''
        '''
        value = self.player_turn
        print(value)
        if (value == BLACK):
            King = BLACK_KING
            print(King)
        else:
            King = RED_KING
        pos = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == value or self.board[i][j] == King:
                    pos.append([i, j])
        return pos

    def is_enemy(self, cur_pos, destination):
        '''
            Function -- is_enemy:
                This function will return true if the row and col index is
                pointing an enemy false otherwise
            Parameters:
                row -- row index
                col -- col index
            Returns:
                True if the row index is pointing at an enemy
                False otherwise
        '''
        x = cur_pos[0]
        y = cur_pos[1]
        des_piece = self.board[destination[0]][destination[1]]
        if (self.board[x][y] == RED) and des_piece == BLACK:
            return True
        elif (self.board[x][y] == BLACK) and des_piece == RED:
            return True
        else:
            return False
    
    # def __str__(self):
    #     '''
    #         Method -- __str__
    #             Creates a string representation of the GAME_BOARD
    #         Parameter:
    #             self -- The current game board object
    #         Returns:
    #             A string representation of the GAME_BOARD.
    #     '''
        
    #     for i in range(len(self.board)):
    #         for j in range(len(len(self.board))):
    #             self.board[i][j] = self.board[i][j].color
    #     return self.board

    


        

def main():
    game = GAME()
    print(game.board)
    print(game.possible_move())

if __name__ == "__main__":
    main()