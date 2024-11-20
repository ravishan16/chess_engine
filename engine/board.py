from typing import List, Tuple
from .constants import *

class Board:
    def __init__(self):
        # 10x12 board representation with border
        self.board = [0] * 120
        self.color = [0] * 120
        self.piece_lists = {color: {piece: [] for piece in range(1, 7)} 
                          for color in [WHITE, BLACK]}
        self.side_to_move = WHITE
        self.castling_rights = {WHITE: (True, True), BLACK: (True, True)}
        self.ep_square = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.init_board()
        # Initialize movegen after board setup
        from .movegen import MoveGenerator
        self.movegen = MoveGenerator(self)

    def init_board(self):
        # Initialize empty board with border squares marked as invalid
        self.board = [-1] * 120  # Use -1 for border squares
        self.color = [EMPTY] * 120
        
        # Setup initial position
        piece_setup = [
            (ROOK, 21), (KNIGHT, 22), (BISHOP, 23), (QUEEN, 24),
            (KING, 25), (BISHOP, 26), (KNIGHT, 27), (ROOK, 28)
        ]
        
        # Place pieces
        for piece, square in piece_setup:
            # Place black pieces
            self.board[square] = piece
            self.color[square] = BLACK
            self.board[square + 10] = PAWN
            self.color[square + 10] = BLACK
            
            # Place white pieces
            self.board[square + 70] = piece
            self.color[square + 70] = WHITE
            self.board[square + 60] = PAWN
            self.color[square + 60] = WHITE
            
        # Mark central squares as empty
        for rank in range(2, 6):
            for file in range(1, 9):
                sq = rank * 10 + file + 20
                if self.board[sq] == -1:
                    self.board[sq] = EMPTY

    def make_move(self, move: Tuple[int, int, int]) -> bool:
        from_sq, to_sq, promotion = move
        piece = self.board[from_sq]
        
        # Make the move
        self.board[to_sq] = promotion if promotion else piece
        self.board[from_sq] = EMPTY
        self.color[to_sq] = self.color[from_sq]
        self.color[from_sq] = EMPTY

        # Handle special moves (castling, en passant, etc.)
        if piece == KING:
            self.handle_castling(from_sq, to_sq)
        elif piece == PAWN:
            self.handle_pawn_move(from_sq, to_sq, promotion)

        # Update move counters and side to move
        if piece == PAWN or self.board[to_sq] != EMPTY:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        if self.side_to_move == BLACK:
            self.fullmove_number += 1

        self.side_to_move = 1 - self.side_to_move
        return True

    def handle_castling(self, from_sq: int, to_sq: int):
        # Handle castling moves
        if abs(to_sq - from_sq) == 2:
            rook_from = from_sq + 3 if to_sq > from_sq else from_sq - 4
            rook_to = (from_sq + to_sq) // 2
            self.board[rook_to] = ROOK
            self.board[rook_from] = EMPTY
            self.color[rook_to] = self.color[to_sq]
            self.color[rook_from] = EMPTY

        # Update castling rights
        side = self.side_to_move
        self.castling_rights[side] = (False, False)

    def handle_pawn_move(self, from_sq: int, to_sq: int, promotion: int):
        # Handle en passant captures
        if self.ep_square and to_sq == self.ep_square:
            captured_sq = to_sq + (10 if self.side_to_move == WHITE else -10)
            self.board[captured_sq] = EMPTY
            self.color[captured_sq] = EMPTY

        # Set en passant square for double pawn moves
        if abs(to_sq - from_sq) == 20:
            self.ep_square = (from_sq + to_sq) // 2
        else:
            self.ep_square = None

    def get_fen(self) -> str:
        # Generate FEN string for current position
        fen = []
        empty = 0
        
        for rank in range(8):
            for file in range(8):
                sq = 21 + file + rank * 10
                piece = self.board[sq]
                
                if piece == EMPTY:
                    empty += 1
                else:
                    if empty > 0:
                        fen.append(str(empty))
                        empty = 0
                    piece_char = "PNBRQK"[piece - 1]
                    if self.color[sq] == BLACK:
                        piece_char = piece_char.lower()
                    fen.append(piece_char)
                    
            if empty > 0:
                fen.append(str(empty))
                empty = 0
            if rank < 7:
                fen.append('/')
                
        return ''.join(fen)
