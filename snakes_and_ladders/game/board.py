"""
Game Board Logic and Visualization
"""

class Board:
    def __init__(self, size=100, theme="classic"):
        self.size = size
        self.theme = theme
        self.cells = [i for i in range(1, size + 1)]
        
    def get_cell_coordinates(self, position):
        """Convert position to board coordinates (row, col)"""
        if position < 1 or position > self.size:
            return None
        
        row = (position - 1) // 10
        # Even rows go left to right, odd rows go right to left
        col = (position - 1) % 10
        if row % 2 == 1:  # Odd rows (from bottom)
            col = 9 - col
        
        return row, col
    
    def display_ascii(self, players, snakes_ladders_manager):
        """Display board in ASCII format"""
        print("\n" + "="*60)
        print(f"🎲 SNAKES AND LADDERS BOARD (Position 1-{self.size}) 🎲")
        print("="*60)
        
        elements = snakes_ladders_manager.get_board_elements()
        
        for row in range(9, -1, -1):  # From top to bottom
            line = ""
            for col in range(10):
                position = self._get_position_from_coords(row, col)
                
                # Check what's at this position
                cell_content = self._get_cell_content(position, players, elements)
                line += f"{cell_content:>4}"
            
            print(line)
        
        self._display_legend(players, elements)
    
    def _get_position_from_coords(self, row, col):
        """Convert board coordinates to position number"""
        if row % 2 == 0:  # Even rows (from bottom)
            return row * 10 + col + 1
        else:  # Odd rows
            return row * 10 + (9 - col) + 1
    
    def _get_cell_content(self, position, players, elements):
        """Get what to display in a cell"""
        # Check for players
        player_symbols = []
        for player in players:
            if player.position == position:
                player_symbols.append(player.name[0].upper())
        
        if player_symbols:
            return f"[{''.join(player_symbols)}]"
        
        # Check for snakes
        if position in elements['snakes']:
            return " S "
        
        # Check for ladders
        if position in elements['ladders']:
            return " L "
        
        return f"{position:2d}"
    
    def _display_legend(self, players, elements):
        """Display legend for board symbols"""
        print("\n📖 LEGEND:")
        for player in players:
            print(f"  [{player.name[0].upper()}] = {player.name} (Position: {player.position})")
        
        if elements['snakes']:
            print("  S = Snake head")
        if elements['ladders']:
            print("  L = Ladder bottom")
        
        print(f"\nSnakes: {len(elements['snakes'])} | Ladders: {len(elements['ladders'])}")
    
    def is_winning_position(self, position):
        """Check if position is the winning position"""
        return position == self.size
    
    def validate_move(self, current_position, dice_roll):
        """Validate if move is possible"""
        new_position = current_position + dice_roll
        return new_position <= self.size