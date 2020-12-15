import turtle
import math
from game import *
import random
NUM_SQUARES = 8  # The number of squares on each row.
SQUARE = 50  # The size of each square in the checkerboard.
SQUARE_COLORS = ("light gray", "white")
PIECE_COLOR = ("BLACK", "RED")
BOARD_SIZE = NUM_SQUARES * SQUARE
CORNER = -BOARD_SIZE / 2
ROW = 3  # Three row for each play's pieces
BLACK = 1
RED = 2
BLACK_KING = 3
RED_KING = 4
MOVED = False


class Game_UI():
    '''
        class Game_UI
        Attributes:
            turtle -- turtle object that will draw the game UI
            game -- game object that perform all calculation and moves
            board -- a 8x8 matrix that represent the game board
            init_board() -- initialize the board when game starts
    '''
    def __init__(self):
        self.turtle = turtle
        self.game = GAME()
        self.board = self.game.board
        self.game_over = False
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
        # The extra + SQUARE is the margin
        self.window_size = BOARD_SIZE + SQUARE
        self.turtle.setup(self.window_size, self.window_size)
        # Set the drawing canvas size. The should be actual board size
        self.turtle.screensize(BOARD_SIZE, BOARD_SIZE)
        self.turtle.bgcolor("white")  # The window's background color
        self.turtle.tracer(0, 0)  # makes the drawing appear immediately
        self.pen = turtle.Turtle()
        self.pen.penup()
        self.update_board()
        self.piece_selected = False
        self.clicked_at = {"row": 0, "col": 0, "piece": None}
        self.screen = turtle.Screen()
        # This will call call the click_handler function when a click occurs
        self.screen.onclick(self.click_handler)
        self.turtle.done()  # Stops the window from closing.

    def update_board(self):
        '''
            Method update_board:
                This method will draw all square and piece on the board when
                initialization happens
            Parameters:
                self -- current game UI object
            Returns:
                None. Draw squares and pieces on the game board
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
        pos = self.convert_index_to_coordinates(x, y)
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
                This method convert row and column index to x and y coordinates
                on the game canvas, which helps turtle object to draw stuff
                (update the game UI)
            Parameters:
                self -- current game UI object
                x -- row index of current clicked position
                y -- column index of current clicked position
            Returns:
                a list contains x and y coordinates.
        '''
        y_pos = CORNER + x * SQUARE
        x_pos = CORNER + y * SQUARE
        return [x_pos, y_pos]

    def convert_coordinates_to_index(self, x, y):
        '''
            Method convert_coordinates_to_index:
                This method convert x and y coordinates from click handler to
                row and column indexes for the game board
            Parameters:
                self -- current game UI object
                x -- x coordinates passed by another function
                y -- y coordinates passed by another function
            Returns:
                Return a list containing row and column index for this game
                board. In a form [x, y]
        '''
        if (x >= CORNER and x <= -CORNER) and (y >= CORNER and y <= -CORNER):
            return [math.floor(y / 50) + 4, math.floor(x / 50) + 4]
        else:
            return []

    def get_back_ground_color(self, x, y):
        '''
            Function get_back_ground_color:
                This Function will return the back ground color of the squre
                from given x and y position
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
        '''
            Method draw_piece:
                This method draw a piece based on its x, y position and its
                value. If it is a red piece, it will fill the piece with red
                color. If it is a black piece, it will fill the piece with
                black color
            Parameters:
                self -- current game UI object
                a_turtle -- turtle object that is being used to draw this piece
                color -- color for the perimeter of the circle.
                x -- x position of this piece
                y -- y position of this piece
        '''
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
                This Function will draw a circle and fill with the color that
                come with turtle's color
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
        '''
            Method highlight:
                This method highlight the selected piece and its potential
                move
            Parameters:
                self -- current gameUI object
                x -- x position of selected piece
                y -- y position of selected piece
            Returns:
                None. Only update game UI and won't return anything
        '''
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
        '''
            Method unhighlight:
                This method unhighlight the piece and its potential move when
                player clicked somewhere else.
            Parameters:
                self -- current gameUI object
                x -- x position of current clicked position
                y -- y position of current clicked position
            Returns:
                None. Only update the game UI. Won't return anything
        '''
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
        '''
            Method potential_move:
                This method returns potential moves for current piece selected
                by player
            Parameters:
                self -- current gameUI object
                x -- x position of current selected piece
                y -- y position of current selected piece
            Returns:
                Returns a list of potential move for current selected piece
                if capture move is possible, only return the capture moves
        '''
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

    def computer_move(self):
        '''
            Method computer_move:
                This method let computer to move red piece by randomly select
                current available moves.
            Parameters:
                self -- current gameUI
            Returns:
                A list contains current x,y position of piece it selected and
                future x, y positions where it want the piece to move to.
        '''
        if (self.game.player_turn == RED):
            # make random move from possible_move
            cur_possible_move = self.game.possible_move()
            if (len(cur_possible_move) == 0):
                return []
            random_select = random.randrange(len(cur_possible_move))
            return cur_possible_move[random_select]
        else:
            return []

    def click_handler(self, x, y):
        '''
            Function -- click_handler
                Called when a click occurs.
            Parameters:
                x -- X coordinate of the click.
                    Automatically provided by Turtle.
                y -- Y coordinate of the click.
                    Automatically provided by Turtle.
            Returns:
                Does not and should not return. Click handlers are a special
                type of function automatically called by Turtle. You will not
                have access to anything returned by this function.
        '''
        if self.game_over:
            return
        pos = self.convert_coordinates_to_index(x, y)
        if (len(pos) == 0):
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
            self.unhighlight(old_x, old_y)
            self.game.move(old_x, old_y, pos[0], pos[1])
            # if there is capture move availble, keep the user's turn until
            # if move was successful, update board on UI
            if (self.game.move_success):
                # clear the square if check move is made
                self.update_move(old_x, old_y, pos[0], pos[1])
                if not self.game.possible_capture_move:
                    self.game.switch_turn()
            self.piece_selected = False
        while (self.game.player_turn == RED):
            computer_choice = self.computer_move()
            if len(computer_choice) == 0:
                self.game.switch_turn()
                if (self.game.red_piece != 0):
                    self.write_try_again()
                    print("Game over. Try again")
                self.game_over = True
                break
            self.game.move(computer_choice[0], computer_choice[1],
                           computer_choice[2], computer_choice[3])
            self.update_move(computer_choice[0], computer_choice[1],
                             computer_choice[2], computer_choice[3])
            if not self.game.possible_capture_move:
                self.game.switch_turn()
        print("red piece left:" + str(self.game.red_piece))
        print("black piece left: " + str(self.game.black_piece))
        if self.game.red_piece == 0:
            self.write_win()
            print("Game Over, You win!")
            self.game_over = True
        elif self.game.black_piece == 0:
            self.write_lose()
            print("Game Over, You lose!")
            self.game_over = True
        elif (not self.game.player_can_continue()):
            self.write_try_again()
            print("Game Over, try again!")
            self.game_over = True
        return

    def write_lose(self):
        '''
            Method write_lose:
                This method write losing message on the board when game is
                over.
            Parameters:
                self -- current gameUI object
            Returns:
                None. Drawing message on the board
        '''
        self.pen.color("purple")
        pos = self.convert_index_to_coordinates(5, 1)
        pos_x = pos[0]
        pos_y = pos[1]
        self.pen.setposition(pos_x, pos_y)
        style = ('Courier', 50, 'italic')
        self.pen.write('Game Over!', font=style)
        pos = self.convert_index_to_coordinates(3, 2)
        pos_x = pos[0]
        pos_y = pos[1]
        self.pen.setposition(pos_x, pos_y)
        self.pen.write('You lose!', font=style)

    def write_win(self):
        '''
            Method write_win:
                This method write winning message on the board when game is
                over.
            Parameters:
                self -- current gameUI object
            Returns:
                None. Drawing message on the board
        '''
        self.pen.color("purple")
        pos = self.convert_index_to_coordinates(5, 1)
        pos_x = pos[0]
        pos_y = pos[1]
        self.pen.setposition(pos_x, pos_y)
        style = ('Courier', 50, 'italic')
        self.pen.write('Game Over!', font=style)
        pos = self.convert_index_to_coordinates(3, 2)
        pos_x = pos[0]
        pos_y = pos[1]
        self.pen.setposition(pos_x, pos_y)
        self.pen.write('You win!', font=style)

    def write_try_again(self):
        '''
            Method write_try_again:
                This method write try again message on the board when game is
                over.
            Parameters:
                self -- current gameUI object
            Returns:
                None. Drawing message on the board
        '''
        self.pen.color("purple")
        pos = self.convert_index_to_coordinates(5, 1)
        pos_x = pos[0]
        pos_y = pos[1]
        self.pen.setposition(pos_x, pos_y)
        style = ('Courier', 50, 'italic')
        self.pen.write('Game Over!', font=style)
        pos = self.convert_index_to_coordinates(3, 2)
        pos_x = pos[0]
        pos_y = pos[1]
        self.pen.setposition(pos_x, pos_y)
        self.pen.write('Try Again!', font=style)

    def update_move(self, old_x, old_y, x, y):
        '''
            Method update_move:
                This method update the board on UI after user has made a move
            Parameters:
                self -- current gameUI object
                old_x -- current piece x position
                old_y -- cuurent piece y position
                x -- x position where this piece is moving to
                y -- y position where this piece is moving to
            Returns:
                None. Update the move on the board
        '''
        if abs(x - old_x) == 2:
            self.draw_square(self.pen, "black", SQUARE,
                             (old_x + x) // 2, (old_y + y) // 2)
        self.draw_square(self.pen, "black", SQUARE, old_x, old_y)
        self.draw_square(self.pen, "black", SQUARE, x, y)
        self.draw_piece(self.pen, "black", x, y)
