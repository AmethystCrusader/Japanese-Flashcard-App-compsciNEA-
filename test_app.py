#!/usr/bin/env python3
"""
Test script to verify FSRS-6 implementation and persistence.
"""
import sys
import os
from datetime import datetime, timedelta

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import Card, DeckMetadata
from fsrs import FSRS6Scheduler
from persistence import PersistenceManager


def test_card_model():
    """Test Card model."""
    print("Testing Card model...")
    card = Card(front="あ", back="a", state=0)
    assert card.front == "あ"
    assert card.back == "a"
    assert card.state == 0
    assert card.stability == 0.0
    assert card.difficulty == 5.0
    
    # Test CSV conversion
    csv_row = card.to_csv_row()
    assert csv_row['front'] == "あ"
    assert csv_row['state'] == "0"
    
    # Test metadata conversion
    metadata = card.to_metadata()
    assert metadata['stability'] == 0.0
    assert metadata['difficulty'] == 5.0
    
    print("✓ Card model tests passed")


def test_deck_metadata():
    """Test DeckMetadata model."""
    print("Testing DeckMetadata model...")
    metadata = DeckMetadata()
    assert metadata.max_per_day == 20
    assert metadata.get_today_count() == 0
    assert metadata.can_review_more() == True
    
    # Test increment
    metadata.increment_today_count()
    assert metadata.get_today_count() == 1
    
    # Test serialization
    data = metadata.to_dict()
    metadata2 = DeckMetadata.from_dict(data)
    assert metadata2.max_per_day == metadata.max_per_day
    
    print("✓ DeckMetadata tests passed")


def test_fsrs_scheduler():
    """Test FSRS-6 scheduler."""
    print("Testing FSRS-6 scheduler...")
    scheduler = FSRS6Scheduler()
    
    # Test new card - Good grade
    card = Card(front="あ", back="a", state=0)
    scheduler.schedule_card(card, grade_again=False)
    
    assert card.state == 2  # Should be in Review state
    assert card.stability > 0
    assert card.interval_days > 0
    assert card.last_seen is not None
    assert card.lapses == 0
    print(f"  New card (Good): stability={card.stability:.2f}, interval={card.interval_days}, difficulty={card.difficulty:.2f}")
    
    # Test new card - Again grade
    card2 = Card(front="い", back="i", state=0)
    scheduler.schedule_card(card2, grade_again=True)
    
    assert card2.state == 1  # Should be in Learning state
    assert card2.stability > 0
    assert card2.lapses == 1
    print(f"  New card (Again): stability={card2.stability:.2f}, interval={card2.interval_days}, difficulty={card2.difficulty:.2f}")
    
    # Test review card - Good grade
    card3 = Card(front="う", back="u", state=2, stability=5.0, difficulty=5.0, interval_days=3)
    scheduler.schedule_card(card3, grade_again=False)
    
    assert card3.state == 2  # Should stay in Review state
    assert card3.stability > 5.0  # Should increase
    assert card3.difficulty < 5.0  # Should decrease
    print(f"  Review card (Good): stability={card3.stability:.2f}, interval={card3.interval_days}, difficulty={card3.difficulty:.2f}")
    
    # Test due card detection
    card4 = Card(front="え", back="e", state=0)
    assert scheduler.is_card_due(card4) == True  # New cards are always due
    
    card5 = Card(front="お", back="o", state=2, last_seen=datetime.now().strftime('%Y-%m-%d'), interval_days=1)
    assert scheduler.is_card_due(card5) == False  # Just reviewed today with 1 day interval
    
    print("✓ FSRS-6 scheduler tests passed")


def test_persistence():
    """Test persistence layer."""
    print("Testing persistence layer...")
    pm = PersistenceManager(base_dir="/tmp/test_flashcard_data")
    
    # Create test user
    test_user = "test_user"
    test_deck = "test_deck"
    pm.create_user(test_user)
    
    # Create test cards
    cards = [
        Card(front="あ", back="a", state=2, stability=3.0, difficulty=4.5),
        Card(front="い", back="i", state=1, stability=1.0, difficulty=6.0)
    ]
    
    # Save card metadata
    pm.save_card_metadata(test_user, test_deck, cards)
    
    # Load card metadata
    loaded_metadata = pm.load_card_metadata(test_user, test_deck)
    assert "あ" in loaded_metadata
    assert loaded_metadata["あ"]["stability"] == 3.0
    assert loaded_metadata["い"]["difficulty"] == 6.0
    
    # Test deck metadata
    deck_meta = DeckMetadata(max_per_day=25)
    deck_meta.increment_today_count()
    pm.save_deck_metadata(test_user, test_deck, deck_meta)
    
    loaded_deck_meta = pm.load_deck_metadata(test_user, test_deck)
    assert loaded_deck_meta.max_per_day == 25
    assert loaded_deck_meta.get_today_count() == 1
    
    print("✓ Persistence tests passed")


def test_csv_loading():
    """Test loading hiragana.csv."""
    print("Testing CSV loading...")
    pm = PersistenceManager(base_dir="/tmp/test_flashcard_data")
    
    test_user = "csv_test_user"
    test_deck = "hiragana"
    
    # Load actual hiragana.csv
    cards = pm.load_deck_from_csv("hiragana.csv", test_user, test_deck)
    
    assert len(cards) > 0
    assert cards[0].front == "あ"
    assert cards[0].back == "a"
    assert cards[0].state == 0
    
    print(f"✓ CSV loading tests passed (loaded {len(cards)} cards)")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Running FSRS-6 Flashcard App Tests")
    print("=" * 60)
    
    try:
        test_card_model()
        test_deck_metadata()
        test_fsrs_scheduler()
        test_persistence()
        test_csv_loading()
        
        print("=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
