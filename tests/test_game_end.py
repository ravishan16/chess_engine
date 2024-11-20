import unittest
from engine.board import Board
from engine.movegen import MoveGenerator
from engine.constants import *

class TestGameEnd(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.movegen = MoveGenerator(self.board)
        
    def test_checkmate_scholar(self):
        # Setup Scholar's mate position
        self.board = Board()
        # 1. e4 e5 2. Bc4 Nc6 3. Qh5 Nf6?? 4. Qxf7#
        moves = [
            (81, 61, 0),  # e2-e4
            (31, 51, 0),  # e7-e5
            (83, 56, 0),  # f1-c4
            (22, 43, 0),  # b8-c6
            (84, 45, 0),  # d1-h5
            (27, 46, 0),  # g8-f6
            (45, 37, 0),  # h5xf7
        ]
        
        for move in moves:
            self.board.make_move(move)
            
        # Verify checkmate
        moves = self.movegen.generate_moves()
        self.assertEqual(len(moves), 0)
        
    def test_stalemate(self):
        # Setup stalemate position
        self.board = Board()
        # Clear the board except kings and a queen
        for sq in range(21, 99):
            self.board.board[sq] = EMPTY
            
        # Place pieces for stalemate
        self.board.board[21] = KING  # Black king at a8
        self.board.board[95] = KING  # White king at h1
        self.board.board[31] = QUEEN # White queen at a7
        self.board.color[21] = BLACK
        self.board.color[95] = WHITE
        self.board.color[31] = WHITE
        self.board.side_to_move = BLACK
        
        # Verify stalemate
        moves = self.movegen.generate_moves()
        self.assertEqual(len(moves), 0)
        
    def test_insufficient_material(self):
        # Setup king vs king position
        self.board = Board()
        for sq in range(21, 99):
            self.board.board[sq] = EMPTY
            
        self.board.board[25] = KING
        self.board.board[95] = KING
        self.board.color[25] = WHITE
        self.board.color[95] = BLACK
        
        # Both sides should still have legal moves
        self.board.side_to_move = WHITE
        white_moves = self.movegen.generate_moves()
        self.board.side_to_move = BLACK
        black_moves = self.movegen.generate_moves()
        
        self.assertTrue(len(white_moves) > 0)
        self.assertTrue(len(black_moves) > 0)
