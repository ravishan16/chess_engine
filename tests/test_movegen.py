import unittest
from engine.board import Board
from engine.movegen import MoveGenerator
from engine.constants import *

class TestMoveGenerator(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.movegen = MoveGenerator(self.board)
        
    def test_initial_moves(self):
        moves = self.movegen.generate_moves()
        # In initial position, there should be 20 legal moves
        self.assertEqual(len(moves), 20)
        
    def test_pawn_moves(self):
        # Test single pawn push
        self.board = Board()
        moves = self.movegen.generate_pawn_moves(81)  # e2
        single_push = (81, 61, 0)  # e2-e4
        self.assertIn(single_push, moves)
        
        # Test pawn capture
        self.board.board[62] = PAWN
        self.board.color[62] = BLACK
        moves = self.movegen.generate_pawn_moves(81)
        capture = (81, 62, 0)
        self.assertIn(capture, moves)
        
    def test_knight_moves(self):
        moves = self.movegen.generate_knight_moves(22)  # Nb1
        self.assertEqual(len(moves), 2)  # Only Na3 and Nc3 possible
        
    def test_bishop_moves(self):
        # Clear some squares
        self.board.board[73] = EMPTY  # Clear f2
        self.board.board[74] = EMPTY  # Clear g2
        moves = self.movegen.generate_bishop_moves(23)  # c1
        self.assertTrue(len(moves) > 0)
        
    def test_rook_moves(self):
        # Clear some squares
        self.board.board[81] = EMPTY  # Clear e2
        moves = self.movegen.generate_rook_moves(21)  # a1
        self.assertTrue(len(moves) > 0)
        
    def test_queen_moves(self):
        # Clear some squares
        self.board.board[82] = EMPTY  # Clear f2
        moves = self.movegen.generate_queen_moves(24)  # d1
        self.assertTrue(len(moves) > 0)
        
    def test_king_moves(self):
        # Test normal king moves
        self.board.board[82] = EMPTY
        moves = self.movegen.generate_king_moves(25)  # e1
        self.assertTrue(len(moves) > 0)
        
        # Test castling
        self.board.board[26] = EMPTY
        self.board.board[27] = EMPTY
        moves = self.movegen.generate_king_moves(25)
        castle_kingside = (25, 27, 0)
        self.assertIn(castle_kingside, moves)
