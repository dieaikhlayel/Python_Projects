"""
Main Game Engine - Controls game flow and rules
"""

import time
from .player import PlayerManager
from .dice import Dice
from .snakes_ladders import SnakeLadderManager
from .board import Board

class GameEngine:
    def __init__(self, config, ui):
        self.config = config
        self.ui = ui
        self.board = Board(config.board_size, config.board_theme)
        self.player_manager = PlayerManager(config.max_players)
        self.dice = Dice(config.dice_sides)
        self.snakes_ladders_manager = SnakeLadderManager(config)
        self.game_state = "setup"  # setup, playing, paused, finished
        self.winner = None
        self.turn_history = []
    
    def start_game(self):
        """Start a new game"""
        self.ui.show_welcome()
        
        # Setup players
        self.setup_players()
        
        # Main game loop
        self.game_loop()
    
    def setup_players(self):
        """Setup players for the game"""
        num_players = self.ui.get_number_of_players(
            self.config.min_players, 
            self.config.max_players
        )
        
        for i in range(num_players):
            name, color = self.ui.get_player_info(i + 1)
            self.player_manager.add_player(name, color)
        
        self.ui.show_message(f"Game started with {num_players} players!")
        self.game_state = "playing"
    
    def game_loop(self):
        """Main game loop"""
        while self.game_state == "playing":
            current_player = self.player_manager.get_current_player()
            
            # Display game state
            self.ui.display_game_state(self)
            
            # Player turn
            self.handle_player_turn(current_player)
            
            # Check for winner
            if self.check_winner(current_player):
                self.game_state = "finished"
                self.winner = current_player
                self.ui.show_winner(current_player, self.turn_history)
                break
            
            # Move to next player
            self.player_manager.next_turn()
            
            # Small delay for better UX
            time.sleep(0.5)
    
    def handle_player_turn(self, player):
        """Handle a single player's turn"""
        self.ui.show_message(f"{player.name}'s turn! Current position: {player.position}")
        
        # Roll dice
        dice_roll = self.dice.roll(animated=True)
        self.ui.show_dice_roll(player, dice_roll)
        
        # Move player
        success, message = player.move(dice_roll, self.config.board_size)
        
        if success:
            self.ui.show_message(message)
            self.turn_history.append({
                'player': player.name,
                'dice_roll': dice_roll,
                'old_position': player.position - dice_roll,
                'new_position': player.position
            })
            
            # Check for snakes and ladders
            self.check_snakes_ladders(player)
            
            # Check for special positions
            self.check_special_positions(player)
        else:
            self.ui.show_message(message)
    
    def check_snakes_ladders(self, player):
        """Check if player landed on snake or ladder"""
        element_type, element = self.snakes_ladders_manager.check_position(player.position)
        
        if element_type == "snake":
            message = element.bite(player)
            self.ui.show_message(message)
            self.turn_history[-1]['snake'] = element.head
            
        elif element_type == "ladder":
            message = element.climb(player)
            self.ui.show_message(message)
            self.turn_history[-1]['ladder'] = element.bottom
    
    def check_special_positions(self, player):
        """Check for special board positions"""
        special_positions = {
            7: "Lucky 7! Roll again!",
            13: "Unlucky 13! Skip next turn!",
            25: "Quarter mark! Move forward 5 spaces!",
            50: "Halfway there! Extra turn!",
            77: "Lucky 77! Teleport to 90!",
            100: "Winner!"
        }
        
        if player.position in special_positions:
            effect = special_positions[player.position]
            self.ui.show_message(f"🎉 Special position {player.position}: {effect}")
            
            # Apply effects
            if player.position == 13:
                player.skip_turns = 1
            elif player.position == 25:
                player.move(5, self.config.board_size)
            elif player.position == 50:
                # Extra turn handled in game loop
                pass
            elif player.position == 77:
                player.set_position(90)
    
    def check_winner(self, player):
        """Check if player has won the game"""
        if self.board.is_winning_position(player.position):
            player.has_won = True
            return True
        return False
    
    def get_game_stats(self):
        """Get current game statistics"""
        return {
            'total_turns': len(self.turn_history),
            'players': [p.get_stats() for p in self.player_manager.players],
            'current_player': self.player_manager.get_current_player().name if self.player_manager.players else None,
            'game_state': self.game_state,
            'board_size': self.config.board_size
        }
    
    def save_game(self, filename):
        """Save game state to file"""
        import json
        save_data = {
            'players': [p.__dict__ for p in self.player_manager.players],
            'current_player_index': self.player_manager.current_player_index,
            'turn_history': self.turn_history,
            'game_state': self.game_state,
            'config': self.config.__dict__
        }
        
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=2)
    
    def load_game(self, filename):
        """Load game state from file"""
        import json
        with open(filename, 'r') as f:
            save_data = json.load(f)
        
        # Recreate players
        self.player_manager.players = []
        for player_data in save_data['players']:
            player = Player(player_data['name'], player_data['player_id'], player_data['color'])
            player.__dict__.update(player_data)
            self.player_manager.players.append(player)
        
        self.player_manager.current_player_index = save_data['current_player_index']
        self.turn_history = save_data['turn_history']
        self.game_state = save_data['game_state']