"""
Persistence layer for saving/loading deck and card data.
"""
import csv
import json
import os
from pathlib import Path
from typing import Optional
from models import Card, DeckMetadata


class PersistenceManager:
    """Manages persistence of card and deck metadata."""
    
    def __init__(self, base_dir: str = "data/users"):
        self.base_dir = Path(base_dir)
    
    def get_user_deck_dir(self, user: str, deck_name: str) -> Path:
        """Get the directory for a user's deck data."""
        return self.base_dir / user / deck_name
    
    def ensure_user_deck_dir(self, user: str, deck_name: str):
        """Ensure the user's deck directory exists."""
        deck_dir = self.get_user_deck_dir(user, deck_name)
        deck_dir.mkdir(parents=True, exist_ok=True)
        return deck_dir
    
    def save_card_metadata(self, user: str, deck_name: str, cards: list[Card]):
        """Save card metadata to JSON file."""
        deck_dir = self.ensure_user_deck_dir(user, deck_name)
        metadata_file = deck_dir / "cards_metadata.json"
        
        # Build metadata dict keyed by front side of card
        metadata = {}
        for card in cards:
            metadata[card.front] = card.to_metadata()
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    def load_card_metadata(self, user: str, deck_name: str) -> dict:
        """Load card metadata from JSON file."""
        deck_dir = self.get_user_deck_dir(user, deck_name)
        metadata_file = deck_dir / "cards_metadata.json"
        
        if not metadata_file.exists():
            return {}
        
        with open(metadata_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_deck_metadata(self, user: str, deck_name: str, deck_metadata: DeckMetadata):
        """Save deck metadata to JSON file."""
        deck_dir = self.ensure_user_deck_dir(user, deck_name)
        metadata_file = deck_dir / "deck_metadata.json"
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(deck_metadata.to_dict(), f, indent=2)
    
    def load_deck_metadata(self, user: str, deck_name: str) -> DeckMetadata:
        """Load deck metadata from JSON file."""
        deck_dir = self.get_user_deck_dir(user, deck_name)
        metadata_file = deck_dir / "deck_metadata.json"
        
        if not metadata_file.exists():
            return DeckMetadata()
        
        with open(metadata_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return DeckMetadata.from_dict(data)
    
    def load_deck_from_csv(self, csv_path: str, user: str, deck_name: str) -> list[Card]:
        """Load cards from CSV file and merge with saved metadata."""
        cards = []
        
        # Load card metadata
        card_metadata = self.load_card_metadata(user, deck_name)
        
        # Read CSV
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Get metadata for this card if it exists
                metadata = card_metadata.get(row['front'])
                card = Card.from_csv_and_metadata(row, metadata)
                cards.append(card)
        
        return cards
    
    def save_deck_to_csv(self, csv_path: str, cards: list[Card]):
        """Save cards to CSV file (only front, back, state, lastSeen)."""
        with open(csv_path, 'w', encoding='utf-8', newline='') as f:
            fieldnames = ['front', 'back', 'state', 'lastSeen']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for card in cards:
                writer.writerow(card.to_csv_row())
    
    def list_users(self) -> list[str]:
        """List all users."""
        if not self.base_dir.exists():
            return []
        return [d.name for d in self.base_dir.iterdir() if d.is_dir()]
    
    def user_exists(self, user: str) -> bool:
        """Check if a user exists."""
        return (self.base_dir / user).exists()
    
    def create_user(self, user: str):
        """Create a new user directory."""
        user_dir = self.base_dir / user
        user_dir.mkdir(parents=True, exist_ok=True)
