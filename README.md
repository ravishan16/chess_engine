# equifAI Chess Engine

## Overview
equiFi Chess is a sophisticated chess engine and web interface built with Python. The engine implements advanced chess algorithms including alpha-beta pruning search, positional evaluation, and multi-depth move analysis. The web interface, built with Streamlit, provides a user-friendly experience with real-time game analysis and interactive features.

## Demo
[![Watch the video](https://img.youtube.com/vi/As6f-FCAscM/0.jpg)](https://youtu.be/As6f-FCAscM)

## Project Structure
```
chess_engine/
├── LICENSE
├── README.md
├── assets/
│   └── chessboard.svg         # Board visualization assets
├── engine/
│   ├── board.py              # Board representation and move execution
│   ├── constants.py          # Game constants and configurations
│   ├── evaluation.py         # Position evaluation logic
│   ├── movegen.py           # Move generation algorithms
│   └── search.py            # Search tree implementation
├── environment.yaml          # Conda environment specification
├── generated-icon.png        # Project icon
├── main.py                  # Main application entry point
├── pyproject.toml           # Project metadata and dependencies
├── requirements.txt         # Python package requirements
├── setup.py                # Package installation script
└── tests/
    ├── test_board.py       # Board functionality tests
    ├── test_evaluation.py  # Evaluation logic tests
    ├── test_game_end.py    # Game ending conditions tests
    ├── test_movegen.py     # Move generation tests
    ├── test_search.py      # Search algorithm tests
    └── test_special_moves.py # Special chess moves tests
```

## Features

### Core Engine Features
* Advanced move generation and validation
* Configurable search depth (1-5 levels)
* Alpha-beta pruning with move ordering
* Transposition table for position caching
* Quiescence search for tactical stability
* Iterative deepening for optimal time management

### Game Features
* Complete chess rules implementation
* Support for special moves:
  - Castling (kingside and queenside)
  - En passant captures
  - Pawn promotion
* Move validation and legal move suggestions
* Game state tracking and FEN generation

### User Interface
* Interactive web-based board display
* Real-time position evaluation
* Game timer functionality
* Move history with algebraic notation
* Captured pieces display
* Engine difficulty adjustment
* Legal moves display button

## Technical Stack

### Core Technologies
* **Python 3.11+**: Primary development language
* **Streamlit**: Web interface framework
* **python-chess**: Chess logic and board representation
* **NumPy**: Numerical computations and board analysis

### Development Tools
* **unittest**: Test framework
* **Git**: Version control
* **Conda**: Environment management

## Installation and Setup

### Prerequisites
- Conda package manager
- Git (for cloning repository)

### Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/ravishan16/chess-engine.git
cd chess-engine
```

2. Create Conda environment:
```bash
conda env create -f environment.yaml
conda activate chess-engine
```

3. Run the application:
```bash
streamlit run main.py
```

### Alternative: Pip Installation
If you prefer using pip:
```bash
pip install -r requirements.txt
```

### Development Installation
For development work:
```bash
pip install -e .
```

## Testing

### Running Tests
```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests/test_board.py
```
### Docker Deployment
```dockerfile
# Dockerfile
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run application
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run the Docker container:
```bash
docker build -t chess-engine .
docker run -p 8501:8501 chess-engine
```

### Test Coverage
The test suite includes comprehensive tests covering all major components:

| Component         | Tests | Coverage |
|------------------|-------|----------|
| Board            | 15    | 100%     |
| Evaluation       | 4     | 100%     |
| Move Generation  | 7     | 100%     |
| Search           | 4     | 100%     |
| Game End         | 3     | 100%     |
| Special Moves    | 4     | 100%     |

## Future Improvements

### Engine Enhancements
1. **Neural Network Integration**
   - Position evaluation using deep learning
   - Pattern recognition for tactical motifs
   - Self-play training capability

2. **Opening Book**
   - Built-in opening database
   - Learning from master games
   - Opening repertoire customization

3. **Endgame Tablebases**
   - Syzygy tablebase integration
   - Perfect play in positions up to 7 pieces

### Performance Optimizations
1. **Search Improvements**
   - Principal Variation Search
   - Null Move Pruning
   - Late Move Reductions
   - Multi-threading support

2. **Board Representation**
   - Bitboard implementation
   - Move generation optimization
   - Cache-friendly data structures

### UI Enhancements
1. **Analysis Features**
   - Multiple variation analysis
   - Interactive move suggestions
   - Position assessment explanations
   - Critical moment detection

2. **Game Management**
   - PGN import/export
   - Game database integration
   - Session persistence
   - Move timing analysis

## Contributing
We welcome contributions! Please see our contributing guidelines for details on how to submit pull requests, report issues, and contribute to development.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support
For support, questions, or feature requests:
1. Open an issue in the GitHub repository
2. Contact the development team
3. Check the documentation

---
## Release Notes

### Version 1.0.0 (Current)
- Initial release with core functionality
- Web interface implementation
- Basic AI opponent
- Move validation and game rules
- Position evaluation

## Contact
- Project Link: [GitHub Repository](https://github.com/ravishan16/chess-engine)
