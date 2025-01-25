import pygame
import sys
import math


BACKGROUND = (240, 248, 255)
GRID_COLOR = (100, 149, 237)
X_COLOR = (65, 105, 225)
O_COLOR = (220, 20, 60)
TEXT_COLOR = (0, 0, 0)

class RexzeaTicTacToe:
    def __init__(self, screen_width=800, screen_height=900):
        pygame.init()
        pygame.display.set_caption('Rexzea 5x5 Tic Tac Toe')
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        
        self.board_size = 5
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        
        self.cell_size = screen_width // self.board_size
        self.current_player = 'X'
        self.game_over = False
        self.winner = None

        self.title_font = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 48)
        
    def draw_board(self):
        self.screen.fill(BACKGROUND)

        title = self.title_font.render('5x5 Tic Tac Toe', True, TEXT_COLOR)
        title_rect = title.get_rect(center=(self.screen_width//2, 50))
        self.screen.blit(title, title_rect)

        for x in range(self.board_size + 1):
            pygame.draw.line(self.screen, GRID_COLOR, 
                             (x * self.cell_size, 100), 
                             (x * self.cell_size, self.screen_height), 2)
            pygame.draw.line(self.screen, GRID_COLOR, 
                             (0, x * self.cell_size + 100), 
                             (self.screen_width, x * self.cell_size + 100), 2)

        for row in range(self.board_size):
            for col in range(self.board_size):
                x = col * self.cell_size + self.cell_size // 2
                y = row * self.cell_size + 100 + self.cell_size // 2
                
                if self.board[row][col] == 'X':
                    self.draw_x(x, y)
                elif self.board[row][col] == 'O':
                    self.draw_o(x, y)
    
    def draw_x(self, x, y):
        line_width = 8
        size = self.cell_size * 0.7
        pygame.draw.line(self.screen, X_COLOR, 
                         (x - size/2, y - size/2), 
                         (x + size/2, y + size/2), line_width)
        pygame.draw.line(self.screen, X_COLOR, 
                         (x + size/2, y - size/2), 
                         (x - size/2, y + size/2), line_width)
    
    def draw_o(self, x, y):
        line_width = 8
        size = self.cell_size * 0.6
        pygame.draw.circle(self.screen, O_COLOR, (x, y), size/2, line_width)
    
    def is_winner(self, player):
        for row in range(self.board_size):
            for col in range(self.board_size - 4):
                if all(self.board[row][col+i] == player for i in range(5)):
                    return True
        
        for col in range(self.board_size):
            for row in range(self.board_size - 4):
                if all(self.board[row+i][col] == player for i in range(5)):
                    return True
        
        for row in range(self.board_size - 4):
            for col in range(self.board_size - 4):
                if all(self.board[row+i][col+i] == player for i in range(5)):
                    return True
        
        for row in range(self.board_size - 4):
            for col in range(4, self.board_size):
                if all(self.board[row+i][col-i] == player for i in range(5)):
                    return True
        
        return False
    
    def is_board_full(self):
        return all(cell != ' ' for row in self.board for cell in row)
    
    def minimax(self, depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
        if self.is_winner('O'):
            return 1
        if self.is_winner('X'):
            return -1
        if self.is_board_full() or depth == 0:
            return 0
        
        if is_maximizing:
            best_score = float('-inf')
            for row in range(self.board_size):
                for col in range(self.board_size):
                    if self.board[row][col] == ' ':
                        self.board[row][col] = 'O'
                        score = self.minimax(depth - 1, False, alpha, beta)
                        self.board[row][col] = ' '
                        best_score = max(score, best_score)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
            return best_score
        else:
            best_score = float('inf')
            for row in range(self.board_size):
                for col in range(self.board_size):
                    if self.board[row][col] == ' ':
                        self.board[row][col] = 'X'
                        score = self.minimax(depth - 1, True, alpha, beta)
                        self.board[row][col] = ' '
                        best_score = min(score, best_score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
            return best_score
    
    def get_best_move(self):
        best_score = float('-inf')
        best_move = None
        
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == ' ':
                    self.board[row][col] = 'O'
                    score = self.minimax(3, False)
                    self.board[row][col] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        
        return best_move
    
    def ai_move(self):
        move = self.get_best_move()
        if move:
            self.board[move[0]][move[1]] = 'O'
    
    def show_game_over(self):
        self.screen.fill(BACKGROUND)
        
        if self.winner:
            text = f"{self.winner} Menang!"
        else:
            text = "Permainan Seri!"
        
        game_over_text = self.font.render(text, True, TEXT_COLOR)
        text_rect = game_over_text.get_rect(center=(self.screen_width//2, self.screen_height//2))
        self.screen.blit(game_over_text, text_rect)
        
        restart_text = pygame.font.Font(None, 36).render('Tekan SPACE untuk Main Ulang', True, GRID_COLOR)
        restart_rect = restart_text.get_rect(center=(self.screen_width//2, self.screen_height//2 + 50))
        self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def reset_game(self):
        self.board = [[' ' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
    
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if not self.game_over and event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()

                    if y < 100:
                        continue
                    
                    col = x // self.cell_size
                    row = (y - 100) // self.cell_size
                    
                    if 0 <= row < self.board_size and 0 <= col < self.board_size and self.board[row][col] == ' ':
                        self.board[row][col] = 'X'
                        
                        if self.is_winner('X'):
                            self.game_over = True
                            self.winner = 'X'
                        elif self.is_board_full():
                            self.game_over = True
                        else:
                            self.ai_move()
                            
                            if self.is_winner('O'):
                                self.game_over = True
                                self.winner = 'O'
                            elif self.is_board_full():
                                self.game_over = True
                
                if self.game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.reset_game()
            
            self.draw_board()
            
            if self.game_over:
                self.show_game_over()
            
            pygame.display.update()
            clock.tick(30)

if __name__ == "__main__":
    game = RexzeaTicTacToe()
    game.run()