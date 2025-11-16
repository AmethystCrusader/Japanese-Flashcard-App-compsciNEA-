# Japanese Flashcard App - FSRS-6

A spaced repetition flashcard application using the FSRS-6 (Free Spaced Repetition Scheduler) algorithm with adaptive learning intensity.

## Quick Start

### Requirements
- Python 3.8 or higher
- Tkinter (usually included with Python)

No additional packages required - the application uses only Python standard library modules.

### Running the Application

```bash
python3 flashcard_app.py
```

Or make it executable:
```bash
chmod +x flashcard_app.py
./flashcard_app.py
```

### First Time Setup
1. Enter a username (letters, numbers, hyphens, underscores)
2. Start with default settings (20 minutes/day, intensity 5.0)
3. Practice cards and review progress
4. Adjust intensity in Stats view if needed

## Features

### FSRS-6 Spaced Repetition
- **Binary Grading**: Simple "Again" or "Good" rating system
- **Per-Card Metadata**:
  - S (Stability in days) - how well you know the card
  - D (Difficulty on 1-10 scale) - how hard the card is for you
  - Interval in days - when to review next
  - Lapse count - how many times you've forgotten
- **Smart Scheduling**: Cards are scheduled based on FSRS-6 algorithm
- **Adaptive Intensity**: Learning pace adjusts based on available study time

### Learning Intensity System

The app uses **intensity** (0-10) to control learning pace:
- **Lower intensity** (0-3): Relaxed learning, longer intervals between reviews
- **Medium intensity** (4-6): Balanced pace (default)
- **Higher intensity** (7-10): Intensive learning, more frequent reviews

#### Automatic Intensity (Minutes-Based)
Set your daily study time, and intensity is calculated automatically:
- 5 min/day → intensity 1.0 (very relaxed)
- 10 min/day → intensity 2.5 (light)
- 20 min/day → intensity 5.0 (balanced, default)
- 30 min/day → intensity 7.0 (intense)
- 40+ min/day → intensity 9.0+ (very intense)

#### Manual Intensity Override
For more control, set intensity directly in the Stats view:
1. Go to **View Stats** → **FSRS-6 Learning Parameters**
2. Enter desired intensity (0-10+)
3. Click **Apply**
4. Clear override to return to minutes-based calculation

**Use cases for manual override:**
- Exam preparation (temporarily increase intensity)
- Vacation period (temporarily decrease intensity)
- Fine-tune learning pace beyond minutes mapping

### FSRS-6 Parameters

The intensity controls two key parameters:

#### stabilityGrowth (0.5-2.0)
- Controls how fast card stability increases
- Higher value → slower growth → more frequent reviews
- Derived from intensity: `stabilityGrowth = 0.5 + (intensity × 0.15)`

#### diffAdjust (0.5-1.5)
- Controls how much difficulty changes when you grade cards
- Higher value → larger adjustments
- Derived from intensity: `diffAdjust = 0.5 + (intensity × 0.1)`

See [docs/cheat-sheet-fsrs6.md](docs/cheat-sheet-fsrs6.md) for detailed parameter reference.

### User Management
- Multiple user profiles supported
- Each user has independent progress tracking
- User data stored in `data/users/{username}/{deck_name}/`
- Settings stored in `data/users/{username}/settings.json`

### Daily Limits vs. Extra Study
- **Daily Review Target**: Default 20 cards/day (based on deck settings)
- **Daily Cap Behavior**: 
  - App prompts when daily limit is reached
  - You can choose to continue for extra practice
  - Override persists only for current day
- **No retroactive changes**: Manual intensity changes only affect future reviews, not daily cap

### Statistics & Insights
- View deck statistics (new, learning, review, relearning cards)
- Display current FSRS-6 parameters (intensity, stabilityGrowth, diffAdjust, retention)
- Average difficulty and stability metrics
- Recent activity history (last 7 days)
- Total lapse count
- **Manual intensity override controls**

### Keyboard Shortcuts
- **Space**: Show answer
- **1**: Grade "Again" (forgot card)
- **2**: Grade "Good" (remembered card)

## Data Persistence

### Card Metadata
Stored in: `data/users/{username}/{deck_name}/cards_metadata.json`
```json
{
  "あ": {
    "stability": 3.0,
    "difficulty": 5.0,
    "interval_days": 2,
    "lapses": 0,
    "state": 2,
    "last_seen": "2025-11-09"
  }
}
```

### Deck Metadata
Stored in: `data/users/{username}/{deck_name}/deck_metadata.json`
```json
{
  "max_per_day": 20,
  "daily_counts": {
    "2025-11-09": 15
  },
  "allow_over_limit_today": false
}
```

### User Settings
Stored in: `data/users/{username}/settings.json`
```json
{
  "minutes_per_day": 20,
  "request_retention": 0.9,
  "manual_intensity_override": null
}
```

### CSV Format
The `hiragana.csv` file contains card content and is updated with state and lastSeen:
```csv
front,back,state,lastSeen
あ,a,2,2025-11-09
い,i,1,2025-11-09
```

**States:**
- 0: New (never reviewed)
- 1: Learning (first review failed)
- 2: Review (successfully learned)
- 3: Relearning (previously learned, then failed)

**CSV Requirements:**
- UTF-8 encoding (UTF-8-BOM also supported)
- Headers: `front,back,state,lastSeen`
- Place in same directory as `flashcard_app.py`

## Architecture

```
flashcard_app.py    # Main application entry point and controller
models.py           # Data models (Card, DeckMetadata)
fsrs.py             # FSRS-6 scheduler implementation
persistence.py      # Data persistence layer (JSON, CSV)
user_settings.py    # User settings and intensity management
gui.py              # Tkinter GUI components
```

## FSRS-6 Algorithm Details

The application implements FSRS-6 (Free Spaced Repetition Scheduler):

### Core Concepts

1. **Stability (S)**: How long you can remember a card (in days)
   - New cards start with S=0.4 (Again) or S=3.0 (Good)
   - Increases with successful reviews
   - Decreases with failures

2. **Difficulty (D)**: How hard the card is for you (1-10 scale)
   - Starts at 5.0 (neutral)
   - Increases when you forget (up to 10)
   - Decreases when you remember (down to 1)

3. **Interval**: Days until next review
   - Calculated from stability and target retention
   - Formula: `interval = S × (ln(retention) / ln(0.9))`

4. **Target Retention**: Probability of remembering (default 90%)
   - Higher retention → more frequent reviews
   - Lower retention → longer intervals

### How Intensity Affects Learning

**Difficulty Updates** (uses diffAdjust):
```
Forgot: D += 1.0 × diffAdjust
Remembered: D += -0.5 × diffAdjust
```

**Stability Updates** (uses stabilityGrowth):
```
Successful review:
  base_multiplier = 2.5 × (11 - D) / 10
  S_new = S_old × base_multiplier / stabilityGrowth
```

**Higher intensity means:**
- Larger difficulty adjustments (higher diffAdjust)
- Slower stability growth (higher stabilityGrowth divisor)
- More frequent reviews (shorter intervals)

See [docs/fsrs6-mapping.md](docs/fsrs6-mapping.md) for complete equations.

## Customization

### Adjusting FSRS-6 Parameters

#### Via User Interface (Recommended)
1. Go to **View Stats**
2. Adjust **Manual Intensity Override** (0-10)
3. Click **Apply**

#### Via Settings File
Edit `data/users/{username}/settings.json`:
- `minutes_per_day`: Study time for intensity calculation
- `request_retention`: Target retention rate (0.8-0.95 recommended)
- `manual_intensity_override`: Direct intensity value or `null`

#### Via Code (Advanced)
Modify constants in `fsrs.py`:
- `initial_stability_again`: Starting stability for failed cards (default: 0.4)
- `initial_stability_good`: Starting stability for successful cards (default: 3.0)
- `stability_factor_again`: Multiplier for failed reviews (default: 0.5)
- `stability_factor_good`: Base multiplier for successful reviews (default: 2.5)

### Changing Daily Limit
Edit `data/users/{username}/{deck_name}/deck_metadata.json`:
```json
{
  "max_per_day": 30
}
```

## Resetting Settings

### Reset User Settings Only
Delete the settings file:
```bash
rm data/users/{username}/settings.json
```
Settings will reset to defaults on next login.

### Reset All User Data
Delete the entire user directory:
```bash
rm -rf data/users/{username}
```
All progress and settings will be lost. The user can start fresh on next login.

### Reset Single Deck
Delete deck directory:
```bash
rm -rf data/users/{username}/{deck_name}
```
Deck will be reinitialized from CSV on next load.

## Documentation

- **[Quick Reference](docs/cheat-sheet-fsrs6.md)**: Parameter ranges, mappings, tips
- **[Parameter Mapping](docs/fsrs6-mapping.md)**: Detailed equations, API reference
- **[Flowcharts](docs/flowcharts-fsrs6.md)**: Visual flow of intensity and parameters

## Testing

Run the test suite:
```bash
python3 test_app.py
```

Tests cover:
- Card and metadata models
- FSRS-6 scheduler logic
- Persistence layer
- CSV loading

## Troubleshooting

### App won't start
- Check Python version: `python3 --version` (need 3.8+)
- Verify Tkinter: `python3 -c "import tkinter"`
- Check CSV exists: `ls hiragana.csv`

### Reviews not showing up
- Check if cards are due: state > 0 and interval has passed
- Verify daily limit not reached (or choose to continue)

### Settings not saving
- Check directory permissions: `ls -la data/users/`
- Verify JSON syntax if manually edited
- Delete corrupted settings file to reset

### Intensity changes not taking effect
- Settings apply on next login or when returning from Stats view
- Existing card schedules are not retroactively changed
- Wait for next review to see new intervals

## License

This is a student project for A-Level Computer Science NEA (Non-Exam Assessment).

## Credits

- FSRS algorithm by Jarrett Ye and contributors
- Implementation by AmethystCrusader
