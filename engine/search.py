from typing import Tuple, List
from .evaluation import Evaluator
from .movegen import MoveGenerator
from .constants import EMPTY, PAWN, QUEEN, ROOK

class SearchEngine:
    def __init__(self, board):
        self.board = board
        self.evaluator = Evaluator()
        self.movegen = MoveGenerator(board)
        self.transposition_table = {}
        self.nodes = 0
        self.best_move = None
        self.move_history = {}  # Store move history for move ordering
        
    def search(self, depth: int) -> Tuple[int, Tuple[int, int, int]]:
        self.nodes = 0
        self.max_depth = depth
        score = self.alpha_beta(depth, -float('inf'), float('inf'))
        return score, self.best_move
        
    def alpha_beta(self, depth: int, alpha: float, beta: float) -> int:
        if depth == 0:
            return self.quiescence(alpha, beta)
            
        self.nodes += 1
        
        # Check transposition table
        pos_key = self.board.get_fen()
        if pos_key in self.transposition_table:
            if self.transposition_table[pos_key]['depth'] >= depth:
                return self.transposition_table[pos_key]['score']
                
        moves = self.movegen.generate_moves()
        if not moves:
            return -20000  # Checkmate
            
        # Move ordering with history heuristic
        moves = self.order_moves(moves)
        
        best_move = None
        for move in moves:
            # Make move
            old_state = self.make_move(move)
            
            # Recursive search
            score = -self.alpha_beta(depth - 1, -beta, -alpha)
            
            # Unmake move
            self.unmake_move(old_state)
            
            if score >= beta:
                # Update move history for beta cutoff
                self.update_move_history(move, depth)
                return beta
                
            if score > alpha:
                alpha = score
                best_move = move
                # Update move history for best move
                self.update_move_history(move, depth)
                
        # Store in transposition table
        self.transposition_table[pos_key] = {
            'score': alpha,
            'depth': depth
        }
        
        if depth == self.max_depth:
            self.best_move = best_move
            
        return alpha
        
    def quiescence(self, alpha: float, beta: float) -> int:
        stand_pat = self.evaluator.evaluate(self.board)
        
        if stand_pat >= beta:
            return beta
            
        if alpha < stand_pat:
            alpha = stand_pat
            
        moves = self.movegen.generate_moves()
        moves = [m for m in moves if self.is_capture(m)]
        moves = self.order_moves(moves)  # Order even capture moves
        
        for move in moves:
            old_state = self.make_move(move)
            score = -self.quiescence(-beta, -alpha)
            self.unmake_move(old_state)
            
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
                
        return alpha
        
    def order_moves(self, moves: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
        # Score moves based on multiple factors
        move_scores = []
        for move in moves:
            score = 0
            
            # 1. Captures (MVV-LVA)
            if self.is_capture(move):
                victim = self.board.board[move[1]]
                attacker = self.board.board[move[0]]
                score += 10 * victim - attacker
                
            # 2. Promotions
            if move[2]:  # Promotion piece
                score += 900 if move[2] == QUEEN else 500  # Queen or Rook
                
            # 3. History heuristic
            move_key = (move[0], move[1])
            if move_key in self.move_history:
                score += self.move_history[move_key]
                
            move_scores.append((move, score))
            
        # Sort moves by score in descending order
        move_scores.sort(key=lambda x: x[1], reverse=True)
        return [move for move, _ in move_scores]
        
    def update_move_history(self, move: Tuple[int, int, int], depth: int):
        move_key = (move[0], move[1])
        if move_key not in self.move_history:
            self.move_history[move_key] = 0
        self.move_history[move_key] += depth * depth
        
    def is_capture(self, move: Tuple[int, int, int]) -> bool:
        to_sq = move[1]
        return self.board.board[to_sq] != EMPTY
        
    def make_move(self, move: Tuple[int, int, int]) -> dict:
        # Save current state
        old_state = {
            'board': self.board.board.copy(),
            'color': self.board.color.copy(),
            'castling_rights': self.board.castling_rights.copy(),
            'ep_square': self.board.ep_square,
            'side_to_move': self.board.side_to_move
        }
        
        self.board.make_move(move)
        return old_state
        
    def unmake_move(self, old_state: dict):
        self.board.board = old_state['board']
        self.board.color = old_state['color']
        self.board.castling_rights = old_state['castling_rights']
        self.board.ep_square = old_state['ep_square']
        self.board.side_to_move = old_state['side_to_move']
