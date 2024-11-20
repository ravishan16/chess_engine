import unittest
from engine.board import Board
from engine.evaluation import Evaluator
from engine.constants import *

class TestEvaluation(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.evaluator = Evaluator()
        
    def test_initial_position(self):
        # Initial position should be balanced
        score = self.evaluator.evaluate(self.board)
        self.assertEqual(score, 0)
        
    def test_material_advantage(self):
        # Clear the board
        for sq in range(21, 99):
            self.board.board[sq] = EMPTY
            
        # Setup position with material advantage
        self.board.board[25] = KING
        self.board.board[95] = KING
        self.board.board[45] = QUEEN
        self.board.color[25] = WHITE
        self.board.color[95] = BLACK
        self.board.color[45] = WHITE
        
        score = self.evaluator.evaluate(self.board)
        self.assertTrue(score > 800)  # Queen value is 900
        
    def test_piece_position_bonus(self):
        # Test central knight vs corner knight
        self.board = Board()
        for sq in range(21, 99):
            self.board.board[sq] = EMPTY
            
        # Place knights
        self.board.board[44] = KNIGHT  # Central knight
        self.board.board[21] = KNIGHT  # Corner knight
        self.board.color[44] = WHITE
        self.board.color[21] = BLACK
        
        score = self.evaluator.evaluate(self.board)
        self.assertTrue(score > 0)  # Central knight should be better
        
    def test_king_safety(self):
        # Test king safety evaluation
        self.board = Board()
        
        # Setup protected king vs exposed king
        self.board.board[25] = KING
        self.board.board[95] = KING
        self.board.board[24] = PAWN
        self.board.board[26] = PAWN
        self.board.color[25] = WHITE
        self.board.color[95] = BLACK
        self.board.color[24] = WHITE
        self.board.color[26] = WHITE
        
        score = self.evaluator.evaluate(self.board)
        self.assertTrue(score > 0)  # Protected king should be better
