class CardCounter:
    def __init__(self):
        self.running_count = 0
        self.decks_remaining = 6
        self.true_count = 0
        
    def update_count(self, card):
        """Hi-Lo card counting system"""
        if card.value in [2, 3, 4, 5, 6]:
            self.running_count += 1
        elif card.value in [10, 11, 12, 13, 1]:  # 1 is Ace
            self.running_count -= 1
            
    def get_true_count(self):
        """Calculate true count based on remaining decks"""
        self.true_count = self.running_count / self.decks_remaining
        return self.true_count