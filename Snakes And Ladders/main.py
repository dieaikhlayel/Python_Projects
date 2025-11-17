#!/usr/bin/env python3
"""
Snakes and Ladders - Main Entry Point
A comprehensive implementation of the classic board game
"""

import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game.game_engine import GameEngine
from ui.console_ui import ConsoleUI
from ui.pygame_ui import PyGameUI
from utils.config import GameConfig

def main():
    print("🎲 Welcome to Snakes and Ladders! 🎲")
    print("Choose interface:")
    print("1. Console (Terminal)")
    print("2. Graphical (Pygame)")
    
    try:
        choice = input("Enter choice (1 or 2): ").strip()
        
        config = GameConfig()
        
        if choice == "2":
            print("Launching graphical version...")
            ui = PyGameUI(config)
        else:
            print("Launching console version...")
            ui = ConsoleUI(config)
        
        game = GameEngine(config, ui)
        game.start_game()
        
    except KeyboardInterrupt:
        print("\n\nThanks for playing! 👋")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()