from typing import List, Tuple
from .constants import *

class MoveGenerator:
    def __init__(self, board):
        self.board = board
        self.moves = []
        
    def generate_moves(self) -> List[Tuple[int, int, int]]:
        self.moves = []
        side = self.board.side_to_move
        
        for sq in range(21, 99):
            if self.board.board[sq] != EMPTY and self.board.color[sq] == side:
                self.generate_piece_moves(sq)
                
        return self.moves
        
    def generate_piece_moves(self, square: int):
        piece = self.board.board[square]
        if piece == PAWN:
            self.generate_pawn_moves(square)
        elif piece == KNIGHT:
            self.generate_knight_moves(square)
        elif piece == BISHOP:
            self.generate_bishop_moves(square)
        elif piece == ROOK:
            self.generate_rook_moves(square)
        elif piece == QUEEN:
            self.generate_queen_moves(square)
        elif piece == KING:
            self.generate_king_moves(square)
            
    def generate_pawn_moves(self, square: int):
        direction = -10 if self.board.side_to_move == WHITE else 10
        
        # Single push
        to_sq = square + direction
        if self.board.board[to_sq] == EMPTY:
            self.add_pawn_moves(square, to_sq)
            
            # Double push
            if ((self.board.side_to_move == WHITE and 80 <= square <= 89) or
                (self.board.side_to_move == BLACK and 30 <= square <= 39)):
                to_sq = square + 2 * direction
                if self.board.board[to_sq] == EMPTY:
                    self.moves.append((square, to_sq, 0))
        
        # Captures
        for to_sq in [square + direction - 1, square + direction + 1]:
            if (self.board.board[to_sq] != EMPTY and 
                self.board.color[to_sq] != self.board.side_to_move):
                self.add_pawn_moves(square, to_sq)
                
            # En passant captures
            if to_sq == self.board.ep_square:
                self.moves.append((square, to_sq, 0))
                
    def add_pawn_moves(self, from_sq: int, to_sq: int):
        # Handle promotions
        if (self.board.side_to_move == WHITE and 20 <= to_sq <= 29) or \
           (self.board.side_to_move == BLACK and 90 <= to_sq <= 99):
            for piece in [QUEEN, ROOK, BISHOP, KNIGHT]:
                self.moves.append((from_sq, to_sq, piece))
        else:
            self.moves.append((from_sq, to_sq, 0))
            
    def generate_knight_moves(self, square: int):
        offsets = [-21, -19, -12, -8, 8, 12, 19, 21]
        for offset in offsets:
            to_sq = square + offset
            if (self.board.board[to_sq] == EMPTY or 
                self.board.color[to_sq] != self.board.side_to_move):
                self.moves.append((square, to_sq, 0))
                
    def generate_sliding_moves(self, square: int, directions: List[int]):
        for direction in directions:
            to_sq = square + direction
            # Change the condition to continue while square is valid
            while self.board.board[to_sq] != -1:  # Stop at border squares
                if self.board.board[to_sq] == EMPTY:
                    self.moves.append((square, to_sq, 0))
                elif self.board.color[to_sq] != self.board.side_to_move:
                    self.moves.append((square, to_sq, 0))
                    break
                else:
                    break
                to_sq += direction
                
    def generate_bishop_moves(self, square: int):
        self.generate_sliding_moves(square, [-11, -9, 9, 11])
        
    def generate_rook_moves(self, square: int):
        self.generate_sliding_moves(square, [-10, -1, 1, 10])
        
    def generate_queen_moves(self, square: int):
        self.generate_sliding_moves(square, [-11, -10, -9, -1, 1, 9, 10, 11])
        
    def generate_king_moves(self, square: int):
        offsets = [-11, -10, -9, -1, 1, 9, 10, 11]
        for offset in offsets:
            to_sq = square + offset
            if (self.board.board[to_sq] == EMPTY or 
                self.board.color[to_sq] != self.board.side_to_move):
                self.moves.append((square, to_sq, 0))
                
        # Castling
        if self.board.castling_rights[self.board.side_to_move][0]:  # Kingside
            if (self.board.board[square + 1] == EMPTY and 
                self.board.board[square + 2] == EMPTY):
                self.moves.append((square, square + 2, 0))
                
        if self.board.castling_rights[self.board.side_to_move][1]:  # Queenside
            if (self.board.board[square - 1] == EMPTY and 
                self.board.board[square - 2] == EMPTY and
                self.board.board[square - 3] == EMPTY):
                self.moves.append((square, square - 2, 0))
