"""
Save and Load Game State Management
"""

import json
import os
from datetime import datetime

class SaveManager:
    def __init__(self, save_dir="saves"):
        self.save_dir = save_dir
        self.ensure_save_dir()
    
    def ensure_save_dir(self):
        """Create save directory if it doesn't exist"""
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
    
    def save_game(self, game_engine, save_name=None):
        """Save game state to file"""
        if not save_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_name = f"game_save_{timestamp}.json"
        
        save_path = os.path.join(self.save_dir, save_name)
        
        save_data = {
            'metadata': {
                'save_date': datetime.now().isoformat(),
                'game_version': '1.0',
                'total_players': len(game_engine.player_manager.players)
            },
            'game_state': {
                'players': [p.__dict__ for p in game_engine.player_manager.players],
                'current_player_index': game_engine.player_manager.current_player_index,
                'turn_history': game_engine.turn_history,
                'game_state': game_engine.game_state,
                'dice_last_roll': game_engine.dice.last_roll
            },
            'config': game_engine.config.__dict__
        }
        
        try:
            with open(save_path, 'w') as f:
                json.dump(save_data, f, indent=2)
            return True, f"Game saved as {save_name}"
        except Exception as e:
            return False, f"Error saving game: {e}"
    
    def load_game(self, save_name, game_engine):
        """Load game state from file"""
        save_path = os.path.join(self.save_dir, save_name)
        
        try:
            with open(save_path, 'r') as f:
                save_data = json.load(f)
            
            # Recreate players
            game_engine.player_manager.players = []
            for player_data in save_data['game_state']['players']:
                from game.player import Player
                player = Player(
                    player_data['name'], 
                    player_data['player_id'], 
                    player_data['color']
                )
                player.__dict__.update(player_data)
                game_engine.player_manager.players.append(player)
            
            # Restore game state
            game_engine.player_manager.current_player_index = save_data['game_state']['current_player_index']
            game_engine.turn_history = save_data['game_state']['turn_history']
            game_engine.game_state = save_data['game_state']['game_state']
            game_engine.dice.last_roll = save_data['game_state']['dice_last_roll']
            
            return True, "Game loaded successfully"
            
        except Exception as e:
            return False, f"Error loading game: {e}"
    
    def list_saves(self):
        """List all available save files"""
        saves = []
        if os.path.exists(self.save_dir):
            for file in os.listdir(self.save_dir):
                if file.endswith('.json'):
                    file_path = os.path.join(self.save_dir, file)
                    stats = os.stat(file_path)
                    save_date = datetime.fromtimestamp(stats.st_mtime)
                    saves.append({
                        'filename': file,
                        'date': save_date,
                        'size': stats.st_size
                    })
        
        return sorted(saves, key=lambda x: x['date'], reverse=True)
    
    def delete_save(self, save_name):
        """Delete a save file"""
        save_path = os.path.join(self.save_dir, save_name)
        try:
            os.remove(save_path)
            return True, "Save file deleted"
        except Exception as e:
            return False, f"Error deleting save: {e}"