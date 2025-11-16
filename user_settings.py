"""
User settings management for FSRS-6 scheduler configuration.
Handles intensity mapping, manual overrides, and settings persistence.
"""
from typing import Optional
from pathlib import Path
import json


class UserSettings:
    """Manages user-specific FSRS-6 settings."""
    
    def __init__(self, user: str, base_dir: str = "data/users"):
        """
        Initialize user settings.
        
        Args:
            user: Username
            base_dir: Base directory for user data
        """
        self.user = user
        self.base_dir = Path(base_dir)
        self.settings_file = self.base_dir / user / "settings.json"
        
        # Default settings
        self.minutes_per_day: int = 20  # Study time in minutes
        self.request_retention: float = 0.9  # Target retention (90%)
        self.manual_intensity_override: Optional[float] = None
        
        # Load existing settings if available
        self.load()
    
    def load(self):
        """Load settings from JSON file."""
        if not self.settings_file.exists():
            return
        
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.minutes_per_day = data.get('minutes_per_day', 20)
                self.request_retention = data.get('request_retention', 0.9)
                self.manual_intensity_override = data.get('manual_intensity_override')
        except (json.JSONDecodeError, IOError):
            # If file is corrupted, use defaults
            pass
    
    def save(self):
        """Save settings to JSON file."""
        # Ensure directory exists
        self.settings_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            'minutes_per_day': self.minutes_per_day,
            'request_retention': self.request_retention,
            'manual_intensity_override': self.manual_intensity_override
        }
        
        with open(self.settings_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def minutes_to_intensity(self, minutes: int) -> float:
        """
        Map study time (minutes per day) to learning intensity.
        
        This converts daily available study time into an intensity parameter
        that controls how aggressively the scheduler spaces reviews.
        
        Args:
            minutes: Daily study time in minutes
        
        Returns:
            Intensity value (0-10+)
            
        Mapping:
            5 min  → intensity 1.0 (very relaxed)
            10 min → intensity 2.5 (relaxed)
            20 min → intensity 5.0 (balanced, default)
            30 min → intensity 7.0 (intense)
            40+ min → intensity 9.0+ (very intense)
        """
        if minutes <= 5:
            return 1.0
        elif minutes <= 10:
            return 1.0 + (minutes - 5) * 0.3  # 1.0 to 2.5
        elif minutes <= 20:
            return 2.5 + (minutes - 10) * 0.25  # 2.5 to 5.0
        elif minutes <= 30:
            return 5.0 + (minutes - 20) * 0.2  # 5.0 to 7.0
        else:
            return 7.0 + min((minutes - 30) * 0.1, 3.0)  # 7.0 to 10.0 (capped)
    
    def effective_intensity(self) -> float:
        """
        Get the effective intensity to use.
        
        Returns manual override if set, otherwise calculates from minutes_per_day.
        
        Returns:
            Effective intensity value
        """
        if self.manual_intensity_override is not None:
            return self.manual_intensity_override
        return self.minutes_to_intensity(self.minutes_per_day)
    
    def set_manual_intensity(self, value: Optional[float]):
        """
        Set manual intensity override.
        
        Args:
            value: Intensity value (>=0) or None to clear override.
                   Values >10 are capped at 10.
        """
        if value is None:
            self.manual_intensity_override = None
        else:
            # Validate and clamp
            value = max(0.0, value)
            if value > 10.0:
                value = 10.0
            self.manual_intensity_override = value
        
        self.save()
    
    def set_minutes_per_day(self, minutes: int):
        """
        Set daily study time in minutes.
        
        Args:
            minutes: Study time (>=1)
        """
        self.minutes_per_day = max(1, minutes)
        self.save()
    
    def set_retention(self, retention: float):
        """
        Set target retention rate.
        
        Args:
            retention: Retention rate (0.5-1.0)
        """
        self.request_retention = max(0.5, min(1.0, retention))
        self.save()
    
    def is_manual_override_active(self) -> bool:
        """Check if manual intensity override is active."""
        return self.manual_intensity_override is not None
    
    def to_dict(self) -> dict:
        """Convert settings to dictionary."""
        return {
            'minutes_per_day': self.minutes_per_day,
            'request_retention': self.request_retention,
            'manual_intensity_override': self.manual_intensity_override,
            'effective_intensity': self.effective_intensity(),
            'is_manual_override': self.is_manual_override_active()
        }
