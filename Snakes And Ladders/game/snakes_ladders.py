"""
Snakes and Ladders Configuration and Logic
"""

import random

class Snake:
    def __init__(self, head, tail, name=None):
        self.head = head
        self.tail = tail
        self.name = name or f"Snake {head}→{tail}"
        self.length = head - tail
    
    def bite(self, player):
        """Move player down the snake"""
        old_pos = player.position
        player.set_position(self.tail)
        return f"🐍 {self.name}! {player.name} slid from {old_pos} to {self.tail}"
    
    def __str__(self):
        return f"Snake {self.head}→{self.tail}"


class Ladder:
    def __init__(self, bottom, top, name=None):
        self.bottom = bottom
        self.top = top
        self.name = name or f"Ladder {bottom}→{top}"
        self.height = top - bottom
    
    def climb(self, player):
        """Move player up the ladder"""
        old_pos = player.position
        player.set_position(self.top)
        return f"🪜 {self.name}! {player.name} climbed from {old_pos} to {self.top}"
    
    def __str__(self):
        return f"Ladder {self.bottom}→{self.top}"


class SnakeLadderManager:
    def __init__(self, config):
        self.snakes = []
        self.ladders = []
        self.load_config(config)
    
    def load_config(self, config):
        """Load snakes and ladders from configuration"""
        sl_config = config.get_snakes_ladders_config()
        
        # Create snakes
        for head, tail in sl_config["snakes"].items():
            snake_names = ["Python Pit", "Viper Valley", "Cobra Curve", "Anaconda Abyss"]
            name = random.choice(snake_names)
            self.snakes.append(Snake(head, tail, name))
        
        # Create ladders
        for bottom, top in sl_config["ladders"].items():
            ladder_names = ["Golden Ladder", "Emerald Ascent", "Diamond Rise", "Ruby Steps"]
            name = random.choice(ladder_names)
            self.ladders.append(Ladder(bottom, top, name))
    
    def check_position(self, position):
        """Check if position has a snake or ladder"""
        for snake in self.snakes:
            if snake.head == position:
                return "snake", snake
        
        for ladder in self.ladders:
            if ladder.bottom == position:
                return "ladder", ladder
        
        return None, None
    
    def get_board_elements(self):
        """Get all snakes and ladders for board display"""
        return {
            'snakes': {s.head: s.tail for s in self.snakes},
            'ladders': {l.bottom: l.top for l in self.ladders}
        }
    
    def auto_generate(self, board_size=100, num_snakes=8, num_ladders=8):
        """Automatically generate snakes and ladders"""
        self.snakes.clear()
        self.ladders.clear()
        
        # Generate ladders (always go up)
        positions = list(range(2, board_size - 5))
        for _ in range(num_ladders):
            if not positions:
                break
            bottom = random.choice(positions)
            positions.remove(bottom)
            # Ladder should go up at least 10 spaces, but not beyond board
            min_top = min(bottom + 10, board_size)
            max_top = min(bottom + 30, board_size)
            top = random.randint(min_top, max_top)
            self.ladders.append(Ladder(bottom, top))
        
        # Generate snakes (always go down)
        positions = list(range(20, board_size))
        for _ in range(num_snakes):
            if not positions:
                break
            head = random.choice(positions)
            positions.remove(head)
            # Snake should go down at least 10 spaces, but not below 1
            min_tail = max(1, head - 30)
            max_tail = max(1, head - 10)
            tail = random.randint(min_tail, max_tail)
            self.snakes.append(Snake(head, tail))