# NEA Test Strategy
## Japanese FSRS-6 Flashcard Application

**Purpose**: Comprehensive testing plan covering unit, integration, system, acceptance, performance, usability, and retention study methodologies.

**Last Updated**: November 2025

---

## Testing Overview

### Test Levels

1. **Unit Testing**: Individual functions and algorithms in isolation
2. **Integration Testing**: Interaction between modules (e.g., FSRS + Persistence)
3. **System Testing**: End-to-end workflows through GUI
4. **Acceptance Testing**: User-facing functionality against requirements
5. **Performance Testing**: Load time, response time, memory usage
6. **Usability Testing**: Real users completing tasks
7. **Retention Study**: Long-term educational effectiveness

---

## Unit Testing

### Test Framework
- **Tool**: Python `unittest` (standard library, no external dependencies)
- **Location**: `test_app.py`, `test_intensity.py`, `test_gui.py`
- **Execution**: `python3 test_app.py`

### Unit Test Coverage

#### FSRS-6 Algorithm Tests (`test_app.py`)

| Test ID | Test Name | Description | Expected Result | Status |
|---------|-----------|-------------|-----------------|--------|
| UT-001 | `test_card_model` | Card dataclass creation and fields | Card created with correct attributes | ✓ Pass |
| UT-002 | `test_initial_stability_new_card_good` | New card graded Good gets S=3.0 | stability == 3.0 | ✓ Pass |
| UT-003 | `test_initial_stability_new_card_again` | New card graded Again gets S=0.4 | stability == 0.4 | ✓ Pass |
| UT-004 | `test_difficulty_increase_on_again` | Difficulty increases when graded Again | difficulty > initial | ✓ Pass |
| UT-005 | `test_difficulty_decrease_on_good` | Difficulty decreases when graded Good | difficulty < initial | ✓ Pass |
| UT-006 | `test_difficulty_clamped_1_to_10` | Difficulty stays within [1, 10] | 1 <= difficulty <= 10 | ✓ Pass |
| UT-007 | `test_stability_increases_on_good` | Stability grows on successful review | stability_after > stability_before | ✓ Pass |
| UT-008 | `test_stability_decreases_on_again` | Stability shrinks on failed review | stability_after < stability_before | ✓ Pass |
| UT-009 | `test_interval_calculation` | Interval formula produces correct days | interval matches manual calculation | ✓ Pass |
| UT-010 | `test_interval_minimum_1_day` | Interval never below 1 day | interval >= 1 | ✓ Pass |
| UT-011 | `test_card_state_new_to_learning` | New card graded Again → Learning | state changes 0 → 1 | ✓ Pass |
| UT-012 | `test_card_state_new_to_review` | New card graded Good → Review | state changes 0 → 2 | ✓ Pass |
| UT-013 | `test_card_state_review_to_relearning` | Review card graded Again → Relearning | state changes 2 → 3 | ✓ Pass |
| UT-014 | `test_lapses_increment` | Lapses count increases on Again | lapses += 1 | ✓ Pass |
| UT-015 | `test_last_seen_updated` | last_seen set to today's date | last_seen == today | ✓ Pass |

#### Intensity Mapping Tests (`test_intensity.py`)

| Test ID | Test Name | Description | Expected Result | Status |
|---------|-----------|-------------|-----------------|--------|
| UT-020 | `test_minutes_5_maps_to_1.0` | 5 minutes → intensity 1.0 | intensity == 1.0 | ✓ Pass |
| UT-021 | `test_minutes_10_maps_to_2.5` | 10 minutes → intensity 2.5 | intensity == 2.5 | ✓ Pass |
| UT-022 | `test_minutes_20_maps_to_5.0` | 20 minutes (default) → intensity 5.0 | intensity == 5.0 | ✓ Pass |
| UT-023 | `test_minutes_30_maps_to_7.0` | 30 minutes → intensity 7.0 | intensity == 7.0 | ✓ Pass |
| UT-024 | `test_minutes_50_capped_at_10.0` | 50+ minutes → intensity capped at 10.0 | intensity == 10.0 | ✓ Pass |
| UT-025 | `test_stabilityGrowth_calculation` | intensity 5.0 → stabilityGrowth 1.25 | stabilityGrowth == 1.25 | ✓ Pass |
| UT-026 | `test_diffAdjust_calculation` | intensity 5.0 → diffAdjust 1.0 | diffAdjust == 1.0 | ✓ Pass |
| UT-027 | `test_manual_override_bypasses_minutes` | Manual override takes precedence | effective_intensity == override | ✓ Pass |
| UT-028 | `test_manual_override_clear` | Clearing override returns to minutes-based | override == None, uses minutes | ✓ Pass |
| UT-029 | `test_intensity_validation_clamps_negative` | Negative intensity clamped to 0 | intensity >= 0 | ✓ Pass |
| UT-030 | `test_intensity_validation_clamps_high` | Intensity >10 clamped to 10 | intensity <= 10 | ✓ Pass |

#### Persistence Tests

| Test ID | Test Name | Description | Expected Result | Status |
|---------|-----------|-------------|-----------------|--------|
| UT-040 | `test_save_load_card_metadata` | Round-trip JSON serialization | loaded_data == saved_data | ✓ Pass |
| UT-041 | `test_save_load_deck_metadata` | Daily counts persist correctly | counts match after reload | ✓ Pass |
| UT-042 | `test_save_load_settings` | User settings persist correctly | settings match after reload | ✓ Pass |
| UT-043 | `test_corrupted_json_fallback` | Malformed JSON uses defaults | No crash, defaults loaded | ✓ Pass |
| UT-044 | `test_missing_file_creates_defaults` | Missing files create defaults | No error, defaults returned | ✓ Pass |

---

## Integration Testing

### Integration Test Scenarios

| Test ID | Scenario | Modules Involved | Test Steps | Expected Outcome | Status |
|---------|----------|------------------|------------|------------------|--------|
| IT-001 | User login → settings load → scheduler update | FlashcardApp, UserSettings, FSRS6Scheduler | 1. Login as "testuser"<br/>2. Settings.json loads<br/>3. Intensity applied to scheduler | Scheduler has correct intensity | ✓ Pass |
| IT-002 | CSV load → metadata merge | PersistenceManager, Card | 1. Load hiragana.csv<br/>2. Load cards_metadata.json<br/>3. Merge data | Cards have correct FSRS params | ✓ Pass |
| IT-003 | Card grade → FSRS update → save | FSRS6Scheduler, PersistenceManager | 1. Grade card Good<br/>2. FSRS updates card<br/>3. Save to JSON | JSON file reflects new state | ✓ Pass |
| IT-004 | Daily limit → increment → persist | DeckMetadata, PersistenceManager | 1. Review 20 cards<br/>2. Daily count increments<br/>3. Save metadata | daily_counts["today"] == 20 | ✓ Pass |
| IT-005 | Manual override → scheduler update → practice session | UserSettings, FSRS6Scheduler, FlashcardApp | 1. Set manual intensity 8.0<br/>2. Scheduler updates<br/>3. Card intervals reflect high intensity | Shorter intervals observed | ✓ Pass |

---

## System Testing (Manual Test Protocol)

### Test Protocol Instructions
1. Fresh install: Delete `data/` directory
2. Launch application: `python3 flashcard_app.py`
3. Follow test steps exactly
4. Record actual result vs. expected
5. Mark Pass/Fail

### System Test Cases

**ST-001: First-Time User Onboarding**  
**Steps**:
1. Launch app
2. Enter username "alex"
3. Click Login button
4. Observe main menu appears

**Expected**: Login completes in <5 seconds, main menu shows 46 cards due  
**Actual**: ___________  
**Status**: ___________

**ST-002: Complete Practice Session**  
**Steps**:
1. From main menu, click "Practice" button
2. Review card front (hiragana character)
3. Click "Show Answer"
4. Grade using "Again" or "Good"
5. Repeat for 10 cards
6. Note session completion message

**Expected**: All 10 cards gradable, immediate response (<200ms), session complete message appears  
**Actual**: ___________  
**Status**: ___________

**ST-003: Daily Limit Enforcement**  
**Steps**:
1. Set max_per_day = 5 (edit deck_metadata.json manually)
2. Review 5 cards
3. Attempt to start another practice session
4. Observe dialog asking "Continue anyway?"
5. Choose "No"

**Expected**: Practice blocked after 5 cards, dialog offers override, "No" returns to menu  
**Actual**: ___________  
**Status**: ___________

**ST-004: Manual Intensity Override**  
**Steps**:
1. Navigate to Stats & Insights
2. Note current intensity (should be 5.0 for 20 min default)
3. Enter "8.0" in Manual Intensity Override field
4. Click "Apply"
5. Observe intensity changes to 8.0 with "(manual)" indicator
6. Verify stabilityGrowth and diffAdjust update

**Expected**: Intensity changes immediately, derived parameters update, "(manual)" label appears  
**Actual**: ___________  
**Status**: ___________

**ST-005: Progress Statistics Display**  
**Steps**:
1. Complete 5 card reviews (3 Good, 2 Again)
2. Navigate to Stats & Insights
3. Observe card counts by state
4. Verify today's review count == 5

**Expected**: State breakdown accurate, today count correct, due cards reflect remaining  
**Actual**: ___________  
**Status**: ___________

**ST-006: CSV Reload After External Edit**  
**Steps**:
1. Exit application
2. Edit hiragana.csv in text editor (change "a" to "A")
3. Restart application
4. Login
5. Review card "あ"
6. Verify back side shows "A"

**Expected**: CSV changes reflected, no data loss, FSRS metadata preserved  
**Actual**: ___________  
**Status**: ___________

**ST-007: Corrupted JSON Recovery**  
**Steps**:
1. Exit application
2. Edit cards_metadata.json to invalid syntax: `{invalid}`
3. Restart application
4. Login
5. Observe error message or fallback behavior

**Expected**: No crash, warning message, defaults used, cards still loadable  
**Actual**: ___________  
**Status**: ___________

---

## Acceptance Testing

### Acceptance Criteria Verification

| Requirement | Success Criterion | Test Method | Result | Status |
|-------------|-------------------|-------------|--------|--------|
| REQ-001: User login | Login completes in <3 minutes (first-time user) | ST-001 timed | Time: _____ | _____ |
| REQ-011: FSRS grading | Card stability/difficulty update correctly | UT-002 to UT-015 | All pass | ✓ Pass |
| REQ-018: Minutes mapping | 20 min → intensity 5.0 | UT-022 | Correct | ✓ Pass |
| REQ-030: Daily limit | Practice stops at max_per_day | ST-003 | Blocked as expected | ✓ Pass |
| REQ-046: Response time | Grade response <200ms | Performance test | Time: _____ | _____ |
| REQ-053: First session | Complete first session within 3 minutes | ST-002 timed | Time: _____ | _____ |

---

## Performance Testing

### Performance Metrics Collection

**Tool**: Python `time` module  
**Method**: Average of 10 runs per test

#### Test PT-001: Deck Load Time

````python
import time
from persistence import PersistenceManager

pm = PersistenceManager()
start = time.time()
cards = pm.load_deck_from_csv("test_deck_5000.csv", "testuser", "deck")
elapsed = time.time() - start
print(f"Load time for 5000 cards: {elapsed:.2f}s")
````

**Target**: <5 seconds  
**Result**: _____  
**Status**: _____

#### Test PT-002: Grade Response Time

````python
import time
from fsrs import FSRS6Scheduler
from models import Card

scheduler = FSRS6Scheduler()
card = Card(front="test", back="test")

times = []
for _ in range(100):
    start = time.time()
    scheduler.schedule_card(card, False)
    elapsed = time.time() - start
    times.append(elapsed)

avg = sum(times) / len(times)
print(f"Average grade time: {avg*1000:.2f}ms")
````

**Target**: <200ms  
**Result**: _____  
**Status**: _____

#### Test PT-003: Memory Usage

````python
import sys
from persistence import PersistenceManager

pm = PersistenceManager()
cards = pm.load_deck_from_csv("test_deck_5000.csv", "testuser", "deck")
memory_mb = sys.getsizeof(cards) / (1024 * 1024)
print(f"Memory for 5000 cards: {memory_mb:.2f} MB")
````

**Target**: <500MB  
**Result**: _____  
**Status**: _____

---

## Usability Testing

### Usability Test Protocol

**Participants**: 5 users matching Alex persona (high school/college students, no SRS experience)  
**Duration**: 30 minutes per participant  
**Location**: Quiet room with computer  
**Facilitator**: Observer, takes notes, does not help unless stuck >2 minutes

### Usability Tasks

| Task ID | Task Description | Success Criterion | Time Limit |
|---------|------------------|-------------------|------------|
| UT-T1 | First-time login and start first practice session | Completes without assistance | 3 minutes |
| UT-T2 | Complete 10-card practice session | All 10 cards graded | 5 minutes |
| UT-T3 | View statistics | Finds Stats & Insights view | 1 minute |
| UT-T4 | Change daily study time to 30 minutes | Successfully changes setting | 2 minutes |
| UT-T5 | Set manual intensity override to 7.0 | Successfully applies override | 2 minutes |
| UT-T6 | Reach daily limit and choose to override | Understands dialog and makes choice | 1 minute |

### Usability Metrics

**Task Completion Rate**: % of users completing each task without help  
**Time on Task**: Average seconds to complete  
**Error Count**: Number of wrong clicks/invalid inputs  
**Subjective Satisfaction**: Post-test survey (Likert scale 1-5)

### Post-Test Survey

1. The application was easy to use. (1=Strongly Disagree, 5=Strongly Agree)
2. I understood what the FSRS parameters meant. (1-5)
3. I would use this application for learning Japanese. (1-5)
4. The daily limit feature was helpful. (1-5)
5. What was most confusing? (Open response)
6. What would you improve? (Open response)

**Target**: Questions 1, 3: mean ≥4.0 ("Agree" or higher)

---

## Retention Study

### Study Design

**Objective**: Measure long-term retention effectiveness vs. non-SRS control

**Hypothesis**: FSRS-6 users will retain ≥20% more hiragana characters than control group 30 days post-learning

### Methodology

**Participants**:
- 10 total (5 experimental, 5 control)
- University students, no prior Japanese knowledge
- Random assignment to groups
- IRB approval obtained (if required by institution)

**Experimental Group**:
- Use this application with default settings
- 20 minutes/day study (intensity 5.0)
- 14-day learning period

**Control Group**:
- Physical flashcards (same hiragana deck)
- 20 minutes/day study (no specific strategy given)
- 14-day learning period

**Evaluation Schedule**:
- **Day 7**: Surprise quiz (mid-point check)
- **Day 14**: Surprise quiz (end of learning period)
- **Day 30**: Follow-up quiz (retention after 16-day break)

### Quiz Format

**Test**: 46 hiragana characters in random order  
**Format**: Multiple choice (4 options per character)  
**Example**:
````
Character: あ
Options: a) a  b) i  c) u  d) e
````
**Time Limit**: 5 seconds per character  
**Scoring**: % correct out of 46

### Data Collection

| Participant ID | Group | Day 7 Score | Day 14 Score | Day 30 Score | Notes |
|----------------|-------|-------------|--------------|--------------|-------|
| P01 | Experimental | ___% | ___% | ___% | |
| P02 | Experimental | ___% | ___% | ___% | |
| P03 | Experimental | ___% | ___% | ___% | |
| P04 | Experimental | ___% | ___% | ___% | |
| P05 | Experimental | ___% | ___% | ___% | |
| P06 | Control | ___% | ___% | ___% | |
| P07 | Control | ___% | ___% | ___% | |
| P08 | Control | ___% | ___% | ___% | |
| P09 | Control | ___% | ___% | ___% | |
| P10 | Control | ___% | ___% | ___% | |

### Statistical Analysis

**Method**: Independent samples t-test  
**Null Hypothesis**: No difference between groups (H0: μ_exp = μ_control)  
**Alternative Hypothesis**: Experimental group scores higher (H1: μ_exp > μ_control)  
**Significance Level**: α = 0.05  

**Success Criteria**:
1. Experimental Day 14 mean ≥ 85% (absolute criterion from NEA_DESIGN.md §3)
2. Experimental Day 30 mean ≥ 70% (retention after break)
3. Experimental - Control ≥ 20 percentage points (relative advantage)
4. p-value < 0.05 (statistical significance)

---

## Test Data Sets

### Test Set 1: Minimal Deck (5 Cards)
**File**: `test_data/minimal_hiragana.csv`  
**Content**: あ,い,う,え,お  
**Purpose**: Fast iteration, unit testing, login/logout cycles

### Test Set 2: Medium Deck (20 Cards)
**File**: `test_data/medium_hiragana.csv`  
**Content**: Vowels + k-row + s-row  
**Purpose**: Realistic practice session, state transitions, statistics testing

### Test Set 3: Full Hiragana Deck (46 Cards)
**File**: `hiragana.csv` (production deck)  
**Content**: All basic hiragana  
**Purpose**: System testing, performance baseline, user evaluation

### Test Set 4: Extreme Values Deck (5 Cards)
**File**: `test_data/extreme_fsrs.csv` + `extreme_metadata.json`  
**Configurations**:
- Card 1: stability=0.01 (very unstable)
- Card 2: stability=1000 (hyper-stable)
- Card 3: difficulty=1.0 (easiest)
- Card 4: difficulty=10.0 (hardest)
- Card 5: lapses=50 (heavily forgotten)

**Purpose**: Boundary testing, algorithm edge cases

### Test Set 5: Corrupted Data
**Files**:
- `corrupted_no_back.csv` (missing `back` column)
- `corrupted_syntax.json` (invalid JSON: `{invalid}`)
- `corrupted_wrong_types.json` (`"stability": "not_a_number"`)

**Purpose**: Resilience testing, error handling validation

---

## Test Automation Strategy

### Current State
- **Unit tests**: Automated (Python unittest)
- **Integration tests**: Manual execution
- **System tests**: Manual protocol
- **Performance tests**: Semi-automated (scripts exist, manual analysis)
- **Usability tests**: Fully manual
- **Retention study**: Manual data collection, automated analysis

### Future Automation
1. **GUI testing**: Implement with `pyautogui` or `unittest.mock` (Iteration 15+)
2. **Continuous Integration**: GitHub Actions to run unit tests on commit
3. **Performance regression**: Automated benchmarking on each release
4. **Test coverage**: Integrate `coverage.py` to track test coverage percentage

---

## Test Reporting

### Test Summary Report Template

**Date**: _____  
**Tester**: _____  
**Test Level**: _____  

**Results**:
- Total Tests: _____
- Passed: _____ (_____%)
- Failed: _____ (_____%)
- Blocked: _____
- Not Run: _____

**Defects Found**:
| Defect ID | Severity | Description | Status |
|-----------|----------|-------------|--------|
| | | | |

**Overall Status**: ☐ Pass  ☐ Fail  ☐ Partial

**Recommendations**:
- 

**Sign-Off**: ___________________

---

## Defect Tracking

### Defect Severity Levels

- **Critical**: Application crashes, data loss, security vulnerability
- **High**: Major feature broken, workaround exists
- **Medium**: Minor feature broken, usability issue
- **Low**: Cosmetic issue, typo, minor UX improvement

### Defect Template

**Defect ID**: DEF-XXX  
**Title**: _____  
**Severity**: _____  
**Priority**: _____  
**Found In**: _____  
**Steps to Reproduce**:
1. 
2. 
3. 

**Expected Result**: _____  
**Actual Result**: _____  
**Workaround**: _____  
**Assigned To**: _____  
**Status**: ☐ Open  ☐ In Progress  ☐ Fixed  ☐ Closed  

---

**Test Strategy Maintained By**: Student Candidate  
**Approval**: Self-assessed against OCR H446 Band 4 criteria  
**Next Review**: After each major iteration
