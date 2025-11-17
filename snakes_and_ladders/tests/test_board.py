"""
Unit Tests for Board Logic
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.board import Board
from game.player import Player

class TestBoard(unittest.TestCase):
    
    def setUp(self):
        self.board = Board(size=100)
    
    def test_board_initialization(self):
        self.assertEqual(self.board.size, 100)
        self.assertEqual(len(self.board.cells), 100)
    
    def test_get_cell_coordinates(self):
        # Test position 1 (bottom-left)
        row, col = self.board.get_cell_coordinates(1)
        self.assertEqual((row, col), (0, 0))
        
        # Test position 10 (bottom-right)
        row, col = self.board.get_cell_coordinates(10)
        self.assertEqual((row, col), (0, 9))
        
        # Test position 11 (second row, right side)
        row, col = self.board.get_cell_coordinates(11)
        self.assertEqual((row, col), (1, 9))
    
    def test_winning_position(self):
        self.assertTrue(self.board.is_winning_position(100))
        self.assertFalse(self.board.is_winning_position(99))
        self.assertFalse(self.board.is_winning_position(101))
    
    def test_validate_move(self):
        # Valid moves
        self.assertTrue(self.board.validate_move(95, 5))
        self.assertTrue(self.board.validate_move(50, 50))
        
        # Invalid moves (would exceed board size)
        self.assertFalse(self.board.validate_move(95, 6))
        self.assertFalse(self.board.validate_move(100, 1))

if __name__ == '__main__':
    unittest.main()