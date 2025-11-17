"""
Pygame-based Graphical User Interface
"""

import pygame
import sys
import os

class PyGameUI:
    def __init__(self, config):
        self.config = config
        self.screen = None
        self.clock = None
        self.fonts = {}
        self.colors = {
            'background': (0, 0, 0),
            'text': (255, 255, 255),
            'player_red': (255, 50, 50),
            'player_blue': (50, 50, 255),
            'player_green': (50, 255, 50),
            'player_yellow': (255, 255, 50),
            'snake': (255, 0, 0),
            'ladder': (0, 255, 0)
        }
        self.init_pygame()
    
    def init_pygame(self):
        """Initialize Pygame"""
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 700))
        pygame.display.set_caption("Snakes and Ladders")
        self.clock = pygame.time.Clock()
        
        # Load fonts
        self.fonts['large'] = pygame.font.Font(None, 48)
        self.fonts['medium'] = pygame.font.Font(None, 32)
        self.fonts['small'] = pygame.font.Font(None, 24)
    
    def show_welcome(self):
        """Show welcome screen"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False
            
            self.screen.fill(self.colors['background'])
            
            # Draw title
            title = self.fonts['large'].render("SNAKES AND LADDERS", True, self.colors['text'])
            self.screen.blit(title, (250, 200))
            
            instruction = self.fonts['medium'].render("Press ENTER to start", True, self.colors['text'])
            self.screen.blit(instruction, (350, 300))
            
            pygame.display.flip()
            self.clock.tick(60)
    
    def get_number_of_players(self, min_players, max_players):
        """Simple number input - in real implementation, would use GUI elements"""
        return 2  # Default for demo
    
    def get_player_info(self, player_num):
        """Simple player info - in real implementation, would use GUI elements"""
        names = ["Alice", "Bob", "Charlie", "Diana"]
        colors = ["red", "blue", "green", "yellow"]
        return names[player_num - 1], colors[player_num - 1]
    
    def display_game_state(self, game_engine):
        """Display game state graphically"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        self.screen.fill(self.colors['background'])
        
        # Draw board
        self.draw_board(game_engine)
        
        # Draw player info
        self.draw_player_info(game_engine)
        
        pygame.display.flip()
        self.clock.tick(60)
    
    def draw_board(self, game_engine):
        """Draw the game board"""
        board_size = 500
        cell_size = board_size // 10
        
        # Draw board background
        board_surface = pygame.Surface((board_size, board_size))
        board_surface.fill((50, 50, 50))
        
        # Draw cells
        for i in range(1, 101):
            row, col = game_engine.board.get_cell_coordinates(i)
            x = col * cell_size
            y = (9 - row) * cell_size  # Flip Y axis
            
            # Cell color based on position
            color = (200, 200, 200) if (row + col) % 2 == 0 else (150, 150, 150)
            pygame.draw.rect(board_surface, color, (x, y, cell_size, cell_size))
            
            # Cell number
            number = self.fonts['small'].render(str(i), True, (0, 0, 0))
            board_surface.blit(number, (x + 5, y + 5))
        
        self.screen.blit(board_surface, (50, 50))
    
    def draw_player_info(self, game_engine):
        """Draw player information panel"""
        panel_x = 600
        panel_y = 50
        
        # Current player
        current_player = game_engine.player_manager.get_current_player()
        current_text = self.fonts['medium'].render(
            f"Current: {current_player.name}", 
            True, 
            self.colors['text']
        )
        self.screen.blit(current_text, (panel_x, panel_y))
        
        # Player list
        for i, player in enumerate(game_engine.player_manager.get_ranking()):
            player_text = self.fonts['small'].render(
                f"{i+1}. {player.name}: Position {player.position}", 
                True, 
                self.colors['text']
            )
            self.screen.blit(player_text, (panel_x, panel_y + 50 + i * 30))
    
    def show_message(self, message):
        """Show message on screen"""
        print(f"Pygame UI: {message}")  # For now, just print
    
    def show_dice_roll(self, player, dice_roll):
        """Show dice roll graphically"""
        print(f"Pygame UI: {player.name} rolled {dice_roll}")
    
    def show_winner(self, winner, turn_history):
        """Show winner screen"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    running = False
            
            self.screen.fill(self.colors['background'])
            
            winner_text = self.fonts['large'].render(
                f"{winner.name} WINS!", 
                True, 
                self.colors['text']
            )
            self.screen.blit(winner_text, (300, 300))
            
            pygame.display.flip()
            self.clock.tick(60)