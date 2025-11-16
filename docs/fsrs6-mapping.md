# FSRS-6 Variable and Parameter Mapping

This document maps FSRS-6 terminology to the implementation in this application.

## Parameter Name Conventions

### Current Implementation (Post-Refactoring)

| Variable Name | Type | Range | Description |
|---------------|------|-------|-------------|
| `intensity` | float | 0-10+ | Overall learning intensity, controls pacing |
| `stabilityGrowth` | float | 0.5-2.0 | Controls stability increase rate (derived from intensity) |
| `diffAdjust` | float | 0.5-1.5 | Controls difficulty adjustment magnitude (derived from intensity) |
| `request_retention` | float | 0.5-1.0 | Target retention rate (default 0.9 = 90%) |

### Legacy Terminology (Removed)
- ❌ `alpha` → ✅ `stabilityGrowth`
- ❌ `beta` → ✅ `diffAdjust`

All code, comments, and documentation now use the new naming convention.

## FSRS-6 Core Equations

### Difficulty Update
```python
if grade_again:
    # Increase difficulty when card is forgotten
    new_difficulty = current_difficulty + (difficulty_increase * diffAdjust)
else:
    # Decrease difficulty when card is remembered
    new_difficulty = current_difficulty + (difficulty_decay * diffAdjust)

# Clamp to valid range
new_difficulty = max(1.0, min(10.0, new_difficulty))
```

**Parameters used:**
- `diffAdjust`: Multiplier that scales difficulty changes based on intensity
- `difficulty_increase`: Base increase (1.0)
- `difficulty_decay`: Base decrease (-0.5)

### Stability Update
```python
if state == 0:  # New card
    stability = initial_stability_again if grade_again else initial_stability_good
else:  # Subsequent reviews
    if grade_again:
        stability = current_stability * stability_factor_again
    else:
        difficulty_factor = 11 - difficulty  # Easier cards increase more
        base_multiplier = stability_factor_good * (difficulty_factor / 10)
        stability = current_stability * base_multiplier / stabilityGrowth
```

**Parameters used:**
- `stabilityGrowth`: Divisor that controls how fast stability grows
  - Higher values → slower growth → more frequent reviews
- `initial_stability_again`: Starting stability for failed cards (0.4 days)
- `initial_stability_good`: Starting stability for successful cards (3.0 days)
- `stability_factor_again`: Multiplier for failed reviews (0.5)
- `stability_factor_good`: Base multiplier for successful reviews (2.5)

### Interval Calculation
```python
interval = stability * (log(request_retention) / log(0.9))
interval = max(1, int(round(interval)))
```

**Parameters used:**
- `request_retention`: Target retention rate (e.g., 0.9 = 90%)
- Uses natural logarithm to calculate optimal interval

## Intensity Derivation Formulas

### stabilityGrowth Calculation
```python
stabilityGrowth = 0.5 + (intensity × 0.15)
```

**Examples:**
- intensity = 0 → stabilityGrowth = 0.5 (easiest)
- intensity = 5 → stabilityGrowth = 1.25 (balanced)
- intensity = 10 → stabilityGrowth = 2.0 (most intense)

### diffAdjust Calculation
```python
diffAdjust = 0.5 + (intensity × 0.1)
```

**Examples:**
- intensity = 0 → diffAdjust = 0.5 (gentle adjustments)
- intensity = 5 → diffAdjust = 1.0 (balanced)
- intensity = 10 → diffAdjust = 1.5 (aggressive adjustments)

## Minutes to Intensity Mapping

### Piecewise Linear Function
```python
if minutes <= 5:
    return 1.0
elif minutes <= 10:
    return 1.0 + (minutes - 5) * 0.3
elif minutes <= 20:
    return 2.5 + (minutes - 10) * 0.25
elif minutes <= 30:
    return 5.0 + (minutes - 20) * 0.2
else:
    return 7.0 + min((minutes - 30) * 0.1, 3.0)  # capped at 10.0
```

**Mapping Points:**
- 5 min → 1.0
- 10 min → 2.5
- 20 min → 5.0 (default)
- 30 min → 7.0
- 50+ min → 10.0 (capped)

## API Reference

### FSRS6Scheduler Class

#### Constructor
```python
def __init__(self, intensity: float = 5.0, request_retention: float = 0.9)
```
Creates scheduler with specified intensity and retention target.

#### Methods

##### `get_current_parameters() -> dict`
Returns dictionary with current parameters:
```python
{
    'intensity': float,
    'stabilityGrowth': float,
    'diffAdjust': float,
    'request_retention': float
}
```

##### `set_intensity(intensity: float, request_retention: float = None)`
Updates intensity and recalculates derived parameters.
- `intensity`: New intensity value (clamped to 0-10)
- `request_retention`: Optional new retention target (clamped to 0.5-1.0)

##### `schedule_card(card: Card, grade_again: bool) -> Card`
Updates card based on grade:
- `card`: Card to schedule
- `grade_again`: True for "Again", False for "Good"
- Returns: Updated card with new FSRS-6 metadata

### UserSettings Class

#### Constructor
```python
def __init__(self, user: str, base_dir: str = "data/users")
```

#### Key Methods

##### `effective_intensity() -> float`
Returns the active intensity:
- Manual override if set
- Otherwise, calculated from `minutes_per_day`

##### `set_manual_intensity(value: Optional[float])`
Sets or clears manual intensity override:
- `value=None`: Clears override
- `value>=0`: Sets override (capped at 10.0)

##### `minutes_to_intensity(minutes: int) -> float`
Converts study time to intensity using piecewise mapping.

##### `is_manual_override_active() -> bool`
Returns True if manual override is currently active.

## Data Flow

```
User Input (minutes/day or manual intensity)
    ↓
UserSettings.effective_intensity()
    ↓
FSRS6Scheduler.set_intensity(intensity)
    ↓
Calculate stabilityGrowth and diffAdjust
    ↓
Use in schedule_card() for each review
    ↓
Update card stability, difficulty, interval
```

## Storage Format

### settings.json
```json
{
  "minutes_per_day": 20,
  "request_retention": 0.9,
  "manual_intensity_override": null
}
```

When manual override is active:
```json
{
  "minutes_per_day": 20,
  "request_retention": 0.9,
  "manual_intensity_override": 7.5
}
```

### cards_metadata.json
Each card stores FSRS-6 parameters:
```json
{
  "あ": {
    "stability": 5.2,
    "difficulty": 4.8,
    "interval_days": 5,
    "lapses": 0,
    "state": 2,
    "last_seen": "2025-11-09"
  }
}
```

## Migration Notes

### From Old Naming
No migration needed - alpha/beta were never in production. This is the initial implementation with correct naming.

### Adding to Existing User Data
- Old user data (pre-intensity) will use default intensity=5.0
- settings.json created on first login if missing
- No manual migration required
