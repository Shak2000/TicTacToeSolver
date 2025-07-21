// --- UI State ---
let board = [];
let height = 3;
let width = 3;
let win = 3;
let player = 'X';
let rem = 0;
let history = [];
let gameActive = false;

const boardDiv = document.getElementById('board');
const statusDiv = document.getElementById('status');
const startBtn = document.getElementById('start-btn');
const undoBtn = document.getElementById('undo-btn');
const restartBtn = document.getElementById('restart-btn');
const aiBtn = document.getElementById('ai-btn');
const uiControls = document.getElementById('ui-controls');

function initBoard(h, w) {
    board = Array.from({length: h}, () => Array(w).fill('.'));
    rem = h * w;
    history = [];
    player = 'X';
    gameActive = true;
}

function renderBoard() {
    boardDiv.innerHTML = '';
    boardDiv.style.gridTemplateRows = `repeat(${height}, 1fr)`;
    boardDiv.style.gridTemplateColumns = `repeat(${width}, 1fr)`;
    for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.textContent = board[y][x] === '.' ? '' : board[y][x];
            cell.dataset.x = x;
            cell.dataset.y = y;
            cell.addEventListener('click', onCellClick);
            boardDiv.appendChild(cell);
        }
    }
}

function onCellClick(e) {
    if (!gameActive) return;
    const x = parseInt(e.target.dataset.x);
    const y = parseInt(e.target.dataset.y);
    if (board[y][x] !== '.') return;
    makeMove(x, y);
}

function makeMove(x, y) {
    if (board[y][x] !== '.') return;
    history.push(board.map(row => row.slice()));
    board[y][x] = player;
    rem--;
    renderBoard();
    const winner = checkWinner();
    if (winner) {
        statusDiv.textContent = `Player ${winner} wins!`;
        gameActive = false;
        return;
    } else if (rem === 0) {
        statusDiv.textContent = "It's a draw!";
        gameActive = false;
        return;
    }
    player = player === 'X' ? 'O' : 'X';
    statusDiv.textContent = `Player ${player}'s turn`;
}

function undoMove() {
    if (history.length === 0) return;
    board = history.pop();
    rem = board.flat().filter(c => c === '.').length;
    player = player === 'X' ? 'O' : 'X';
    gameActive = true;
    renderBoard();
    statusDiv.textContent = `Player ${player}'s turn`;
}

function restartGame() {
    initBoard(height, width);
    renderBoard();
    statusDiv.textContent = `Player ${player}'s turn`;
    gameActive = true;
}

function startGame() {
    height = parseInt(document.getElementById('height').value);
    width = parseInt(document.getElementById('width').value);
    win = parseInt(document.getElementById('win').value);
    initBoard(height, width);
    renderBoard();
    statusDiv.textContent = `Player ${player}'s turn`;
    uiControls.style.display = '';
}

function checkWinner() {
    // Check all rows, columns, and diagonals
    const lines = [];
    // Rows
    for (let row of board) lines.push(row);
    // Columns
    for (let col = 0; col < width; col++) {
        lines.push(board.map(row => row[col]));
    }
    // Diagonals
    for (let d = -(height-1); d < width; d++) {
        let diag1 = [], diag2 = [];
        for (let y = 0; y < height; y++) {
            let x1 = d + y, x2 = d + height - 1 - y;
            if (x1 >= 0 && x1 < width) diag1.push(board[y][x1]);
            if (x2 >= 0 && x2 < width) diag2.push(board[y][x2]);
        }
        if (diag1.length >= win) lines.push(diag1);
        if (diag2.length >= win) lines.push(diag2);
    }
    for (let line of lines) {
        for (let i = 0; i <= line.length - win; i++) {
            const segment = line.slice(i, i+win);
            if (segment.every(c => c === 'X')) return 'X';
            if (segment.every(c => c === 'O')) return 'O';
        }
    }
    return null;
}

function aiMove() {
    if (!gameActive) return;
    if (height === 3 && width === 3 && win === 3) {
        // Use minimax for 3x3
        const move = getBestMove(player, 9);
        if (move) makeMove(move.x, move.y);
    } else {
        // For larger boards, pick a random move for now
        const moves = [];
        for (let y = 0; y < height; y++) {
            for (let x = 0; x < width; x++) {
                if (board[y][x] === '.') moves.push({x, y});
            }
        }
        if (moves.length > 0) {
            const move = moves[Math.floor(Math.random() * moves.length)];
            makeMove(move.x, move.y);
        }
    }
}

function getBestMove(aiPlayer, depth) {
    let bestScore = -Infinity;
    let move = null;
    for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
            if (board[y][x] === '.') {
                board[y][x] = aiPlayer;
                rem--;
                let score = minimax(depth - 1, false, aiPlayer, aiPlayer === 'X' ? 'O' : 'X');
                board[y][x] = '.';
                rem++;
                if (score > bestScore) {
                    bestScore = score;
                    move = {x, y};
                }
            }
        }
    }
    return move;
}

function minimax(depth, isMax, aiPlayer, currentPlayer) {
    const winner = checkWinner();
    if (winner === aiPlayer) return 100;
    if (winner && winner !== aiPlayer) return -100;
    if (rem === 0 || depth === 0) return 0;
    let best = isMax ? -Infinity : Infinity;
    for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
            if (board[y][x] === '.') {
                board[y][x] = currentPlayer;
                rem--;
                let score = minimax(depth - 1, !isMax, aiPlayer, currentPlayer === 'X' ? 'O' : 'X');
                board[y][x] = '.';
                rem++;
                if (isMax) {
                    best = Math.max(best, score);
                } else {
                    best = Math.min(best, score);
                }
            }
        }
    }
    return best;
}

startBtn.addEventListener('click', startGame);
undoBtn.addEventListener('click', undoMove);
restartBtn.addEventListener('click', restartGame);
aiBtn.addEventListener('click', aiMove);

// Initial render
renderBoard();
statusDiv.textContent = 'Click "Start New Game" to begin.'; 