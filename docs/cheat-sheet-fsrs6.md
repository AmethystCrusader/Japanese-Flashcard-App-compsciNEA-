# FSRS-6 Quick Reference Cheat Sheet

## Core Parameters

### Intensity
- **Range**: 0 - 10+ (typically 0-10)
- **Default**: 5.0 (balanced)
- **Effect**: Controls overall learning pace
  - Lower (0-3): Relaxed, longer intervals, less frequent reviews
  - Medium (4-6): Balanced learning pace
  - Higher (7-10): Intense, shorter intervals, more frequent reviews

### stabilityGrowth
- **Range**: 0.5 - 2.0
- **Derived from**: Intensity
- **Formula**: `stabilityGrowth = 0.5 + (intensity × 0.15)`
- **Effect**: Acts as divisor in stability calculations
  - Higher value → slower stability growth → shorter intervals
  - Lower value → faster stability growth → longer intervals

### diffAdjust
- **Range**: 0.5 - 1.5
- **Derived from**: Intensity  
- **Formula**: `diffAdjust = 0.5 + (intensity × 0.1)`
- **Effect**: Multiplier for difficulty adjustments
  - Higher value → larger difficulty changes on mistakes/successes
  - Lower value → gentler difficulty changes

### request_retention
- **Range**: 0.5 - 1.0 (typically 0.8-0.95)
- **Default**: 0.9 (90% retention)
- **Effect**: Target probability of recalling a card
  - Higher → shorter intervals (more reviews to maintain high retention)
  - Lower → longer intervals (accepts more forgetting)

## Minutes to Intensity Mapping

| Minutes/Day | Intensity | stabilityGrowth | diffAdjust | Description |
|-------------|-----------|-----------------|------------|-------------|
| ≤ 5         | 1.0       | 0.65            | 0.60       | Very relaxed |
| 10          | 2.5       | 0.88            | 0.75       | Light |
| 15          | 3.75      | 1.06            | 0.88       | Moderate |
| 20          | 5.0       | 1.25            | 1.00       | Balanced (default) |
| 25          | 6.0       | 1.40            | 1.10       | Active |
| 30          | 7.0       | 1.55            | 1.20       | Intense |
| 40+         | 9.0+      | 1.85+           | 1.40+      | Very intense |

## Manual Intensity Override

### How to Use
1. Go to **Stats & Insights** view
2. Scroll to **FSRS-6 Learning Parameters** section
3. Enter desired intensity in "Manual Intensity Override" field
4. Click **Apply** button
5. Intensity marked as "(manual)" when override is active

### Validation Rules
- **Minimum**: 0.0 (clamped)
- **Warning threshold**: 10.0
- **Maximum**: 10.0 (values >10 are capped with user confirmation)
- **Format**: Floating point number (e.g., 7.5, 3.25)

### Clearing Override
- Click **Clear Override** button (appears when override is active)
- Returns to minutes-based intensity calculation
- Changes take effect immediately

## Card States

| State | Value | Description |
|-------|-------|-------------|
| New | 0 | Never reviewed |
| Learning | 1 | First review failed |
| Review | 2 | Successfully learned |
| Relearning | 3 | Previously learned, then failed |

## Scheduler Methods

### `schedule_card(card, grade_again)`
Updates card based on binary grade:
- `grade_again=True`: "Again" (forgot card)
- `grade_again=False`: "Good" (remembered card)

### `get_current_parameters()`
Returns current scheduler configuration:
```python
{
    'intensity': 5.0,
    'stabilityGrowth': 1.25,
    'diffAdjust': 1.0,
    'request_retention': 0.9
}
```

### `set_intensity(intensity, request_retention=None)`
Updates intensity and recalculates derived parameters.

## Settings Persistence

Settings stored in: `data/users/{username}/settings.json`

```json
{
  "minutes_per_day": 20,
  "request_retention": 0.9,
  "manual_intensity_override": null
}
```

### To Reset Settings
Delete `settings.json` file or entire user directory:
```bash
rm data/users/{username}/settings.json
```

## Quick Tips

1. **Start with defaults** (20 min/day, intensity 5.0)
2. **Adjust gradually** - change intensity by ±1-2 at a time
3. **Give it time** - wait a few days to see effects before adjusting again
4. **Monitor daily progress** - check if you're hitting your review targets
5. **Manual override for short-term changes** - exam prep, vacation, etc.
6. **Higher intensity ≠ better** - find sustainable pace for long-term retention
