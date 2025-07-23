# Tic-Tac-Toe Solver

A customizable Tic-Tac-Toe game with AI opponent, supporting variable board sizes and win conditions. Features both a web interface and command-line interface.

## Features

- **Customizable Board**: Play on boards from 3x3 up to 10x10
- **Variable Win Conditions**: Set custom win requirements (3-in-a-row, 4-in-a-row, etc.)
- **AI Opponent**: Minimax algorithm with alpha-beta pruning and configurable difficulty
- **Multiple Interfaces**: Web UI and command-line interface
- **Game Controls**: Undo moves, restart games, and step-by-step gameplay
- **Responsive Design**: Mobile-friendly web interface

## Quick Start

### Web Interface

1. Open `index.html` in your web browser
2. Set your preferred board dimensions and win condition
3. Click "Start New Game"
4. Click cells to make moves or use "Computer Move" for AI assistance

### Command Line Interface

```bash
python main.py
```

Follow the interactive prompts to:
- Start new games with custom settings
- Make moves by entering coordinates
- Get AI assistance with configurable search depth
- Undo moves and restart games

### Web Server (FastAPI)

```bash
pip install fastapi uvicorn
uvicorn app:app --reload
```

Then visit `http://localhost:8000` in your browser.

## Game Configuration

- **Height/Width**: Board dimensions (3-10)
- **Win**: Number of consecutive pieces needed to win (3-10)
- **AI Depth**: Minimax search depth for computer moves (1-10)

## AI Algorithm

The computer opponent uses the **Minimax algorithm** with:
- **Alpha-beta pruning** for performance optimization
- **Strategic evaluation** considering center control and line potential
- **Configurable depth** for adjustable difficulty levels

For 3x3 boards, the AI searches the entire game tree for perfect play. Larger boards use depth-limited search with heuristic evaluation.

## File Structure

```
├── index.html          # Web interface
├── styles.css          # Styling for web UI
├── script.js           # Frontend game logic and AI
├── main.py            # Command-line interface and core game logic
├── app.py             # FastAPI web server
└── README.md          # This file
```

## Technical Details

### Core Components

- **Game Class** (`main.py`): Core game logic, board management, and AI
- **Web Interface** (`script.js`): Browser-based gameplay with interactive UI
- **FastAPI Server** (`app.py`): RESTful API endpoints for web integration

### AI Implementation

The minimax algorithm evaluates positions by:
1. Checking for immediate wins/losses
2. Evaluating board positions with strategic scoring
3. Recursively exploring possible moves up to specified depth
4. Using alpha-beta pruning to eliminate suboptimal branches

### Evaluation Heuristics

- **Center control bonus** (especially important for 3x3)
- **Line potential scoring** based on partial sequences
- **Blocking opponent threats** with negative scoring
- **Exponential scoring** for multiple pieces in winning lines

## Browser Compatibility

The web interface works in all modern browsers including:
- Chrome/Chromium
- Firefox
- Safari
- Edge

## Performance Notes

- **3x3 boards**: AI uses complete game tree analysis
- **Larger boards**: Depth-limited search with configurable limits
- **Alpha-beta pruning**: Significantly reduces search time
- **Responsive UI**: Optimized for both desktop and mobile devices

## Contributing

Feel free to contribute improvements such as:
- Enhanced AI evaluation functions
- Additional game variants
- UI/UX improvements
- Performance optimizations

## License

This project is open source and available under the MIT License.
