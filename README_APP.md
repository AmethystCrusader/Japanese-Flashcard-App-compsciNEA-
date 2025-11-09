# Japanese Flashcard App - FSRS-6

## Requirements
- Python 3.8 or higher
- Tkinter (usually included with Python)

## Installation

No additional packages required - the application uses only Python standard library modules.

## Running the Application

```bash
python3 flashcard_app.py
```

Or make it executable:
```bash
chmod +x flashcard_app.py
./flashcard_app.py
```

## Features

### FSRS-6 Spaced Repetition
- **Binary Grading**: Simple "Again" or "Good" rating system
- **Per-Card Metadata**:
  - S (Stability in days)
  - D (Difficulty on 1-10 scale)
  - Interval in days
  - Lapse count
- **Smart Scheduling**: Cards are scheduled based on FSRS-6 algorithm

### User Management
- Multiple user profiles supported
- Each user has independent progress tracking
- User data stored in `data/users/{username}/{deck_name}/`

### Daily Limits
- Configurable daily review limit (default: 20 cards)
- Option to override limit for dedicated practice
- Daily progress tracking

### Statistics & Insights
- View deck statistics (new, learning, review, relearning cards)
- Average difficulty and stability metrics
- Recent activity history
- Total lapse count

### Keyboard Shortcuts
- **Space**: Show answer
- **1**: Grade "Again"
- **2**: Grade "Good"

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

### CSV Format
The `hiragana.csv` file is updated with state and lastSeen:
```csv
front,back,state,lastSeen
あ,a,2,2025-11-09
い,i,1,2025-11-09
```

States:
- 0: New
- 1: Learning
- 2: Review
- 3: Relearning

## Architecture

- `flashcard_app.py`: Main application entry point and controller
- `models.py`: Data models (Card, DeckMetadata)
- `fsrs.py`: FSRS-6 scheduler implementation
- `persistence.py`: Data persistence layer
- `gui.py`: Tkinter GUI components

## FSRS-6 Algorithm

The application implements a simplified version of FSRS-6 (Free Spaced Repetition Scheduler):

1. **Initial Stability**: New cards start with different stability values based on first grade
   - Again: 0.4 days
   - Good: 3.0 days

2. **Difficulty**: Adjusted based on performance (1-10 scale)
   - Increases when card is forgotten
   - Decreases when card is remembered

3. **Stability Update**: Based on current stability, difficulty, and grade
   - Failed reviews reduce stability
   - Successful reviews increase stability (easier cards increase more)

4. **Interval Calculation**: Based on stability and target retention (90%)

## Customization

You can adjust FSRS-6 parameters by modifying the `FSRS6Scheduler` class in `fsrs.py`:
- `initial_stability_again`: Starting stability for failed first reviews
- `initial_stability_good`: Starting stability for successful first reviews
- `difficulty_decay`: How much difficulty decreases on success
- `difficulty_increase`: How much difficulty increases on failure
- `stability_factor_good`: Stability multiplier for successful reviews
- `stability_factor_again`: Stability multiplier for failed reviews
- `request_retention`: Target retention rate (default: 90%)

Daily limit can be changed in the deck metadata file or will be configurable in future versions.
