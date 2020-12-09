from game import *

def test_constructor():
    game = GAME()
    assert(game.board[7][0] == RED)
    assert(game.board[7][2] == RED)
    assert(game.board[7][4] == RED)
    assert(game.board[7][6] == RED)
    assert(game.board[7][0] == RED)
    assert(game.board[0][1] == BLACK)
    assert(game.board[0][3] == BLACK)
    assert(game.board[0][5] == BLACK)
    assert(game.board[0][7] == BLACK)
    assert(game.black_piece == 12)
    assert(game.red_piece == 12)
    assert(game.player_turn == BLACK)
    assert(not game.move_success)


def test_switch_turn():
    game = GAME()
    assert(game.player_turn == BLACK)
    game.switch_turn()
    assert(game.player_turn == RED)

def test_get_player_turn():
    game = GAME()
    assert(game.get_player_turn() == BLACK)
    game.switch_turn()
    assert(game.get_player_turn() == RED)

def test_player_can_continue():
    game = GAME()
    game.board = [
                [2, 0, 0, 0, 0, 2, 0, 0],
                [0, 0, 0, 0, 0, 0, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 2, 0],
                [0, 0, 0, 0, 0, 2, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    print(game.board)
    if (game.player_turn == BLACK):
        print("BLACK")
    print(game.possible_move())
    assert(game.player_can_continue() is False)
    game.board = [
                [2, 0, 0, 0, 0, 2, 0, 0],
                [0, 0, 0, 0, 0, 0, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    assert(game.player_can_continue())
    assert(game.possible_capture_move)


def test_move():
    game = GAME()
    game.board = [
                [2, 0, 0, 0, 0, 2, 0, 0],
                [0, 0, 0, 0, 0, 0, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    game.move(2,7,4,5)
    assert(game.board[4][5] == 1)
    assert(game.board[3][6] == 0)
    assert(game.move_success)
    game.switch_turn()


def test_possible_move():
    game = GAME()
    game.board = [
                [2, 0, 0, 0, 0, 2, 0, 0],
                [0, 0, 0, 0, 0, 0, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    assert(len(game.possible_move()) == 1)
    assert(game.possible_capture_move)

def test_is_valid_move():
    game = GAME()
    game.board = [
                [2, 0, 0, 0, 0, 2, 0, 0],
                [0, 0, 0, 0, 0, 0, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    assert(not game.is_valid_move(0,0,1,1))
    assert(game.is_valid_move(2,7,4,5))
    game.switch_turn()
    assert(not game.is_valid_move(1,6,2,7))


def test_get_pieces_pos():
    game = GAME()
    game.board =  [
                [2, 0, 0, 0, 0, 2, 0, 0],
                [0, 0, 0, 0, 0, 0, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 2, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    assert(game.get_pieces_pos() == [[2,7]])
    game.switch_turn()
    assert(game.get_pieces_pos() == [[0,0], [0,5], [1,6], [3,6]])


def test_king_upgrade():
    game = GAME()
    game.board =  [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    game.move(6,6,7,7)
    assert(game.board[7][7] == BLACK_KING)
    game.switch_turn()
    game.board =  [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 2, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    game.move(1,5,0,6)
    assert(game.board[0][6] == RED_KING)