"""
Data models for flashcard application.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Card:
    """Represents a single flashcard with FSRS-6 metadata."""
    front: str
    back: str
    state: int = 0  # 0=new, 1=learning, 2=review, 3=relearning
    last_seen: Optional[str] = None
    
    # FSRS-6 metadata
    stability: float = 0.0  # S in days
    difficulty: float = 5.0  # D: 1-10 scale
    interval_days: int = 0
    lapses: int = 0
    
    def to_csv_row(self) -> dict:
        """Convert card to CSV row format."""
        return {
            'front': self.front,
            'back': self.back,
            'state': str(self.state),
            'lastSeen': self.last_seen or ''
        }
    
    def to_metadata(self) -> dict:
        """Convert card to metadata format for persistence."""
        return {
            'stability': self.stability,
            'difficulty': self.difficulty,
            'interval_days': self.interval_days,
            'lapses': self.lapses,
            'state': self.state,
            'last_seen': self.last_seen
        }
    
    @classmethod
    def from_csv_and_metadata(cls, csv_row: dict, metadata: dict = None):
        """Create card from CSV row and optional metadata."""
        card = cls(
            front=csv_row['front'],
            back=csv_row['back'],
            state=int(csv_row.get('state', 0)),
            last_seen=csv_row.get('lastSeen') or None
        )
        
        if metadata:
            card.stability = metadata.get('stability', 0.0)
            card.difficulty = metadata.get('difficulty', 5.0)
            card.interval_days = metadata.get('interval_days', 0)
            card.lapses = metadata.get('lapses', 0)
            # Override state and last_seen from metadata if present
            card.state = metadata.get('state', card.state)
            card.last_seen = metadata.get('last_seen', card.last_seen)
        
        return card


@dataclass
class DeckMetadata:
    """Global metadata for a deck."""
    max_per_day: int = 20
    daily_counts: dict = field(default_factory=dict)  # date -> count
    allow_over_limit_today: bool = False
    
    def to_dict(self) -> dict:
        """Convert to dictionary for persistence."""
        return {
            'max_per_day': self.max_per_day,
            'daily_counts': self.daily_counts,
            'allow_over_limit_today': self.allow_over_limit_today
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary."""
        return cls(
            max_per_day=data.get('max_per_day', 20),
            daily_counts=data.get('daily_counts', {}),
            allow_over_limit_today=data.get('allow_over_limit_today', False)
        )
    
    def get_today_count(self) -> int:
        """Get count of cards reviewed today."""
        today = datetime.now().strftime('%Y-%m-%d')
        return self.daily_counts.get(today, 0)
    
    def increment_today_count(self):
        """Increment today's review count."""
        today = datetime.now().strftime('%Y-%m-%d')
        self.daily_counts[today] = self.daily_counts.get(today, 0) + 1
    
    def can_review_more(self) -> bool:
        """Check if more cards can be reviewed today."""
        if self.allow_over_limit_today:
            return True
        return self.get_today_count() < self.max_per_day
