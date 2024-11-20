import streamlit as st
import chess
import chess.svg
from engine.board import Board
from engine.search import SearchEngine
from engine.evaluation import Evaluator
import time
from datetime import timedelta

def init_session_state():
    if 'board' not in st.session_state:
        st.session_state.board = Board()
        st.session_state.game = chess.Board()
        st.session_state.search_engine = SearchEngine(st.session_state.board)
        st.session_state.evaluator = Evaluator()
        st.session_state.start_time = time.time()
        st.session_state.last_move = None  # Track last move made

def format_time(seconds):
    """Format time in MM:SS"""
    minutes, seconds = divmod(int(seconds), 60)
    return f"{minutes:02d}:{seconds:02d}"

def get_game_time():
    elapsed = time.time() - st.session_state.start_time
    return format_time(elapsed)

def convert_to_internal(square):
    file = square % 8
    rank = square // 8
    return 21 + file + ((7 - rank) * 10)

def convert_from_internal(square):
    file = (square - 21) % 10
    rank = 7 - ((square - 21) // 10)
    if 0 <= file < 8 and 0 <= rank < 8:
        return rank * 8 + file
    return None

def handle_move(move_str):
    try:
        # Parse the move
        from_square = chess.parse_square(move_str[:2])
        to_square = chess.parse_square(move_str[2:4])
        promotion = chess.QUEEN if len(move_str) > 4 and move_str[4].lower() == 'q' else None

        # Create the move
        chess_move = chess.Move(from_square, to_square, promotion=promotion)

        # Make move on chess.Board
        st.session_state.game.push(chess_move)
        st.session_state.last_move = move_str  # Store the move

        # Make move on internal board
        internal_from = convert_to_internal(from_square)
        internal_to = convert_to_internal(to_square)
        st.session_state.board.make_move((internal_from, internal_to, promotion if promotion else 0))

        # Generate engine response
        if not st.session_state.game.is_game_over():
            with st.spinner('Engine thinking...'):
                score, engine_move = st.session_state.search_engine.search(search_depth)
                if engine_move:
                    chess_from = convert_from_internal(engine_move[0])
                    chess_to = convert_from_internal(engine_move[1])
                    engine_chess_move = chess.Move(chess_from, chess_to,
                                                 promotion=engine_move[2] if engine_move[2] else None)

                    if engine_chess_move in st.session_state.game.legal_moves:
                        st.session_state.game.push(engine_chess_move)
                        st.session_state.board.make_move(engine_move)

        st.rerun()
        return True
    except Exception as e:
        st.error(f"Move error: {str(e)}")
        return False

# Initialize session state
init_session_state()

# Main app
st.title('equifAI Chess Game')

# Sidebar controls
st.sidebar.header('Controls')
difficulty = st.sidebar.slider('Engine Strength', 1, 5, 3)
search_depth = difficulty

# Main board display
col1, col2 = st.columns([2, 1])

with col1:
    # Display chess board
    board_svg = chess.svg.board(board=st.session_state.game, size=400)
    st.image(board_svg)

    # Display game status
    if st.session_state.game.is_game_over():
        if st.session_state.game.is_checkmate():
            st.error('Checkmate! ' + ('Black' if st.session_state.game.turn else 'White') + ' wins!')
        elif st.session_state.game.is_stalemate():
            st.warning('Game drawn by stalemate')
        elif st.session_state.game.is_insufficient_material():
            st.warning('Game drawn by insufficient material')
        elif st.session_state.game.is_fifty_moves():
            st.warning('Game drawn by fifty-move rule')
        elif st.session_state.game.is_repetition():
            st.warning('Game drawn by threefold repetition')

with col2:
    # Game information
    st.subheader('Game Information')

    # Display game timer
    st.metric("Game Time", get_game_time())

    st.write(f"Turn: {'White' if st.session_state.game.turn else 'Black'}")
    st.write(f"Move number: {st.session_state.game.fullmove_number}")

    evaluation = st.session_state.evaluator.evaluate(st.session_state.board)
    st.write(f'Evaluation: {evaluation/100:.2f}')

    # Move input section
    move_input = st.text_input('Make a move (e.g., e2e4):', '')

    # Process move input
    if move_input and move_input != st.session_state.last_move:  # Only process if it's a new move
        legal_moves = [move.uci() for move in st.session_state.game.legal_moves]
        if move_input in legal_moves:
            handle_move(move_input)
        elif move_input not in legal_moves and st.session_state.last_move != move_input:
            st.error(f"Invalid move. Legal moves: {', '.join(legal_moves[:5])}...")

    # New Game button
    if st.button('New Game'):
        st.session_state.board = Board()
        st.session_state.game = chess.Board()
        st.session_state.search_engine = SearchEngine(st.session_state.board)
        st.session_state.evaluator = Evaluator()
        st.session_state.start_time = time.time()
        st.session_state.last_move = None
        st.rerun()

# Move history
st.subheader('Move History')
if st.session_state.game.move_stack:
    moves_text = ""
    for i, move in enumerate(st.session_state.game.move_stack):
        if i % 2 == 0:
            moves_text += f"{i//2 + 1}. {move} "
        else:
            moves_text += f"{move}\n"
    st.text_area('Moves:', value=moves_text, height=100)
else:
    st.text_area('Moves:', value='No moves yet', height=100)

# Footer
st.markdown('---')
footer_html = """
<div style="text-align: center; margin-top: 20px;">
    <p>Built with ❤️ using <a href="https://streamlit.io" target="_blank">Streamlit</a> | 
    View source code on <a href="https://github.com/ravishan16/chess-engine.git" target="_blank">GitHub</a></p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
