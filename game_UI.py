import turtle, math
from game import *
NUM_SQUARES = 8 # The number of squares on each row.
SQUARE = 50 # The size of each square in the checkerboard.
SQUARE_COLORS = ("light gray", "white")
PIECE_COLOR = ("BLACK", "RED")
BOARD_SIZE = NUM_SQUARES * SQUARE
CORNER = -BOARD_SIZE / 2
ROW = 3 # Three row for each play's pieces
BLACK = 1
RED = 2
BLACK_KING = 3
RED_KING = 4
MOVED = False
class Game_UI():
    '''
        class Game_UI
        Attributes:
            turtle -- 
            game --
            board --
            init_board() --
        Method:
            init_board
    '''
    def __init__(self, game):
        self.turtle = turtle
        self.game = game
        self.board = self.game.board
        self.init_board()
    def init_board(self):
        '''
            Function init_board:
                This function will draw the initial board
            Parameters:
                self -- current game_UI object
            Returns:
                None. Draw the game by turtle
        '''
        self.window_size = BOARD_SIZE + SQUARE # The extra + SQUARE is the margin
        self.turtle.setup(self.window_size, self.window_size)
        print(self.board)
        # Set the drawing canvas size. The should be actual board size
        self.turtle.screensize(BOARD_SIZE, BOARD_SIZE)
        self.turtle.bgcolor("white") # The window's background color
        self.turtle.tracer(0, 0) # makes the drawing appear immediately
        self.pen = turtle.Turtle()
        self.pen.penup()
        self.update_board()
        self.piece_selected = False
        self.clicked_at = {"row" : 0, "col" : 0, "piece" : None}
        screen = turtle.Screen()
        screen.onclick(self.click_handler) # This will call call the click_handler function when a click occurs
        self.turtle.done() # Stops the window from closing.


    def update_board(self):
        '''
            Method update_board
        '''
        board = self.game.board
        for i in range(len(board)):
            for j in range(len(board)):
                if (board[i][j] == 0):
                    self.draw_square(self.pen, "black", SQUARE, i, j)
                else:
                    self.draw_square(self.pen, "black", SQUARE, i, j)
                    self.draw_piece(self.pen, "black", i, j)
    def draw_square(self, a_turtle, color, size, x, y):
        '''
            Method -- draw_square
                Draw a square of a given size and its row and col index given.
            Parameters:
                a_turtle -- an instance of Turtle
                size -- the length of each side of the square
                x -- row index of the BOARD
                y -- col index of the BOARD
            Returns:
                Nothing. Draws a square on the graphics window. (On the Board)
        '''
        a_turtle.color(color, self.get_back_ground_color(x, y))
        pos = self.convert_index_to_coordinates(x , y)
        pos_x = pos[0]
        pos_y = pos[1]
        a_turtle.setposition(pos_x, pos_y)
        RIGHT_ANGLE = 90
        a_turtle.pendown()
        a_turtle.begin_fill()
        for i in range(4):
            a_turtle.forward(size)
            a_turtle.left(RIGHT_ANGLE)
        a_turtle.end_fill()
        a_turtle.penup()
    

    def convert_index_to_coordinates(self, x, y):
        '''
            Method convert_index_to_coordinates:
                This method 
            Parameters:
                self --
                x --
                y --
            Returns:
                a list contains row and col index.
        '''
        y_pos = CORNER + x * SQUARE
        x_pos = CORNER + y * SQUARE
        return [x_pos, y_pos]


    def convert_coordinates_to_index(self, x, y):
        if (x >= CORNER and x <= -CORNER) and (y >= CORNER and y <= -CORNER):
            return [math.floor(y / 50) + 4, math.floor(x / 50) + 4]
        else:
            return []


    def get_back_ground_color(self, x,y):
        '''
            Function get_back_ground_color:
                This Function will return the back ground color from given
                x and y position
            Parameters:
                x -- row index for current piece
                y -- col index for current piece
            Returns:
                The back ground color at current position
        '''
        if (x + y) % 2 == 1:
            return "light grey"
        else:
            return "white"
    

    def draw_piece(self, a_turtle, color, x, y):
        y_pos = CORNER + x * SQUARE
        x_pos = CORNER + y * SQUARE
        x_pos += SQUARE / 2
        a_turtle.setposition(x_pos, y_pos)
        if (self.board[x][y] == BLACK or self.game.board[x][y] == BLACK_KING):
            a_turtle.color(color, "black")
        elif self.board[x][y] == RED or self.game.board[x][y] == RED_KING:
            a_turtle.color(color, "red")
        self.draw_circle(a_turtle, SQUARE / 2)
        if self.game.board[x][y] == BLACK_KING:
            y_pos += SQUARE / 4
            a_turtle.setposition(x_pos, y_pos)
            a_turtle.color("gold", "black")
            self.draw_circle(a_turtle, SQUARE / 4)
        if self.game.board[x][y] == RED_KING:
            y_pos += SQUARE / 4
            a_turtle.setposition(x_pos, y_pos)
            a_turtle.color("gold", "red")
            self.draw_circle(a_turtle, SQUARE / 4)

    def draw_circle(self, a_turtle, radius):
        '''
            Function -- draw_circle
                This Function will draw a circle and fill with the color that come
                with turtle's color
            Parameter:
                a_turtle -- an instance of Turtle
                radius -- radius of the circle
            Returns:
                None. Draw a circle and fill the color on the graphic window
        '''
        a_turtle.pendown()
        a_turtle.begin_fill()
        a_turtle.circle(radius)
        a_turtle.end_fill()
        a_turtle.penup()
    

    def highlight(self, x, y):
        poten_move = self.potential_move(x, y)
        if (self.game.board[x][y] == 0):
            self.draw_square(self.pen, "red", SQUARE, x, y)
        else:
            self.draw_piece(self.pen, "blue", x, y)
            for pos in poten_move:
                pos_x = pos[0]
                pos_y = pos[1]
                self.draw_square(self.pen, "red", SQUARE, pos_x, pos_y)

    def unhighlight(self, x, y):
        poten_move = self.potential_move(x, y)
        if (self.game.board[x][y] == 0):
            self.draw_square(self.pen, "black", SQUARE, x, y)
        else:
            self.draw_piece(self.pen, "black", x, y)
            for pos in poten_move:
                pos_x = pos[0]
                pos_y = pos[1]
                self.draw_square(self.pen, "black", SQUARE, pos_x, pos_y)

    def potential_move(self, x, y):
        reg_move = []
        cap_move = []
        reg_dir = [[1, -1], [1, 1], [-1, -1], [-1, 1]]
        cap_dir = [[2, -2], [2, 2], [-2, -2], [-2, 2]]
        potentials = self.game.possible_move()
        for potential in potentials:
            for reg in reg_dir:
                new_x = x + reg[0]
                new_y = y + reg[1]
                if x == potential[0] and y == potential[1] and\
                    new_x == potential[2] and new_y == potential[3]:
                    reg_move.append([new_x, new_y])
            for cap in cap_dir:
                new_x = x + cap[0]
                new_y = y + cap[1]
                if x == potential[0] and y == potential[1] and\
                    new_x == potential[2] and new_y == potential[3]:
                    cap_move.append([new_x, new_y])
        if cap_move:
            return cap_move
        else:
            return reg_move




    def click_handler(self, x, y):
        '''
            Function -- click_handler
                Called when a click occurs.
            Parameters:
                x -- X coordinate of the click. Automatically provided by Turtle.
                y -- Y coordinate of the click. Automatically provided by Turtle.
            Returns:
                Does not and should not return. Click handlers are a special type
                of function automatically called by Turtle. You will not have
                access to anything returned by this function.
        '''
        pos = self.convert_coordinates_to_index(x, y)
        if (len(pos) != 0):
            print("Clicked at ", math.floor(y / 50) + 4, math.floor(x / 50) + 4)
        else:
            print("invalid click")
            return
        if not self.piece_selected:
            # if current clicked position is current player's piece, save to
            # clicked_at data
            if self.board[pos[0]][pos[1]] == self.game.player_turn or\
                self.board[pos[0]][pos[1]] == self.game.player_turn + 2:
                self.clicked_at["row"] = pos[0]
                self.clicked_at["col"] = pos[1]
                self.highlight(pos[0], pos[1])
                self.piece_selected = True
        else:
            old_x = self.clicked_at["row"]
            old_y = self.clicked_at["col"]
            print("{} of{} ", old_x, old_y)
            print(self.game.possible_move())
            self.unhighlight(old_x, old_y)
            self.game.move(old_x, old_y, pos[0], pos[1])
            # if there is capture move availble, keep the user's turn until
            # if move was successful, update board on UI
            if (self.game.move_success):
                # clear the square if check move is made
                print(abs(pos[0] - old_x))
                if abs(pos[0] - old_x) == 2:
                    self.draw_square(self.pen, "black", SQUARE,\
                        (old_x + pos[0]) // 2, (old_y + pos[1]) // 2)
                    print((old_x + pos[0]) // 2, (old_y + pos[1]) // 2)
                self.draw_square(self.pen, "black", SQUARE, old_x, old_y)
                self.draw_square(self.pen, "black", SQUARE, pos[0], pos[1])
                self.draw_piece(self.pen, "black", pos[0], pos[1])
                if not self.game.possible_capture_move:
                    self.game.switch_turn()
                print(self.game.player_turn)
            self.piece_selected = False




def main():
    GAME()

if __name__ == "__main__":
    main()