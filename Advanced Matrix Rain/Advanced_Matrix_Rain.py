import pygame
import random
import math

class AdvancedMatrixRain:
    def __init__(self):
        pygame.init()
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Advanced Matrix Rain")
        
        # Multiple font sizes for variation
        self.fonts = [
            pygame.font.Font(None, 12),
            pygame.font.Font(None, 14),
            pygame.font.Font(None, 16)
        ]
        
        # Extended character set
        self.chars = []
        # Katakana
        self.chars.extend([chr(int('0x30a0', 16) + i) for i in range(96)])
        # Latin letters
        self.chars.extend([chr(i) for i in range(65, 91)])  # A-Z
        self.chars.extend([chr(i) for i in range(97, 123)]) # a-z
        # Numbers and symbols
        self.chars.extend([str(i) for i in range(10)])
        self.chars.extend(['@', '#', '$', '%', '&', '*', '+', '=', '~'])
        
        self.column_width = 20
        self.columns = self.screen_width // self.column_width
        
        # More sophisticated drop system
        self.drops = []
        for i in range(self.columns):
            self.drops.append({
                'position': random.randint(-50, 0),
                'speed': random.uniform(1, 3),
                'length': random.randint(5, 30),
                'font': random.choice(self.fonts),
                'bright_head': random.randint(3, 8)
            })
        
        self.clock = pygame.time.Clock()
        self.running = True
    
    def draw_rain(self):
        self.screen.fill((0, 0, 0))
        
        for i, drop in enumerate(self.drops):
            x = i * self.column_width
            
            # Draw the drop
            for j in range(drop['length']):
                y_pos = (drop['position'] - j) * drop['font'].get_linesize()
                
                if 0 <= y_pos < self.screen_height:
                    char = random.choice(self.chars)
                    
                    # Calculate color based on position in drop
                    if j < drop['bright_head']:
                        # Bright head
                        color = (180, 255, 180)
                    else:
                        # Fading trail
                        fade = max(0, 255 - (j - drop['bright_head']) * 15)
                        color = (0, fade, 0)
                    
                    text = drop['font'].render(char, True, color)
                    self.screen.blit(text, (x, y_pos))
            
            # Update drop position
            drop['position'] += drop['speed']
            
            # Reset drop if it goes off screen
            if drop['position'] * drop['font'].get_linesize() > self.screen_height + drop['length']:
                if random.random() < 0.02:  # Random reset
                    drop['position'] = random.randint(-50, 0)
                    drop['speed'] = random.uniform(1, 3)
                    drop['length'] = random.randint(5, 30)
                    drop['font'] = random.choice(self.fonts)
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            
            self.draw_rain()
            pygame.display.flip()
            self.clock.tick(30)
        
        pygame.quit()

# Run advanced version
if __name__ == "__main__":
    matrix = AdvancedMatrixRain()
    matrix.run()