"""
Game Configuration Settings
"""

class GameConfig:
    def __init__(self):
        # Board settings
        self.board_size = 100
        self.board_theme = "classic"  # classic, forest, ocean, space
        
        # Game settings
        self.max_players = 4
        self.min_players = 2
        self.winning_position = 100
        
        # Dice settings
        self.dice_sides = 6
        self.allow_double_turn = True
        
        # UI settings
        self.animation_speed = 1.0
        self.sound_enabled = True
        self.music_enabled = True
        
        # Snakes and Ladders configurations
        self.difficulty = "medium"  # easy, medium, hard
        
    def get_snakes_ladders_config(self):
        """Return snake and ladder positions based on difficulty"""
        configs = {
            "easy": {
                "ladders": {3: 22, 5: 8, 11: 26, 20: 29, 17: 4, 19: 7, 21: 9, 27: 1},
                "snakes": {25: 5, 32: 10, 35: 7, 40: 20, 43: 18, 50: 34, 54: 36, 59: 41, 66: 24, 70: 49, 75: 28, 89: 53, 99: 41}
            },
            "medium": {
                "ladders": {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100},
                "snakes": {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
            },
            "hard": {
                "ladders": {2: 23, 7: 29, 22: 41, 28: 77, 30: 32, 44: 58, 54: 69, 70: 90, 80: 83, 87: 93},
                "snakes": {27: 7, 35: 5, 39: 3, 50: 34, 59: 46, 66: 24, 73: 12, 76: 63, 89: 67, 97: 86, 99: 26}
            }
        }
        return configs.get(self.difficulty, configs["medium"])