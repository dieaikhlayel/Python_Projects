"""
Dice Class and Rolling Mechanics
"""

import random
import time

class Dice:
    def __init__(self, sides=6):
        self.sides = sides
        self.last_roll = None
        self.double_count = 0
    
    def roll(self, animated=False, animation_duration=1.0):
        """Roll the dice with optional animation"""
        if animated:
            return self._roll_with_animation(animation_duration)
        else:
            result = random.randint(1, self.sides)
            self.last_roll = result
            return result
    
    def _roll_with_animation(self, duration=1.0):
        """Show dice rolling animation"""
        print("Rolling dice...", end="")
        start_time = time.time()
        
        while time.time() - start_time < duration:
            temp_roll = random.randint(1, self.sides)
            print(f"\rRolling dice... {temp_roll}", end="")
            time.sleep(0.1)
        
        result = random.randint(1, self.sides)
        self.last_roll = result
        print(f"\rDice roll: {result} 🎲")
        return result
    
    def is_double(self, roll1, roll2):
        """Check if two consecutive rolls are doubles"""
        return roll1 == roll2
    
    def get_double_bonus(self):
        """Get bonus for rolling doubles"""
        self.double_count += 1
        bonuses = {
            1: "Extra turn!",
            2: "Move forward 2 extra spaces!",
            3: "Jump to next ladder!",
        }
        return bonuses.get(self.double_count, "Triple bonus! Move 10 spaces!")
    
    def reset_double_count(self):
        """Reset double counter"""
        self.double_count = 0


class SpecialDice(Dice):
    """Dice with special effects"""
    
    def __init__(self, sides=6):
        super().__init__(sides)
        self.special_faces = {
            1: "normal",
            2: "normal", 
            3: "reverse",  # Move backward
            4: "swap",     # Swap positions with another player
            5: "teleport", # Teleport to random position
            6: "double"    # Roll again
        }
    
    def roll_special(self):
        """Roll with special effects"""
        roll = self.roll()
        effect = self.special_faces.get(roll, "normal")
        return roll, effect