#!/usr/bin/env python3
"""
Tests for user settings and intensity system.
"""
import sys
import os
import json
import tempfile
import shutil
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from user_settings import UserSettings
from fsrs import FSRS6Scheduler
from models import Card


def test_user_settings_initialization():
    """Test UserSettings initialization and defaults."""
    print("Testing UserSettings initialization...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        settings = UserSettings('test_user', base_dir=tmpdir)
        assert settings.minutes_per_day == 20
        assert settings.request_retention == 0.9
        assert settings.manual_intensity_override is None
        assert not settings.is_manual_override_active()
        assert settings.effective_intensity() == 5.0
    
    print("✓ UserSettings initialization tests passed")


def test_minutes_to_intensity_mapping():
    """Test minutes to intensity conversion."""
    print("Testing minutes to intensity mapping...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        settings = UserSettings('test_user', base_dir=tmpdir)
        
        # Test specific mappings
        assert settings.minutes_to_intensity(5) == 1.0
        assert settings.minutes_to_intensity(10) == 2.5
        assert settings.minutes_to_intensity(20) == 5.0
        assert settings.minutes_to_intensity(30) == 7.0
        
        # Test that higher minutes = higher intensity
        assert settings.minutes_to_intensity(15) > settings.minutes_to_intensity(10)
        assert settings.minutes_to_intensity(25) > settings.minutes_to_intensity(20)
    
    print("✓ Minutes to intensity mapping tests passed")


def test_manual_intensity_override():
    """Test manual intensity override functionality."""
    print("Testing manual intensity override...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        settings = UserSettings('test_user', base_dir=tmpdir)
        
        # Initially no override
        assert settings.effective_intensity() == 5.0  # From 20 minutes
        assert not settings.is_manual_override_active()
        
        # Set manual override
        settings.set_manual_intensity(7.5)
        assert settings.effective_intensity() == 7.5
        assert settings.is_manual_override_active()
        
        # Clear override
        settings.set_manual_intensity(None)
        assert settings.effective_intensity() == 5.0
        assert not settings.is_manual_override_active()
    
    print("✓ Manual intensity override tests passed")


def test_intensity_validation():
    """Test intensity validation and clamping."""
    print("Testing intensity validation...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        settings = UserSettings('test_user', base_dir=tmpdir)
        
        # Test clamping to 0
        settings.set_manual_intensity(-5.0)
        assert settings.effective_intensity() == 0.0
        
        # Test clamping to 10
        settings.set_manual_intensity(15.0)
        assert settings.effective_intensity() == 10.0
        
        # Test valid value
        settings.set_manual_intensity(6.5)
        assert settings.effective_intensity() == 6.5
    
    print("✓ Intensity validation tests passed")


def test_settings_persistence():
    """Test settings save and load."""
    print("Testing settings persistence...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create and configure settings
        settings1 = UserSettings('test_user', base_dir=tmpdir)
        settings1.set_minutes_per_day(30)
        settings1.set_retention(0.85)
        settings1.set_manual_intensity(8.0)
        
        # Create new instance - should load saved settings
        settings2 = UserSettings('test_user', base_dir=tmpdir)
        assert settings2.minutes_per_day == 30
        assert settings2.request_retention == 0.85
        assert settings2.manual_intensity_override == 8.0
        assert settings2.effective_intensity() == 8.0
    
    print("✓ Settings persistence tests passed")


def test_scheduler_intensity_parameters():
    """Test scheduler with different intensities."""
    print("Testing scheduler intensity parameters...")
    
    # Low intensity
    low_scheduler = FSRS6Scheduler(intensity=2.0)
    low_params = low_scheduler.get_current_parameters()
    assert low_params['intensity'] == 2.0
    assert 0.5 <= low_params['stabilityGrowth'] <= 1.0
    assert 0.5 <= low_params['diffAdjust'] <= 1.0
    
    # High intensity
    high_scheduler = FSRS6Scheduler(intensity=9.0)
    high_params = high_scheduler.get_current_parameters()
    assert high_params['intensity'] == 9.0
    assert 1.5 <= high_params['stabilityGrowth'] <= 2.0
    assert 1.2 <= high_params['diffAdjust'] <= 1.5
    
    # Verify higher intensity = higher parameters
    assert high_params['stabilityGrowth'] > low_params['stabilityGrowth']
    assert high_params['diffAdjust'] > low_params['diffAdjust']
    
    print("✓ Scheduler intensity parameter tests passed")


def test_intensity_effect_on_scheduling():
    """Test that intensity affects card scheduling."""
    print("Testing intensity effect on scheduling...")
    
    # Create card at review state with moderate difficulty
    card = Card(front="test", back="test", state=2, 
                stability=5.0, difficulty=5.0)
    
    # Schedule with low intensity
    low_scheduler = FSRS6Scheduler(intensity=1.0)
    card_copy = Card(front=card.front, back=card.back, state=card.state,
                     stability=card.stability, difficulty=card.difficulty)
    low_result = low_scheduler.schedule_card(card_copy, grade_again=False)
    
    # Schedule with high intensity
    high_scheduler = FSRS6Scheduler(intensity=10.0)
    card_copy = Card(front=card.front, back=card.back, state=card.state,
                     stability=card.stability, difficulty=card.difficulty)
    high_result = high_scheduler.schedule_card(card_copy, grade_again=False)
    
    # Higher intensity should result in shorter intervals (more reviews)
    assert low_result.interval_days > high_result.interval_days
    
    # Difficulty changes should be larger with higher intensity
    # (though this specific test might not show it clearly with good grade)
    print(f"  Low intensity (1.0): interval={low_result.interval_days} days, S={low_result.stability:.2f}")
    print(f"  High intensity (10.0): interval={high_result.interval_days} days, S={high_result.stability:.2f}")
    
    print("✓ Intensity effect on scheduling tests passed")


def test_set_intensity_method():
    """Test set_intensity method."""
    print("Testing set_intensity method...")
    
    scheduler = FSRS6Scheduler(intensity=5.0)
    
    # Change intensity
    scheduler.set_intensity(8.0)
    params = scheduler.get_current_parameters()
    assert params['intensity'] == 8.0
    assert params['stabilityGrowth'] > 1.5
    
    # Change retention too
    scheduler.set_intensity(3.0, request_retention=0.85)
    params = scheduler.get_current_parameters()
    assert params['intensity'] == 3.0
    assert params['request_retention'] == 0.85
    
    # Test clamping
    scheduler.set_intensity(15.0)
    assert scheduler.intensity == 10.0
    
    scheduler.set_intensity(-5.0)
    assert scheduler.intensity == 0.0
    
    print("✓ set_intensity method tests passed")


def test_get_current_parameters():
    """Test get_current_parameters introspection."""
    print("Testing get_current_parameters...")
    
    scheduler = FSRS6Scheduler(intensity=6.0, request_retention=0.88)
    params = scheduler.get_current_parameters()
    
    # Check all required keys present
    assert 'intensity' in params
    assert 'stabilityGrowth' in params
    assert 'diffAdjust' in params
    assert 'request_retention' in params
    
    # Check values
    assert params['intensity'] == 6.0
    assert params['request_retention'] == 0.88
    assert isinstance(params['stabilityGrowth'], float)
    assert isinstance(params['diffAdjust'], float)
    
    print("✓ get_current_parameters tests passed")


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("Running FSRS-6 Intensity System Tests")
    print("=" * 60)
    
    try:
        test_user_settings_initialization()
        test_minutes_to_intensity_mapping()
        test_manual_intensity_override()
        test_intensity_validation()
        test_settings_persistence()
        test_scheduler_intensity_parameters()
        test_intensity_effect_on_scheduling()
        test_set_intensity_method()
        test_get_current_parameters()
        
        print("=" * 60)
        print("✓ All intensity system tests passed!")
        print("=" * 60)
        return True
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
