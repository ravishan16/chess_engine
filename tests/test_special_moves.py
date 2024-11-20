import unittest
from engine.board import Board
from engine.movegen import MoveGenerator
from engine.constants import *

class TestSpecialMoves(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.movegen = MoveGenerator(self.board)
        
    def test_castling_kingside(self):
        # Setup castling position
        self.board.board[25] = KING
        self.board.board[28] = ROOK
        self.board.board[26] = EMPTY
        self.board.board[27] = EMPTY
        self.board.color[25] = WHITE
        self.board.color[28] = WHITE
        self.board.side_to_move = WHITE
        
        moves = self.movegen.generate_moves()
        castle_move = (25, 27, 0)  # e1-g1
        self.assertIn(castle_move, moves)
        
        # Test castling execution
        self.board.make_move(castle_move)
        self.assertEqual(self.board.board[27], KING)
        self.assertEqual(self.board.board[26], ROOK)
        
    def test_castling_queenside(self):
        # Setup castling position
        self.board.board[25] = KING
        self.board.board[21] = ROOK
        self.board.board[22] = EMPTY
        self.board.board[23] = EMPTY
        self.board.board[24] = EMPTY
        self.board.color[25] = WHITE
        self.board.color[21] = WHITE
        self.board.side_to_move = WHITE
        
        moves = self.movegen.generate_moves()
        castle_move = (25, 23, 0)  # e1-c1
        self.assertIn(castle_move, moves)
        
        # Test castling execution
        self.board.make_move(castle_move)
        self.assertEqual(self.board.board[23], KING)
        self.assertEqual(self.board.board[24], ROOK)
        
    def test_en_passant(self):
        # Setup en passant position
        self.board.board[61] = PAWN  # e4
        self.board.board[52] = PAWN  # d4
        self.board.color[61] = WHITE
        self.board.color[52] = BLACK
        self.board.side_to_move = BLACK
        self.board.ep_square = 61
        
        moves = self.movegen.generate_moves()
        ep_move = (52, 61, 0)  # d4xe3
        self.assertIn(ep_move, moves)
        
        # Test en passant capture
        self.board.make_move(ep_move)
        self.assertEqual(self.board.board[61], PAWN)
        self.assertEqual(self.board.board[51], EMPTY)
        
    def test_pawn_promotion(self):
        # Setup promotion position
        self.board.board[31] = PAWN  # e7
        self.board.color[31] = WHITE
        self.board.side_to_move = WHITE
        
        moves = self.movegen.generate_moves()
        promotion_moves = [
            (31, 21, QUEEN),  # e7-e8=Q
            (31, 21, ROOK),   # e7-e8=R
            (31, 21, BISHOP), # e7-e8=B
            (31, 21, KNIGHT)  # e7-e8=N
        ]
        
        for move in promotion_moves:
            self.assertIn(move, moves)
            
        # Test promotion execution
        self.board.make_move(promotion_moves[0])  # Promote to queen
        self.assertEqual(self.board.board[21], QUEEN)
        self.assertEqual(self.board.color[21], WHITE)
