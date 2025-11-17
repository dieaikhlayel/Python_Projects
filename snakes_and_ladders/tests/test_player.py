"""
Unit Tests for Player Management
"""

import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.player import Player, PlayerManager

class TestPlayer(unittest.TestCase):
    
    def setUp(self):
        self.player = Player("TestPlayer", 1, "red")
    
    def test_player_initialization(self):
        self.assertEqual(self.player.name, "TestPlayer")
        self.assertEqual(self.player.player_id, 1)
        self.assertEqual(self.player.position, 0)
        self.assertEqual(self.player.color, "red")
        self.assertFalse(self.player.has_won)
    
    def test_player_move(self):
        success, message = self.player.move(5, 100)
        self.assertTrue(success)
        self.assertEqual(self.player.position, 5)
        self.assertIn("Moved from 0 to 5", message)
    
    def test_player_move_beyond_board(self):
        self.player.position = 98
        success, message = self.player.move(5, 100)
        self.assertFalse(success)
        self.assertEqual(self.player.position, 98)  # Position shouldn't change
    
    def test_player_set_position(self):
        self.player.set_position(25)
        self.assertEqual(self.player.position, 25)
        self.assertEqual(len(self.player.history), 1)
    
    def test_player_stats(self):
        stats = self.player.get_stats()
        self.assertEqual(stats['name'], "TestPlayer")
        self.assertEqual(stats['position'], 0)
        self.assertEqual(stats['turns_taken'], 0)

class TestPlayerManager(unittest.TestCase):
    
    def setUp(self):
        self.manager = PlayerManager(max_players=4)
    
    def test_add_player(self):
        player = self.manager.add_player("Alice", "blue")
        self.assertEqual(len(self.manager.players), 1)
        self.assertEqual(player.name, "Alice")
        self.assertEqual(player.color, "blue")
    
    def test_add_too_many_players(self):
        for i in range(4):
            self.manager.add_player(f"Player{i+1}")
        
        with self.assertRaises(Exception):
            self.manager.add_player("ExtraPlayer")
    
    def test_current_player(self):
        self.manager.add_player("Player1")
        self.manager.add_player("Player2")
        
        current = self.manager.get_current_player()
        self.assertEqual(current.name, "Player1")
    
    def test_next_turn(self):
        self.manager.add_player("Player1")
        self.manager.add_player("Player2")
        self.manager.add_player("Player3")
        
        # First call should return Player2
        next_player = self.manager.next_turn()
        self.assertEqual(next_player.name, "Player2")
        
        # Second call should return Player3
        next_player = self.manager.next_turn()
        self.assertEqual(next_player.name, "Player3")
        
        # Third call should wrap around to Player1
        next_player = self.manager.next_turn()
        self.assertEqual(next_player.name, "Player1")
    
    def test_ranking(self):
        players = []
        players.append(self.manager.add_player("Player1"))
        players.append(self.manager.add_player("Player2"))
        players.append(self.manager.add_player("Player3"))
        
        players[0].position = 10
        players[1].position = 25
        players[2].position = 5
        
        ranking = self.manager.get_ranking()
        self.assertEqual(ranking[0].name, "Player2")  # Highest position
        self.assertEqual(ranking[1].name, "Player1")
        self.assertEqual(ranking[2].name, "Player3")

if __name__ == '__main__':
    unittest.main()