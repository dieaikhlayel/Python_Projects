"""
Console-based User Interface
"""

import os
import time

class ConsoleUI:
    def __init__(self, config):
        self.config = config
    
    def clear_screen(self):
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_welcome(self):
        """Show welcome message"""
        self.clear_screen()
        print("🎲" * 20)
        print("      SNAKES AND LADDERS")
        print("🎲" * 20)
        print()
    
    def get_number_of_players(self, min_players, max_players):
        """Get number of players from user"""
        while True:
            try:
                num = int(input(f"Enter number of players ({min_players}-{max_players}): "))
                if min_players <= num <= max_players:
                    return num
                else:
                    print(f"Please enter a number between {min_players} and {max_players}")
            except ValueError:
                print("Please enter a valid number")
    
    def get_player_info(self, player_num):
        """Get player name and color"""
        print(f"\n--- Player {player_num} ---")
        name = input("Enter player name: ").strip() or f"Player {player_num}"
        
        colors = ["red", "blue", "green", "yellow", "purple", "orange", "cyan", "pink"]
        print("Available colors: " + ", ".join(colors))
        color = input("Choose color (or press Enter for random): ").strip().lower()
        
        if color not in colors:
            color = colors[(player_num - 1) % len(colors)]
        
        return name, color
    
    def display_game_state(self, game_engine):
        """Display current game state"""
        self.clear_screen()
        
        # Show board
        game_engine.board.display_ascii(
            game_engine.player_manager.players,
            game_engine.snakes_ladders_manager
        )
        
        # Show current player info
        current_player = game_engine.player_manager.get_current_player()
        print(f"\n🎯 Current Player: {current_player.name} ({current_player.color})")
        print(f"📊 Position: {current_player.position}")
        
        # Show rankings
        print("\n🏆 CURRENT STANDINGS:")
        rankings = game_engine.player_manager.get_ranking()
        for i, player in enumerate(rankings, 1):
            print(f"  {i}. {player.name}: Position {player.position}")
        
        print("\n" + "-" * 50)
    
    def show_message(self, message):
        """Display a message to the user"""
        print(f"💬 {message}")
        time.sleep(1)
    
    def show_dice_roll(self, player, dice_roll):
        """Show dice roll animation and result"""
        print(f"\n🎲 {player.name} is rolling the dice...")
        time.sleep(0.5)
        print(f"✅ Rolled: {dice_roll}")
        time.sleep(0.5)
    
    def show_winner(self, winner, turn_history):
        """Show winner celebration"""
        self.clear_screen()
        print("🎉" * 30)
        print(f"          🏆 CONGRATULATIONS! 🏆")
        print(f"         {winner.name} WINS THE GAME!")
        print("🎉" * 30)
        
        print(f"\n🎯 Final Position: {winner.position}")
        print(f"🔄 Turns Taken: {winner.turns_taken}")
        print(f"📈 Total Game Turns: {len(turn_history)}")
        
        input("\nPress Enter to continue...")
    
    def get_user_input(self, prompt, options=None):
        """Get user input with validation"""
        while True:
            user_input = input(prompt).strip().lower()
            
            if not options or user_input in options:
                return user_input
            
            print(f"Please choose from: {', '.join(options)}")