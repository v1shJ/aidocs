import asyncio
import pygame
import platform
from math import inf

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 300, 300
CELL_SIZE = WIDTH // 3
LINE_WIDTH = 5
FONT_SIZE = 40
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe with Minimax")
font = pygame.font.SysFont("arial", FONT_SIZE)

class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.message = ""

    def draw_board(self):
        screen.fill(WHITE)
        # Draw grid lines
        for i in range(1, 3):
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)
        # Draw X's and O's
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 'X':
                    self.draw_x(i, j)
                elif self.board[i][j] == 'O':
                    self.draw_o(i, j)
        # Draw game-over message
        if self.game_over:
            text = font.render(self.message, True, BLACK)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
        pygame.display.flip()

    def draw_x(self, row, col):
        margin = CELL_SIZE // 4
        x = col * CELL_SIZE + margin
        y = row * CELL_SIZE + margin
        pygame.draw.line(screen, RED, (x, y), (x + CELL_SIZE - 2 * margin, y + CELL_SIZE - 2 * margin), LINE_WIDTH)
        pygame.draw.line(screen, RED, (x, y + CELL_SIZE - 2 * margin), (x + CELL_SIZE - 2 * margin, y), LINE_WIDTH)

    def draw_o(self, row, col):
        margin = CELL_SIZE // 4
        center_x = col * CELL_SIZE + CELL_SIZE // 2
        center_y = row * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - margin
        pygame.draw.circle(screen, BLUE, (center_x, center_y), radius, LINE_WIDTH)

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
        best_score = -inf
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
        best_score = inf
        best_move = None
        for row, col in game.get_empty_cells():
            game.make_move(row, col, 'O')
            score, _ = minimax(game, 'X')
            game.undo_move(row, col)
            if score < best_score:
                best_score = score
                best_move = (row, col)
        return best_score, best_move

async def main():
    game = TicTacToe()
    game.draw_board()

    while True:
        if game.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    game = TicTacToe()  # Restart game
                    game.draw_board()
            await asyncio.sleep(1.0 / FPS)
            continue

        if game.current_player == 'X':
            # AI's turn
            _, move = minimax(game, 'X')
            if move:
                row, col = move
                game.make_move(row, col, 'X')
                game.current_player = 'O'
                game.draw_board()
                # Check game status
                if game.is_winner('X'):
                    game.game_over = True
                    game.message = "AI (X) Wins! Press R to Restart"
                elif game.is_draw():
                    game.game_over = True
                    game.message = "Draw! Press R to Restart"
        else:
            # Human's turn
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
                    x, y = pygame.mouse.get_pos()
                    row, col = y // CELL_SIZE, x // CELL_SIZE
                    if game.make_move(row, col, 'O'):
                        game.current_player = 'X'
                        game.draw_board()
                        # Check game status
                        if game.is_winner('O'):
                            game.game_over = True
                            game.message = "You (O) Win! Press R to Restart"
                        elif game.is_draw():
                            game.game_over = True
                            game.message = "Draw! Press R to Restart"

        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())