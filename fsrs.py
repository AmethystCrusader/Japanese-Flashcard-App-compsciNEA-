"""
FSRS-6 (Free Spaced Repetition Scheduler) implementation.
Simplified for binary grading (Again/Good).
"""
import math
from datetime import datetime, timedelta
from models import Card


class FSRS6Scheduler:
    """FSRS-6 scheduler with binary grading."""
    
    # FSRS-6 parameters (simplified default values)
    def __init__(self):
        # Initial stability for new cards (in days)
        self.initial_stability_again = 0.4
        self.initial_stability_good = 3.0
        
        # Difficulty parameters
        self.difficulty_decay = -0.5
        self.difficulty_increase = 1.0
        
        # Stability increase factors
        self.stability_factor_good = 2.5
        self.stability_factor_again = 0.5
        
        # Forgetting curve parameters
        self.request_retention = 0.9  # 90% retention target
        
    def calculate_interval(self, stability: float) -> int:
        """Calculate interval in days based on stability and retention."""
        if stability <= 0:
            return 1
        # Formula: I = S * (R^(1/(D-1)) - 1) where R is request retention
        # Simplified: I = S * ln(request_retention) / ln(0.9)
        interval = stability * (math.log(self.request_retention) / math.log(0.9))
        return max(1, int(round(interval)))
    
    def update_difficulty(self, current_difficulty: float, grade_again: bool) -> float:
        """Update difficulty based on grade."""
        if grade_again:
            # Increase difficulty when card is forgotten
            new_difficulty = current_difficulty + self.difficulty_increase
        else:
            # Decrease difficulty when card is remembered
            new_difficulty = current_difficulty + self.difficulty_decay
        
        # Clamp difficulty to [1, 10]
        return max(1.0, min(10.0, new_difficulty))
    
    def update_stability(self, current_stability: float, difficulty: float, 
                        grade_again: bool, state: int) -> float:
        """Update stability based on grade and current state."""
        if state == 0:  # New card
            # First review
            if grade_again:
                return self.initial_stability_again
            else:
                return self.initial_stability_good
        else:
            # Subsequent reviews
            if grade_again:
                # Failed review - reduce stability
                return current_stability * self.stability_factor_again
            else:
                # Successful review - increase stability
                # Factor depends on difficulty (easier cards increase more)
                difficulty_factor = 11 - difficulty  # Higher for easier cards
                return current_stability * self.stability_factor_good * (difficulty_factor / 10)
    
    def schedule_card(self, card: Card, grade_again: bool) -> Card:
        """
        Schedule a card based on binary grade.
        
        Args:
            card: The card to schedule
            grade_again: True if user graded "Again", False if "Good"
        
        Returns:
            Updated card with new FSRS-6 metadata
        """
        # Update difficulty
        card.difficulty = self.update_difficulty(card.difficulty, grade_again)
        
        # Update stability
        card.stability = self.update_stability(
            card.stability, 
            card.difficulty, 
            grade_again, 
            card.state
        )
        
        # Calculate new interval
        card.interval_days = self.calculate_interval(card.stability)
        
        # Update lapses
        if grade_again:
            card.lapses += 1
        
        # Update state
        if grade_again:
            if card.state == 0:  # New -> Learning
                card.state = 1
            else:  # Any other state -> Relearning
                card.state = 3
        else:  # Good
            if card.state == 0 or card.state == 1:  # New or Learning -> Review
                card.state = 2
            # If already in Review (2) or Relearning (3), stays in Review
            elif card.state == 3:
                card.state = 2
        
        # Update last seen
        card.last_seen = datetime.now().strftime('%Y-%m-%d')
        
        return card
    
    def is_card_due(self, card: Card) -> bool:
        """Check if a card is due for review."""
        if card.state == 0:  # New cards are always due
            return True
        
        if not card.last_seen:
            return True
        
        try:
            last_seen_date = datetime.strptime(card.last_seen, '%Y-%m-%d')
            next_review_date = last_seen_date + timedelta(days=card.interval_days)
            return datetime.now() >= next_review_date
        except (ValueError, TypeError):
            return True
    
    def get_due_cards(self, cards: list[Card]) -> list[Card]:
        """Get all cards that are due for review."""
        return [card for card in cards if self.is_card_due(card)]
