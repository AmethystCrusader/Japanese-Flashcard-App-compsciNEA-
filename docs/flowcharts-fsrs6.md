# FSRS-6 Application Flowcharts

This document contains flowcharts showing how FSRS-6 parameters and intensity flow through the application.

## 1. Application Startup and Login Flow

```
┌─────────────────┐
│  Start App      │
└────────┬────────┘
         │
         v
┌─────────────────┐
│  Show Login     │
│   Screen        │
└────────┬────────┘
         │
         v
┌─────────────────┐
│ User Enters     │
│   Username      │
└────────┬────────┘
         │
         v
    ┌────┴────┐
    │ User    │
    │ Exists? │
    └────┬────┘
      No │    Yes
    ┌────v────┐    │
    │ Create  │    │
    │  User   │    │
    └────┬────┘    │
         └────┬────┘
              v
    ┌─────────────────┐
    │ Load/Create     │
    │  UserSettings   │
    │  (settings.json)│
    └────────┬────────┘
             │
             v
    ┌─────────────────┐
    │ Calculate       │
    │ Effective       │
    │ Intensity       │
    └────────┬────────┘
             │
    ┌────────┴────────────┐
    │ Manual Override?    │
    └────────┬────────────┘
        Yes  │  No
    ┌────────v────────┐  │
    │ Use manual_     │  │
    │ intensity_      │  │
    │ override        │  │
    └────────┬────────┘  │
             └────────┬──┘
             ┌────────v────────┐
             │ Use minutes_to_ │
             │ intensity()     │
             └────────┬────────┘
                      │
                      v
             ┌─────────────────┐
             │ Set Scheduler   │
             │ Intensity       │
             └────────┬────────┘
                      │
                      v
             ┌─────────────────┐
             │ Calculate       │
             │ stabilityGrowth │
             │ diffAdjust      │
             └────────┬────────┘
                      │
                      v
             ┌─────────────────┐
             │ Load Deck       │
             └────────┬────────┘
                      │
                      v
             ┌─────────────────┐
             │ Show Main Menu  │
             └─────────────────┘
```

## 2. Card Review Flow

```
┌─────────────────┐
│ User Clicks     │
│ "Practice"      │
└────────┬────────┘
         │
         v
┌─────────────────┐
│ Get Due Cards   │
│ (scheduler.     │
│  get_due_cards) │
└────────┬────────┘
         │
    ┌────v────┐
    │ Any due?│
    └────┬────┘
      No │  Yes
    ┌────v────┐    │
    │ Show    │    │
    │ Message │    │
    └─────────┘    │
                   v
         ┌─────────────────┐
         │ Check Daily     │
         │ Limit           │
         └────────┬────────┘
                  │
         ┌────────v────────┐
         │ Limit Reached?  │
         └────────┬────────┘
             Yes  │  No
         ┌────────v────────┐
         │ Ask User:       │
         │ Continue?       │
         └────────┬────────┘
              No  │  Yes
         ┌────────v────────┐
         │ Set allow_over_ │
         │ limit_today     │
         └────────┬────────┘
                  │
         ┌────────v────────┐
         │ Show Practice   │
         │ View            │
         └────────┬────────┘
                  │
         ┌────────v────────┐
         │ Display Card    │
         │ Front           │
         └────────┬────────┘
                  │
         ┌────────v────────┐
         │ User Shows      │
         │ Answer          │
         └────────┬────────┘
                  │
         ┌────────v────────┐
         │ User Grades:    │
         │ Again or Good   │
         └────────┬────────┘
                  │
                  v
         ┌─────────────────┐
         │ schedule_card() │
         │ with grade      │
         └────────┬────────┘
                  │
                  v
         ┌─────────────────┐
         │ Update          │
         │ Difficulty      │
         │ (using          │
         │  diffAdjust)    │
         └────────┬────────┘
                  │
                  v
         ┌─────────────────┐
         │ Update          │
         │ Stability       │
         │ (using          │
         │  stabilityGrowth)│
         └────────┬────────┘
                  │
                  v
         ┌─────────────────┐
         │ Calculate       │
         │ New Interval    │
         └────────┬────────┘
                  │
                  v
         ┌─────────────────┐
         │ Update State    │
         │ and Lapses      │
         └────────┬────────┘
                  │
                  v
         ┌─────────────────┐
         │ Save Card and   │
         │ Deck Metadata   │
         └────────┬────────┘
                  │
         ┌────────v────────┐
         │ More cards?     │
         └────────┬────────┘
              No  │  Yes
         ┌────────v────────┐
         │ Show next card  │
         └─────────────────┘
                  │
                  v
         ┌─────────────────┐
         │ Session         │
         │ Complete        │
         └─────────────────┘
```

## 3. Manual Intensity Override Flow

```
┌─────────────────┐
│ User Clicks     │
│ "View Stats"    │
└────────┬────────┘
         │
         v
┌─────────────────┐
│ Show Stats View │
└────────┬────────┘
         │
         v
┌─────────────────┐
│ Display Current │
│ FSRS-6 Params:  │
│ - intensity     │
│ - stabilityGrowth
│ - diffAdjust    │
│ - retention     │
└────────┬────────┘
         │
         v
┌─────────────────┐
│ Is manual       │
│ override active?│
└────────┬────────┘
     Yes │  No
┌────────v────────┐    │
│ Show intensity  │    │
│ with "(manual)" │    │
│ annotation      │    │
└────────┬────────┘    │
         └────────┬────┘
                  │
         ┌────────v────────┐
         │ Show Manual     │
         │ Intensity       │
         │ Controls        │
         └────────┬────────┘
                  │
         ┌────────v────────┐
         │ User enters     │
         │ intensity value │
         └────────┬────────┘
                  │
         ┌────────v────────┐
         │ User clicks     │
         │ "Apply"         │
         └────────┬────────┘
                  │
                  v
         ┌─────────────────┐
         │ Validate Input  │
         └────────┬────────┘
                  │
         ┌────────v────────┐
         │ Value < 0?      │
         └────────┬────────┘
             Yes  │  No
         ┌────────v────────┐
         │ Show Error      │
         │ Message         │
         └─────────────────┘
                  │
         ┌────────v────────┐
         │ Value > 10?     │
         └────────┬────────┘
             Yes  │  No
         ┌────────v────────┐
         │ Show Warning    │
         │ and Confirm     │
         └────────┬────────┘
              No  │  Yes
         ┌────────v────────┐
         │ Cap at 10.0     │
         └────────┬────────┘
                  │
         ┌────────v────────┐
         │ Save to         │
         │ settings.json:  │
         │ manual_intensity│
         │ _override       │
         └────────┬────────┘
                  │
                  v
         ┌─────────────────┐
         │ Reload Scheduler│
         │ with new        │
         │ intensity       │
         └────────┬────────┘
                  │
                  v
         ┌─────────────────┐
         │ Recalculate     │
         │ stabilityGrowth │
         │ diffAdjust      │
         └────────┬────────┘
                  │
                  v
         ┌─────────────────┐
         │ Return to       │
         │ Main Menu       │
         └─────────────────┘
```

## 4. Parameter Calculation Detail

```
┌─────────────────┐
│ intensity       │
│ (0-10+)         │
└────────┬────────┘
         │
    ┌────v─────────────────┐
    │ Calculate            │
    │ stabilityGrowth      │
    │ = 0.5 + (I × 0.15)  │
    └────────┬─────────────┘
             │
    ┌────────v─────────────┐
    │ Calculate            │
    │ diffAdjust           │
    │ = 0.5 + (I × 0.1)   │
    └────────┬─────────────┘
             │
             v
    ┌─────────────────────┐
    │ Used in Card Update:│
    └────────┬────────────┘
             │
     ┌───────v────────┐
     │ Difficulty     │
     │ Update:        │
     │ Δd × diffAdjust│
     └───────┬────────┘
             │
     ┌───────v────────┐
     │ Stability      │
     │ Update:        │
     │ S × M /        │
     │ stabilityGrowth│
     └───────┬────────┘
             │
     ┌───────v────────┐
     │ Interval       │
     │ Calculation:   │
     │ I = S × ln(R)  │
     └───────┬────────┘
             │
             v
    ┌─────────────────┐
    │ New Card State  │
    │ with updated    │
    │ S, D, Interval  │
    └─────────────────┘
```

## 5. Settings Persistence Flow

```
┌─────────────────┐
│ User Action:    │
│ - Login         │
│ - Set Manual    │
│   Intensity     │
│ - Clear Override│
└────────┬────────┘
         │
         v
┌─────────────────┐
│ UserSettings    │
│ Object          │
└────────┬────────┘
         │
    ┌────v────┐
    │ File    │
    │ Exists? │
    └────┬────┘
      No │  Yes
    ┌────v────────┐    │
    │ Create with │    │
    │ defaults    │    │
    └────┬────────┘    │
         └────┬────────┘
              v
    ┌─────────────────┐
    │ Load JSON:      │
    │ - minutes_per_  │
    │   day (20)      │
    │ - request_      │
    │   retention(0.9)│
    │ - manual_       │
    │   intensity_    │
    │   override(null)│
    └────────┬────────┘
             │
    ┌────────v────────┐
    │ When Changed:   │
    └────────┬────────┘
             │
    ┌────────v────────┐
    │ Update in-memory│
    │ values          │
    └────────┬────────┘
             │
    ┌────────v────────┐
    │ Call save()     │
    └────────┬────────┘
             │
    ┌────────v────────┐
    │ Write JSON to:  │
    │ data/users/     │
    │ {user}/         │
    │ settings.json   │
    └─────────────────┘
```

## 6. Intensity Impact on Review Timing

```
Lower Intensity (e.g., 2.0)
┌─────────────────────────────┐
│ stabilityGrowth = 0.80      │
│ diffAdjust = 0.70           │
└────────┬────────────────────┘
         │
         v
    Successful Review
         │
         v
┌─────────────────────────────┐
│ S: 5.0 → 8.5 days           │
│ (faster stability growth)   │
└────────┬────────────────────┘
         │
         v
┌─────────────────────────────┐
│ Next review in ~8-9 days    │
│ (longer interval)           │
└─────────────────────────────┘


Medium Intensity (e.g., 5.0)
┌─────────────────────────────┐
│ stabilityGrowth = 1.25      │
│ diffAdjust = 1.00           │
└────────┬────────────────────┘
         │
         v
    Successful Review
         │
         v
┌─────────────────────────────┐
│ S: 5.0 → 6.5 days           │
│ (balanced growth)           │
└────────┬────────────────────┘
         │
         v
┌─────────────────────────────┐
│ Next review in ~6-7 days    │
│ (balanced interval)         │
└─────────────────────────────┘


Higher Intensity (e.g., 9.0)
┌─────────────────────────────┐
│ stabilityGrowth = 1.85      │
│ diffAdjust = 1.40           │
└────────┬────────────────────┘
         │
         v
    Successful Review
         │
         v
┌─────────────────────────────┐
│ S: 5.0 → 4.4 days           │
│ (slower stability growth)   │
└────────┬────────────────────┘
         │
         v
┌─────────────────────────────┐
│ Next review in ~4-5 days    │
│ (shorter interval)          │
└─────────────────────────────┘
```

## Legend

- `┌─────┐` Box: Process or state
- `│` Vertical line: Flow continues
- `v` Arrow: Direction of flow
- `┬` Split: Decision or multiple paths
- `└─┘` Join: Paths converge

## Notes

1. All flows show the current implementation with stabilityGrowth and diffAdjust (no alpha/beta references)
2. Manual intensity override takes precedence over minutes-based calculation
3. Settings persist across sessions via JSON files
4. Changes to intensity recalculate derived parameters immediately
5. Card scheduling uses the currently active parameters from the scheduler
