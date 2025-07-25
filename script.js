// --- UI State ---
let board = [];
let height = 3;
let width = 3;
let win = 3;
let player = 'X';
let rem = 0;
let history = [];
let gameActive = false;
let isMisere = false;

const boardDiv = document.getElementById('board');
const statusDiv = document.getElementById('status');
const startBtn = document.getElementById('start-btn');
const undoBtn = document.getElementById('undo-btn');
const restartBtn = document.getElementById('restart-btn');
const aiBtn = document.getElementById('ai-btn');
const uiControls = document.getElementById('ui-controls');

function updateStateFromBackend(state) {
    board = state.board;
    height = state.height;
    width = state.width;
    win = state.win;
    player = state.player;
    rem = state.rem;
    isMisere = state.misere;
    history = state.history;
    renderBoard();
    let msg = state.winner ? (isMisere ? `Player ${state.winner} loses (Misère)!` : `Player ${state.winner} wins!`) : `Player ${player}'s turn` + (isMisere ? ' (Misère)' : '');
    if (rem === 0 && !state.winner) msg = "It's a draw!";
    gameActive = !state.winner && rem > 0;
    statusDiv.textContent = gameActive ? msg : '';
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
    fetch('/move', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({x, y})
    })
    .then(res => res.json())
    .then(updateStateFromBackend);
}

function makeMove(x, y) {
    // Not used anymore, all moves go through backend
}

function undoMove() {
    fetch('/undo', {method: 'POST'}).then(res => res.json()).then(updateStateFromBackend);
}

function restartGame() {
    fetch('/restart', {method: 'POST'}).then(res => res.json()).then(updateStateFromBackend);
}

function startGame() {
    height = parseInt(document.getElementById('height').value);
    width = parseInt(document.getElementById('width').value);
    win = parseInt(document.getElementById('win').value);
    isMisere = document.getElementById('misere').checked;
    fetch(`/start?height=${height}&width=${width}&win=${win}&misere=${isMisere}`, {method: 'POST'})
        .then(res => res.json())
        .then(updateStateFromBackend);
    uiControls.style.display = '';
}

function aiMove() {
    if (!gameActive) return;
    const depthInput = document.getElementById('depth');
    let depth = parseInt(depthInput ? depthInput.value : '6');
    if (isNaN(depth) || depth < 1) depth = 6;
    let url = isMisere ? `/get_misere_ai_move?depth=${depth}` : `/get_ai_move?depth=${depth}`;
    fetch(url)
        .then(res => res.json())
        .then(data => {
            let move = data.move;
            if (Array.isArray(move) && move.length === 2) move = {x: move[0], y: move[1]};
            if (move && typeof move.x === 'number' && typeof move.y === 'number') {
                fetch('/move', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({x: move.x, y: move.y})
                })
                .then(res => res.json())
                .then(updateStateFromBackend);
            }
        });
}

startBtn.addEventListener('click', startGame);
undoBtn.addEventListener('click', undoMove);
restartBtn.addEventListener('click', restartGame);
aiBtn.addEventListener('click', aiMove);

// Initial state fetch
fetch('/state').then(res => res.json()).then(updateStateFromBackend);
