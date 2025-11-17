class Tetromino:
    def rotate(self, board):
        """Implement wall kicks and proper rotation"""
        old_rotation = self.rotation
        self.rotation = (self.rotation + 1) % 4
        
        # Test rotation with wall kicks
        for kick in self.wall_kicks[self.rotation][old_rotation]:
            new_pos = self.position + kick
            if self.is_valid_position(board, new_pos):
                self.position = new_pos
                return True
        
        # Rotation failed, revert
        self.rotation = old_rotation
        return False