from .constants import *

class Evaluator:
    def __init__(self):
        self.pst = PIECE_SQUARE_TABLES
        self.piece_values = PIECE_VALUES
        
    def evaluate(self, board) -> int:
        score = 0
        
        # Material and piece-square table evaluation
        score += self.evaluate_material(board)
        score += self.evaluate_position(board)
        
        # Mobility
        score += self.evaluate_mobility(board)
        
        # King safety
        score += self.evaluate_king_safety(board)
        
        # Return score from white's perspective
        return score if board.side_to_move == WHITE else -score
        
    def evaluate_material(self, board) -> int:
        score = 0
        for sq in range(21, 99):
            piece = board.board[sq]
            if piece != EMPTY and piece != -1:  # Skip empty and border squares
                value = self.piece_values[piece]
                if board.color[sq] == BLACK:
                    value = -value
                score += value
        return score
        
    def evaluate_position(self, board) -> int:
        score = 0
        for sq in range(21, 99):
            piece = board.board[sq]
            if piece != EMPTY and piece != -1:  # Skip empty and border squares
                pst_sq = sq - 21
                if 0 <= pst_sq < 64:  # Add bounds check
                    if board.color[sq] == WHITE:
                        pst_sq = 63 - pst_sq
                    if piece in self.pst:  # Check if piece has pst table
                        value = self.pst[piece][pst_sq]
                        if board.color[sq] == BLACK:
                            value = -value
                        score += value
        return score
        
    def evaluate_mobility(self, board) -> int:
        from .movegen import MoveGenerator
        mg = MoveGenerator(board)
        mobility = len(mg.generate_moves())
        
        # Switch sides to count opponent's moves
        board.side_to_move = 1 - board.side_to_move
        opp_mobility = len(mg.generate_moves())
        board.side_to_move = 1 - board.side_to_move
        
        return (mobility - opp_mobility) * 10
        
    def evaluate_king_safety(self, board) -> int:
        score = 0
        
        # Find kings
        white_king = black_king = None
        for sq in range(21, 99):
            if board.board[sq] == KING:
                if board.color[sq] == WHITE:
                    white_king = sq
                else:
                    black_king = sq
                    
        # Evaluate pawn shield
        score += self.evaluate_pawn_shield(board, white_king, WHITE)
        score -= self.evaluate_pawn_shield(board, black_king, BLACK)
        
        return score
        
    def evaluate_pawn_shield(self, board, king_sq: int, color: int) -> int:
        if not king_sq:
            return 0
            
        score = 0
        shield_squares = []
        
        # Define pawn shield squares based on king position
        rank = king_sq // 10
        file = king_sq % 10
        
        direction = -10 if color == WHITE else 10
        
        # Check pawns in front of king
        for f in range(max(1, file - 1), min(9, file + 2)):
            shield_squares.append(king_sq + direction + (f - file))
            
        # Score pawn shield
        for sq in shield_squares:
            if (board.board[sq] == PAWN and 
                board.color[sq] == color):
                score += 10
                
        return score
