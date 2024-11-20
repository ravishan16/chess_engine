import unittest
from engine.board import Board
from engine.search import SearchEngine
from engine.constants import *

class TestSearch(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.search_engine = SearchEngine(self.board)
        
    def test_mate_in_one(self):
        # Setup a mate in one position
        self.board = Board()
        for sq in range(21, 99):
            self.board.board[sq] = EMPTY
            
        # Black king at h8, White queen at g7
        self.board.board[28] = KING
        self.board.board[37] = QUEEN
        self.board.board[95] = KING
        self.board.color[28] = BLACK
        self.board.color[37] = WHITE
        self.board.color[95] = WHITE
        self.board.side_to_move = WHITE
        
        score, best_move = self.search_engine.search(3)
        self.assertIsNotNone(best_move)
        self.assertTrue(score > 10000)  # Should recognize winning position
        
    def test_capture_highest_value(self):
        # Test if engine captures highest value piece when multiple captures available
        self.board = Board()
        for sq in range(21, 99):
            self.board.board[sq] = EMPTY
            
        # Setup position with multiple captures
        self.board.board[45] = QUEEN  # White queen
        self.board.board[54] = PAWN   # Black pawn
        self.board.board[56] = QUEEN  # Black queen
        self.board.color[45] = WHITE
        self.board.color[54] = BLACK
        self.board.color[56] = BLACK
        self.board.side_to_move = WHITE
        
        score, best_move = self.search_engine.search(3)
        self.assertEqual(best_move[1], 56)  # Should capture the queen
        
    def test_depth_effect(self):
        # Test if deeper search produces different/better moves
        self.board = Board()
        
        # Get moves at different depths
        _, move1 = self.search_engine.search(1)
        nodes1 = self.search_engine.nodes
        
        _, move2 = self.search_engine.search(3)
        nodes2 = self.search_engine.nodes
        
        self.assertTrue(nodes2 > nodes1)  # Deeper search should evaluate more nodes
        
    def test_transposition_table(self):
        # Test if transposition table is working
        self.board = Board()
        
        # First search
        self.search_engine.search(3)
        nodes1 = self.search_engine.nodes
        
        # Second search of same position
        self.search_engine.search(3)
        nodes2 = self.search_engine.nodes
        
        self.assertTrue(nodes2 < nodes1)  # Should use cached positions
