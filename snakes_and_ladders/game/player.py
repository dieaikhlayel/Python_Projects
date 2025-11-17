"""
Player Class and Management
"""

class Player:
    def __init__(self, name, player_id, color="white"):
        self.name = name
        self.player_id = player_id
        self.position = 0  # Start at position 0 (before board)
        self.color = color
        self.skip_turns = 0
        self.has_won = False
        self.turns_taken = 0
        self.history = []  # Track position history
        
    def move(self, steps, board_size=100):
        """Move player by specified steps"""
        old_position = self.position
        new_position = self.position + steps
        
        # Can't move beyond board size
        if new_position > board_size:
            return False, f"Cannot move beyond position {board_size}"
        
        self.position = new_position
        self.history.append((old_position, new_position))
        self.turns_taken += 1
        return True, f"Moved from {old_position} to {new_position}"
    
    def set_position(self, new_position):
        """Set player to specific position (for snakes/ladders)"""
        old_position = self.position
        self.position = new_position
        self.history.append((old_position, new_position))
    
    def get_stats(self):
        """Get player statistics"""
        return {
            'name': self.name,
            'position': self.position,
            'turns_taken': self.turns_taken,
            'color': self.color,
            'has_won': self.has_won
        }
    
    def __str__(self):
        return f"Player {self.name} (Position: {self.position})"


class PlayerManager:
    def __init__(self, max_players=4):
        self.players = []
        self.current_player_index = 0
        self.max_players = max_players
    
    def add_player(self, name, color=None):
        """Add a new player to the game"""
        if len(self.players) >= self.max_players:
            raise Exception(f"Cannot add more than {self.max_players} players")
        
        colors = ["red", "blue", "green", "yellow", "purple", "orange"]
        player_color = color or colors[len(self.players) % len(colors)]
        
        player = Player(name, len(self.players) + 1, player_color)
        self.players.append(player)
        return player
    
    def get_current_player(self):
        """Get the current active player"""
        if not self.players:
            return None
        return self.players[self.current_player_index]
    
    def next_turn(self):
        """Move to next player's turn"""
        if not self.players:
            return None
        
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        
        # Skip players who have skip turns
        current_player = self.get_current_player()
        if current_player.skip_turns > 0:
            current_player.skip_turns -= 1
            return self.next_turn()  # Recursively skip
        
        return current_player
    
    def get_ranking(self):
        """Get players ranked by position (highest first)"""
        return sorted(self.players, key=lambda p: p.position, reverse=True)
    
    def reset(self):
        """Reset all players for a new game"""
        for player in self.players:
            player.position = 0
            player.skip_turns = 0
            player.has_won = False
            player.history = []
            player.turns_taken = 0
        self.current_player_index = 0