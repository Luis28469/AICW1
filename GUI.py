import pygame
import sys
import time
from a1_state import State
from a3_agent import Agent
from a4_game import tester

class GameGUI:
    """Manages the Pygame window, drawing, and user input."""
    def __init__(self, rows, cols):
        pygame.init()

        # Constants 
        self.SQUARE_SIZE = 80
        self.PADDING = 20
        self.ROWS, self.COLS = rows, cols

        # Colors and Fonts
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.LIGHT_GREY = (200, 200, 200)
        self.FONT_COUNTER = pygame.font.Font(None, 48)
        self.FONT_MESSAGE = pygame.font.Font(None, 60)

        # Window Setup
        self.WIDTH = self.COLS * self.SQUARE_SIZE + 2 * self.PADDING
        self.HEIGHT = self.ROWS * self.SQUARE_SIZE + 2 * self.PADDING
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Hingers AI Game")

    def draw_board(self, state, message=""):
        """Draws the entire game board, including counters and messages."""
        self.screen.fill(self.WHITE)

        for r in range(self.ROWS):
            for c in range(self.COLS):
                x = self.PADDING + c * self.SQUARE_SIZE
                y = self.PADDING + r * self.SQUARE_SIZE
                rect = pygame.Rect(x, y, self.SQUARE_SIZE, self.SQUARE_SIZE)

                # Draw cell
                pygame.draw.rect(self.screen, self.LIGHT_GREY, rect)
                pygame.draw.rect(self.screen, self.BLACK, rect, 1)

                # Draw counter value
                counter = state.grid[r][c]
                if counter > 0:
                    text_surf = self.FONT_COUNTER.render(str(counter), True, self.BLACK)
                    text_rect = text_surf.get_rect(center=rect.center)
                    self.screen.blit(text_surf, text_rect)

        if message:
            self.draw_message(message)

        pygame.display.flip()

    def draw_message(self, text):
        text_surf = self.FONT_MESSAGE.render(text, True, (200, 0, 0))
        text_rect = text_surf.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        
        # Add a semi-transparent background for the message
        bg_rect = text_rect.inflate(20, 20)
        bg_surf = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
        bg_surf.fill((255, 255, 255, 180))

        self.screen.blit(bg_surf, bg_rect)
        self.screen.blit(text_surf, text_rect)

    def get_human_move(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if self.PADDING <= x < self.WIDTH - self.PADDING and self.PADDING <= y < self.HEIGHT - self.PADDING:
                        c = (x - self.PADDING) // self.SQUARE_SIZE
                        r = (y - self.PADDING) // self.SQUARE_SIZE
                        return (r, c)

def play_gui(game_state, agent1, agent2, mode, gui):
    players = [agent1, agent2]
    current_player_id = 0

    while True:
        # Check for game events (like closing the window)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

        # Draw the current state
        player_name = players[current_player_id].name if isinstance(players[current_player_id], Agent) else players[current_player_id]
        gui.draw_board(game_state, f"{player_name}'s Turn")

        # Check for a draw condition
        if all(cell == 0 for row in game_state.grid for cell in row):
            gui.draw_board(game_state, "Draw - All cells removed!")
            time.sleep(3)
            return "Draw"

        # Get the current player's move
        current_player = players[current_player_id]
        move = None

        if isinstance(current_player, str):  # Human player
            move = gui.get_human_move()
        else:  # AI Agent
            gui.draw_board(game_state, f"{player_name} is thinking...")
            pygame.time.wait(500)
            move = current_player.move(game_state, mode)

        # Apply the move if it's valid
        if move:
            r, c = move
            # We check validity of the move
            if game_state.make_move(r, c, player_name):
                winner = game_state.get_winner()
                if winner:
                    gui.draw_board(game_state, f"{winner} Wins!")
                    time.sleep(3)
                    return winner
                
                # Switch to the next player
                current_player_id = (current_player_id + 1) % 2
            else:
                # If move was invalid (e.g., clicking on an empty cell)
                print(f"Invalid move at {move}")
                continue


if __name__ == "__main__":
    # This will ask for difficulty, game mode, player names, etc.
    game_state, agent1, agent2, mode = tester()

    if game_state:
        #Initialize the GUI
        rows, cols = game_state.rows, game_state.columns
        gui = GameGUI(rows, cols)

        winner = play_gui(game_state, agent1, agent2, mode, gui)
        print(f"Game Over. Winner: {winner}")

    pygame.quit()
    sys.exit()