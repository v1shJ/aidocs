class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'

    def print_board(self):
        for row in self.board:
            print('|'.join(row))
            print('-' * 5)
        print()

    def is_winner(self, player):
        # Check rows
        for row in self.board:
            if all(cell == player for cell in row):
                return True
        # Check columns
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        # Check diagonals
        if all(self.board[i][i] == player for i in range(3)):
            return True
        if all(self.board[i][2-i] == player for i in range(3)):
            return True
        return False

    def is_draw(self):
        return all(cell != ' ' for row in self.board for cell in row) and not self.is_winner('X') and not self.is_winner('O')

    def is_terminal(self):
        return self.is_winner('X') or self.is_winner('O') or self.is_draw()

    def get_empty_cells(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' ']

    def make_move(self, row, col, player):
        if self.board[row][col] == ' ':
            self.board[row][col] = player
            return True
        return False

    def undo_move(self, row, col):
        self.board[row][col] = ' '

def minimax(game, player):
    """Minimax algorithm for Tic-Tac-Toe."""
    if game.is_winner('X'):
        return 1, None
    if game.is_winner('O'):
        return -1, None
    if game.is_draw():
        return 0, None

    if player == 'X':  # MAX player
        best_score = float('-inf')
        best_move = None
        for row, col in game.get_empty_cells():
            game.make_move(row, col, 'X')
            score, _ = minimax(game, 'O')
            game.undo_move(row, col)
            if score > best_score:
                best_score = score
                best_move = (row, col)
        return best_score, best_move
    else:  # MIN player
        best_score = float('inf')
        best_move = None
        for row, col in game.get_empty_cells():
            game.make_move(row, col, 'O')
            score, _ = minimax(game, 'X')
            game.undo_move(row, col)
            if score < best_score:
                best_score = score
                best_move = (row, col)
        return best_score, best_move

def play_game():
    """Play Tic-Tac-Toe: Human (O) vs AI (X)."""
    game = TicTacToe()
    print("Tic-Tac-Toe: You are O, AI is X. Enter row (0-2) and col (0-2).")
    game.print_board()

    while not game.is_terminal():
        if game.current_player == 'X':
            print("AI's turn (X)...")
            _, move = minimax(game, 'X')
            if move:
                row, col = move
                game.make_move(row, col, 'X')
                print(f"AI places X at ({row}, {col})")
            game.current_player = 'O'
        else:
            row = int(input("Enter row (0-2): "))
            col = int(input("Enter col (0-2): "))
            if not game.make_move(row, col, 'O'):
                print("Invalid move. Try again.")
                continue
            game.current_player = 'X'
        game.print_board()

    if game.is_winner('X'):
        print("AI (X) wins!")
    elif game.is_winner('O'):
        print("You (O) win!")
    else:
        print("It's a draw!")

if __name__ == "__main__":
    play_game()