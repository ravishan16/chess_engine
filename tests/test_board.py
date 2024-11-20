import unittest
from engine.board import Board
from engine.constants import *

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        
    def test_initial_position(self):
        # Test initial piece placement
        self.assertEqual(self.board.board[21], ROOK)
        self.assertEqual(self.board.board[28], ROOK)
        self.assertEqual(self.board.board[95], ROOK)
        self.assertEqual(self.board.board[98], ROOK)
        
        # Test colors
        self.assertEqual(self.board.color[21], BLACK)
        self.assertEqual(self.board.color[95], WHITE)
        
    def test_make_move(self):
        # Test pawn move
        self.board.make_move((81, 61, 0))  # e2-e4
        self.assertEqual(self.board.board[61], PAWN)
        self.assertEqual(self.board.board[81], EMPTY)
        
        # Test capture
        self.board.board[41] = PAWN
        self.board.color[41] = BLACK
        self.board.make_move((61, 41, 0))  # e4xe5
        self.assertEqual(self.board.board[41], PAWN)
        self.assertEqual(self.board.color[41], WHITE)
        
    def test_castling(self):
        # Setup castling position
        self.board.board[25] = EMPTY  # f1
        self.board.board[26] = EMPTY  # g1
        self.board.make_move((24, 26, 0))  # O-O
        self.assertEqual(self.board.board[26], KING)
        self.assertEqual(self.board.board[25], ROOK)
        
    def test_en_passant(self):
        # Setup en passant position
        self.board.make_move((81, 61, 0))  # e2-e4
        self.board.make_move((31, 51, 0))  # e7-e5
        self.assertEqual(self.board.ep_square, 51)
