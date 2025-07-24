class Game:
    def __init__(self):
        self.board = []
        self.height = 0
        self.width = 0
        self.win = 0
        self.rem = 0
        self.player = ''
        self.history = []
        self.misere = False

    def start(self, height: int = 3, width: int = 3, win: int = 3, misere: bool = False):
        self.board = [['.' for i in range(width)] for j in range(height)]
        self.height = height
        self.width = width
        self.win = win
        self.rem = self.height * self.width
        self.player = 'X'
        self.history = []
        self.misere = misere

    def switch(self):
        if self.player == 'X':
            self.player = 'O'
        elif self.player == 'O':
            self.player = 'X'

    def move(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height and self.board[y][x] == '.':
            self.history.append([[self.board[i][j] for j in range(self.width)] for i in range(self.height)])
            self.board[y][x] = self.player
            return True
        return False

    def undo(self):
        if len(self.history) > 0:
            self.board = self.history.pop()
            self.switch()
            self.rem += 1
            return True
        return False

    def display(self):
        print("  " + " ".join(str(i) for i in range(self.width)))
        for idx, row in enumerate(self.board):
            print(str(idx) + " " + " ".join(row))

    def check_winner(self):
        # Check all rows, columns, and diagonals for a win
        lines = []
        # Rows
        for row in self.board:
            lines.append(row)
        # Columns
        for col in range(self.width):
            lines.append([self.board[row][col] for row in range(self.height)])
        # Diagonals
        for d in range(-(self.height-1), self.width):
            diag1 = [self.board[y][x] for y in range(self.height) for x in range(self.width) if x-y == d]
            diag2 = [self.board[y][x] for y in range(self.height) for x in range(self.width) if x+y == d+self.height-1]
            if len(diag1) >= self.win:
                lines.append(diag1)
            if len(diag2) >= self.win:
                lines.append(diag2)
        for line in lines:
            for i in range(len(line) - self.win + 1):
                segment = line[i:i+self.win]
                if segment.count(segment[0]) == self.win and segment[0] != '.':
                    return segment[0]
        return None

    def get_valid_moves(self):
        return [(x, y) for y in range(self.height) for x in range(self.width) if self.board[y][x] == '.']

    def evaluate(self, player):
        opponent = 'O' if player == 'X' else 'X'
        score = 0
        # Overwhelming center bonus for 3x3 if available
        if self.height == 3 and self.width == 3:
            if self.board[1][1] == '.':
                score += 10000
            elif self.board[1][1] == player:
                score += 1000
            elif self.board[1][1] == opponent:
                score -= 1000
        # Directions: right, down, diag down-right, diag down-left
        directions = [(1,0), (0,1), (1,1), (-1,1)]
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != '.':
                    continue
                for dx, dy in directions:
                    line = []
                    for k in range(self.win):
                        nx, ny = x + dx*k, y + dy*k
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            line.append(self.board[ny][nx])
                        else:
                            break
                    if len(line) == self.win:
                        if opponent not in line:
                            count = line.count(player)
                            score += 10 ** count
                        if player not in line:
                            count = line.count(opponent)
                            score -= 10 ** count
        return score

    def minimax(self, depth, alpha, beta, player, root_player):
        winner = self.check_winner()
        if winner == root_player:
            return 100000, None
        elif winner == ('O' if root_player == 'X' else 'X'):
            return -100000, None
        elif self.rem == 0 or depth == 0:
            return self.evaluate(root_player), None
        best_move = None
        if player == root_player:
            max_eval = float('-inf')
            for x, y in self.get_valid_moves():
                self.board[y][x] = player
                self.rem -= 1
                eval, _ = self.minimax(depth-1, alpha, beta, ('O' if player == 'X' else 'X'), root_player)
                self.board[y][x] = '.'
                self.rem += 1
                if eval > max_eval:
                    max_eval = eval
                    best_move = (x, y)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for x, y in self.get_valid_moves():
                self.board[y][x] = player
                self.rem -= 1
                eval, _ = self.minimax(depth-1, alpha, beta, ('O' if player == 'X' else 'X'), root_player)
                self.board[y][x] = '.'
                self.rem += 1
                if eval < min_eval:
                    min_eval = eval
                    best_move = (x, y)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_ai_move(self, depth):
        if self.height == 3 and self.width == 3:
            depth = self.rem
        move_player = self.player
        _, move = self.minimax(depth, float('-inf'), float('inf'), move_player, move_player)
        return move

    def misere_evaluate(self, player):
        # Heavily penalize any line about to be completed by self
        # Penalize for potential completions and blocking opponent
        opponent = 'O' if player == 'X' else 'X'
        score = 0
        winner = self.check_winner()
        if winner == player:
            score -= 100000  # Losing is bad in misère
        elif winner == opponent:
            score += 100000  # Forcing opponent to lose is good
        directions = [(1,0), (0,1), (1,1), (-1,1)]
        for y in range(self.height):
            for x in range(self.width):
                for dx, dy in directions:
                    line = []
                    for k in range(self.win):
                        nx, ny = x + dx*k, y + dy*k
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            line.append(self.board[ny][nx])
                        else:
                            break
                    if len(line) == self.win:
                        # Heavily penalize if self is about to win
                        if line.count(player) == self.win - 1 and line.count('.') == 1 and opponent not in line:
                            score -= 10000
                        # Penalize for potential completions
                        if opponent not in line:
                            count = line.count(player)
                            if 0 < count < self.win:
                                score -= 100 * count
                        # Penalize for blocking opponent
                        if player in line and opponent in line:
                            if line.count(player) == 1 and line.count(opponent) >= 1:
                                score -= 10 * line.count(opponent)
        return score

    def misere_minimax(self, depth, alpha, beta, player, root_player):
        winner = self.check_winner()
        if winner == 'X':
            return 100000, None  # X wins (forces O to lose)
        elif winner == 'O':
            return -100000, None # O wins (forces X to lose)
        elif self.rem == 0 or depth == 0:
            return self.misere_evaluate(root_player), None
        valid_moves = self.get_valid_moves()
        best_move = None
        # Filter out moves that create a win for self unless all moves do
        safe_moves = []
        for x, y in valid_moves:
            self.board[y][x] = player
            self.rem -= 1
            if self.check_winner() == player:
                self.board[y][x] = '.'
                self.rem += 1
                continue
            safe_moves.append((x, y))
            self.board[y][x] = '.'
            self.rem += 1
        moves_to_consider = safe_moves if safe_moves else valid_moves
        if player == 'X':  # X maximizes
            max_eval = float('-inf')
            for x, y in moves_to_consider:
                self.board[y][x] = player
                self.rem -= 1
                eval, _ = self.misere_minimax(depth-1, alpha, beta, 'O', root_player)
                self.board[y][x] = '.'
                self.rem += 1
                if eval > max_eval:
                    max_eval = eval
                    best_move = (x, y)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:  # O minimizes
            min_eval = float('inf')
            for x, y in moves_to_consider:
                self.board[y][x] = player
                self.rem -= 1
                eval, _ = self.misere_minimax(depth-1, alpha, beta, 'X', root_player)
                self.board[y][x] = '.'
                self.rem += 1
                if eval < min_eval:
                    min_eval = eval
                    best_move = (x, y)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_misere_ai_move(self, depth):
        # Special case: 3x3, X, first move
        if self.misere and self.height == 3 and self.width == 3 and self.player == 'X':
            flat = [cell for row in self.board for cell in row]
            if flat.count('.') == 9:
                return (1, 1)
            # Mirror every O
            for y in range(3):
                for x in range(3):
                    if self.board[y][x] == 'O':
                        mx, my = 2 - x, 2 - y
                        if self.board[my][mx] == '.':
                            return (mx, my)
        move_player = self.player
        _, move = self.misere_minimax(depth, float('-inf'), float('inf'), move_player, move_player)
        return move


def main():
    print("Welcome to the Tic-Tac-Toe Solver!")
    game = Game()
    in_game = False
    misere = False
    while True:
        if not in_game:
            print("\nOptions: (1) Start new game (regular)  (2) Start new game (misère)  (3) Quit")
            choice = input("Enter your choice: ").strip()
            if choice == '1' or choice == '2':
                try:
                    h = int(input("Enter board height (default 3): ") or 3)
                    w = int(input("Enter board width (default 3): ") or 3)
                    win = int(input("Enter win threshold (default 3): ") or 3)
                except ValueError:
                    print("Invalid input. Please enter integers.")
                    continue
                misere = (choice == '2')
                game.start(h, w, win, misere)
                in_game = True
                game.display()
            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
        else:
            print("\nOptions: (1) Make move  (2) Computer move  (3) Undo  (4) Restart  (5) Quit game")
            choice = input("Enter your choice: ").strip()
            if choice == '1':
                try:
                    x = int(input(f"Enter x (0-{game.width-1}): "))
                    y = int(input(f"Enter y (0-{game.height-1}): "))
                except ValueError:
                    print("Invalid coordinates.")
                    continue
                if game.move(x, y):
                    game.rem -= 1
                    game.display()
                    winner = game.check_winner()
                    if winner:
                        if game.misere:
                            print(f"Player {winner} loses (misère)!")
                        else:
                            print(f"Player {winner} wins!")
                        in_game = False
                    elif game.rem == 0:
                        print("It's a draw!")
                        in_game = False
                    else:
                        game.switch()
                else:
                    print("Invalid move. Try again.")
            elif choice == '2':
                try:
                    depth = int(input("Enter minimax search depth (e.g., 4): "))
                except ValueError:
                    print("Invalid depth.")
                    continue
                if game.misere:
                    move = game.get_misere_ai_move(depth)
                else:
                    move = game.get_ai_move(depth)
                if move:
                    x, y = move
                    game.move(x, y)
                    game.rem -= 1
                    print(f"Computer ({game.player}) moves at ({x}, {y})")
                    game.display()
                    winner = game.check_winner()
                    if winner:
                        if game.misere:
                            print(f"Player {winner} loses (misère)!")
                        else:
                            print(f"Player {winner} wins!")
                        in_game = False
                    elif game.rem == 0:
                        print("It's a draw!")
                        in_game = False
                    else:
                        game.switch()
                else:
                    print("No valid moves left.")
            elif choice == '3':
                if game.undo():
                    game.display()
                else:
                    print("Nothing to undo.")
            elif choice == '4':
                game.start(game.height, game.width, game.win, game.misere)
                game.display()
            elif choice == '5':
                print("Game ended.")
                in_game = False
            else:
                print("Invalid choice.")


if __name__ == "__main__":
    main()
