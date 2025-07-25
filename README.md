# Tic-Tac-Toe Solver

A sophisticated tic-tac-toe game with AI solver capabilities, supporting customizable board sizes, win conditions, and both regular and misère game modes. Features both a modern web interface and command-line interface.

## Features

- **Customizable Game Settings**
  - Variable board dimensions (3x3 to 10x10)
  - Adjustable win condition (3 to 10 in a row)
  - Regular and Misère game modes
  
- **AI Solver**
  - Minimax algorithm with alpha-beta pruning
  - Configurable search depth
  - Specialized misère mode strategy
  - Optimal play for standard 3x3 boards
  
- **Dual Interface**
  - Modern responsive web UI
  - Command-line interface for terminal use
  
- **Game Features**
  - Move history with undo functionality
  - Game restart capability
  - Real-time game state updates

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd tic-tac-toe-solver
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Web Interface

1. Start the web server:
```bash
uvicorn app:app --reload
```

2. Open your browser and navigate to `http://localhost:8000`

3. Configure your game settings:
   - **Height/Width**: Board dimensions (3-10)
   - **Win**: Number in a row needed to win (3-10)
   - **Misère Mode**: Check to enable misère rules (lose by getting a line)

4. Click "Start New Game" and begin playing!

#### Web Interface Controls
- **Click cells** to make moves
- **Computer Move**: Let the AI make the next move
- **Undo**: Revert the last move
- **Restart**: Start over with same settings
- **Depth**: Adjust AI thinking depth (1-10)

### Command Line Interface

Run the command-line version:
```bash
python main.py
```

Follow the interactive prompts to:
- Choose between regular and misère modes
- Set board dimensions and win conditions
- Make moves or request AI moves
- Undo moves and restart games

## Game Modes

### Regular Mode
Standard tic-tac-toe rules - first player to get the required number in a row (horizontally, vertically, or diagonally) wins.

### Misère Mode
Reverse tic-tac-toe - the player who is **forced** to complete a line **loses**. This creates a completely different strategic game where you want to avoid winning lines while forcing your opponent into them.

## AI Strategy

### Regular Mode
- Uses minimax with alpha-beta pruning
- Evaluates positions based on potential winning lines
- Prioritizes center control on 3x3 boards
- Searches to full depth on 3x3 for perfect play

### Misère Mode
- Specialized evaluation function that avoids creating wins
- Strategic opening play (center control for X on 3x3)
- Mirror strategy implementation
- Careful endgame analysis to force opponent losses

## Technical Details

### Architecture
- **Backend**: FastAPI web framework
- **Frontend**: Vanilla JavaScript with modern CSS
- **Game Logic**: Pure Python implementation
- **AI**: Minimax algorithm with alpha-beta pruning

### Files Structure
- `main.py`: Core game logic and CLI interface
- `app.py`: FastAPI web server and API endpoints
- `index.html`: Web interface structure
- `styles.css`: Modern responsive styling
- `script.js`: Frontend game interaction logic
- `requirements.txt`: Python dependencies

### API Endpoints
- `GET /`: Serve web interface
- `POST /start`: Initialize new game
- `POST /move`: Make a move
- `POST /undo`: Undo last move
- `POST /restart`: Restart current game
- `GET /get_ai_move`: Get AI move for regular mode
- `GET /get_misere_ai_move`: Get AI move for misère mode
- `GET /state`: Get current game state

## Performance Notes

- **3x3 Regular**: AI plays optimally (searches full game tree)
- **Larger Boards**: Configurable depth limiting for reasonable response times
- **Misère Mode**: Additional strategic considerations may require deeper search

## Contributing

Feel free to submit issues and enhancement requests! Areas for potential improvement:
- Additional AI difficulty levels
- Tournament mode for multiple games
- Move suggestion highlighting
- Game analysis and statistics
- Network multiplayer support

## License

This project is open source and available under the MIT License.

---

Enjoy playing and exploring the strategic depths of tic-tac-toe and its misère variant!
