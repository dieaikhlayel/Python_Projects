"""
Snakes and Ladders Game Package
"""

__version__ = "1.0.0"
__author__ = "My-Fun-Projects"
__description__ = "A comprehensive Snakes and Ladders implementation"

from .board import Board
from .player import Player, PlayerManager
from .dice import Dice, SpecialDice
from .snakes_ladders import Snake, Ladder, SnakeLadderManager
from .game_engine import GameEngine

__all__ = [
    'Board',
    'Player', 
    'PlayerManager',
    'Dice',
    'SpecialDice',
    'Snake',
    'Ladder',
    'SnakeLadderManager',
    'GameEngine'
]