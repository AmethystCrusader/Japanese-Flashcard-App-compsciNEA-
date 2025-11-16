# FSRS‑6 Mapping: Equations ⇄ Code ⇄ Flowcharts (with Justification)
Updated to use the new terms replacing alpha → stabilityGrowth and beta → diffAdjust.

This document maps each FSRS‑6 formula or rule used in the app to:
- What it means (plain English/justification)
- Where it is implemented in code
- Which flowchart step(s) it corresponds to
- Its key inputs and outputs

Terminology update
- stabilityGrowth: scales how fast stability grows on success (replaces alpha)
- diffAdjust: scales how strongly difficulty shifts on success/failure (replaces beta)

Code locations referenced below correspond to fsrs.py (FSRS6Scheduler) unless noted otherwise.

## Core Update Equations (update_on_answer)

| Element / Equation | Meaning & Why (Justification) | Code Location | Flowchart Node(s) | Inputs | Outputs/Effect |
|---|---|---|---|---|---|
| t = days(now − last_seen) | How long since you last reviewed this card. Time drives forgetting. | fsrs.py → FSRS6Scheduler.update_on_answer | “t = days since last_seen” | last_seen, now | t (elapsed days) |
| R = exp(−t / S) (clipped) | Retrieval probability right now. Larger S or smaller t ⇒ higher R. Basis of spaced repetition: test near the “edge of forgetting.” | fsrs.py → FSRS6Scheduler.update_on_answer | “R = exp(-t / S) clipped” | t, S | R in (≈0..1) |
| stabilityGrowth = base_stabilityGrowth × (0.6 + 0.8 × intensity) | Scales how fast stability grows on success. More daily minutes ⇒ higher intensity ⇒ learn faster or tighter pacing (by design). | fsrs.py → FSRS6Scheduler.update_on_answer | “Scale stabilityGrowth,diffAdjust by intensity” | intensity | stabilityGrowth (growth scaler) |
| diffAdjust = base_diffAdjust × (0.6 + 0.8 × intensity) | Scales how strongly difficulty shifts on success/failure. Higher intensity ⇒ faster adaptation. | fsrs.py → FSRS6Scheduler.update_on_answer | “Scale stabilityGrowth,diffAdjust by intensity” | intensity | diffAdjust (difficulty adjustment) |
| If correct: D_new = clamp(D − diffAdjust × (1 − R), 1..10) | Make the card slightly easier on success; bigger drop if success was “stretchy” (low R ⇒ big 1−R). | fsrs.py → FSRS6Scheduler.update_on_answer | “Good: D-=diffAdjust*(1-R)” | D, diffAdjust, R | D_new |
| ease = (10 − D_new) / 9 | Convert difficulty to an ease factor 0..1 for scaling stability growth (easier items grow faster). | fsrs.py → FSRS6Scheduler.update_on_answer | “ease=(10-D)/9” | D_new | ease (0..1) |
| If correct: S_new = clamp(S × (1 + stabilityGrowth × ease × (1 − R)) + 0.05, 0.2..3650) | Increase stability on success. Bigger growth for easier items and “stretch successes.” +0.05 ensures some growth. | fsrs.py → FSRS6Scheduler.update_on_answer | “S*=1+stabilityGrowth*ease*(1-R)+0.05” | S, stabilityGrowth, ease, R | S_new |
| If incorrect: D_new = clamp(D + diffAdjust × (1 − R), 1..10) | Make the card slightly harder on failure; bigger increase if you waited too long (low R). | fsrs.py → FSRS6Scheduler.update_on_answer | “Again: D+=diffAdjust*(1-R)” | D, diffAdjust, R | D_new |
| If incorrect: S_new = max(0.2, S × 0.5) | Collapse stability on failure so the card resurfaces soon to rebuild memory. Floor prevents zero. | fsrs.py → FSRS6Scheduler.update_on_answer | “Again: S=max(0.2,S*0.5)” | S | S_new |
| interval_days = clamp(−S_new × ln(R_target), 0.01..3650) | Schedule next review so the expected recall prob. at that time equals your target (e.g., 90%). Higher S_new ⇒ longer interval; higher R_target ⇒ shorter interval. | fsrs.py → FSRS6Scheduler.update_on_answer | “interval = -S*ln(R_target) clamped” | S_new, R_target | interval_days |
| card.touch_seen() = now | Record that we just reviewed now; needed for future t calculations. | fsrs.py → FSRS6Scheduler.update_on_answer | “touch_seen() = now” | now | last_seen updated |
| state = f(S_new): [<1d→0, <3d→1, <7d→2, ≥7d→3] | Map stability to a familiar 0..3 state for the UI. The scheduler still uses S/interval internally. | fsrs.py → FSRS6Scheduler.update_on_answer | “Derive state from S_new” | S_new | state (0..3) |
| Increment daily count; persist | Track reviews per day (for caps/insights) and save per-deck FSRS metadata. | fsrs.py → FSRS6Scheduler.update_on_answer | “Increment daily count; save meta” | — | daily counters, JSON saved |

Notes on naming migration
- Where the literature or earlier drafts referenced alpha and beta, the implementation and this document now use stabilityGrowth and diffAdjust, respectively.
- The math and intuition are unchanged: stabilityGrowth governs stability growth on success; diffAdjust governs difficulty movement on success/failure.

### Why these equations?
- R = exp(−t/S) is a standard exponential forgetting curve. It captures that forgetting slows as memories stabilize.
- interval = −S ln(R_target) schedules the next review so your modelled probability of remembering then is R_target (e.g., 90%).
- (1 − R) terms reward “stretch” correct answers (low R) with more growth, and penalize long-overdue failures with stronger difficulty increases, aligning with desirable difficulty.
- Intensity scales stabilityGrowth/diffAdjust so your daily time commitment actually changes how fast the system adapts.

## Due Logic and Card Selection (next)

| Element / Rule | Meaning & Why | Code Location | Flowchart Node(s) | Inputs | Outputs/Effect |
|---|---|---|---|---|---|
| due_time = last_seen + interval_days | When the card becomes due under current plan. | fsrs.py → FSRS6Scheduler._due_time (helper) | (implicit in “Build list of due cards”) | last_seen, interval_days | due_time |
| If cap reached AND Extra OFF ⇒ return None | Respect daily plan. Encourages consistent pacing and avoids burnout. | fsrs.py → FSRS6Scheduler.next | “Cap reached AND Extra OFF?” → “Return None” | max_per_day, daily_count, extra_flag | No card chosen |
| If due cards exist: sort by (due_time asc, D desc, S asc) | Prioritize earliest due; break ties by harder (higher D) first, then lower stability S (more fragile) first. | fsrs.py → FSRS6Scheduler.next | “Sort by (due_time, D, S)” | due list | sorted list |
| Pick random among top 5 | Avoids strict determinism and keeps variety while respecting priority. | fsrs.py → FSRS6Scheduler.next | “Pick random among top 5” | shortlist | chosen card |
| If no due and Extra ON: pick soonest upcoming | When you want to continue studying, use “study ahead” on the nearest future item. | fsrs.py → FSRS6Scheduler.next | “Pick soonest upcoming (study ahead)” | upcoming list, extra_flag | chosen card |

## Global & Persistence

| Element / Rule | Meaning & Why | Code Location | Flowchart Node(s) | Inputs | Outputs/Effect |
|---|---|---|---|---|---|
| set_context(user, deck, intensity, R_target, cap, extra_flag) | Bind FSRS to per-user/deck storage, load existing metadata, and apply current plan settings. | fsrs.py → FSRS6Scheduler.set_context | “Load user/deck meta; apply settings” | user, deck, settings | in-memory state ready |
| _meta (per-card S, D, interval, lapses) | Memory parameters are tracked per card and persisted per deck. | fsrs.py | Used across | — | JSON under data/users/<user>/fsrs/<deck>.json |
| _global.max_per_day, _global.daily | Store per-deck cap and daily review counts for pacing & insights. | fsrs.py | “Increment daily count; save meta” | — | Enforced cap and analytics |
| set_over_limit_today(flag) | Toggle daily cap override and persist for insights. | fsrs.py → FSRS6Scheduler.set_over_limit_today | “Extra Study Today (bypass cap)” | UI flag | Affects next() & suggestions |

## Clamps & Safety Nets

| Clamp | Reason | Code Location |
|---|---|---|
| R ∈ [1e−6, 0.999999] | Prevent numeric edge cases when R≈0 or R≈1. | fsrs.py → FSRS6Scheduler.update_on_answer |
| S_new ∈ [0.2, 3650] days | Stability never zero/negative; cap at ~10 years. | fsrs.py → FSRS6Scheduler.update_on_answer |
| interval_days ∈ [0.01, 3650] | Avoid instant repeats (<~15 minutes) or absurd long gaps. | fsrs.py → FSRS6Scheduler.update_on_answer |

## Inputs and Their Effects (at a glance)

| Input | Where It Comes From | Affects | Effect on Scheduling |
|---|---|---|---|
| daily_minutes | First-login prompt or Insights “Apply” | intensity, R_target, daily cap | Higher minutes → typically higher intensity (tighter pacing), may set higher R_target, and can justify larger daily cap |
| correctness (True/False) | Your answer | D_new, S_new, interval | Correct grows S and lowers D; incorrect halves S and raises D; both recompute interval |
| t (elapsed days) | last_seen vs now | R | Larger t → smaller R ⇒ bigger changes |
| S (stability) | Card meta | R, next interval | Larger S → slower forgetting; longer intervals |
| stabilityGrowth, diffAdjust | Derived from intensity | S growth rate, D adjustments | Higher stabilityGrowth increases stability gains on correct; higher diffAdjust increases magnitude of difficulty changes |

## Flowcharts: Node Mappings Summary

- FSRS-6 update_on_answer():
  - “t = days since last_seen” → compute elapsed days
  - “R = exp(-t / S) clipped” → retrieval probability
  - “Scale stabilityGrowth,diffAdjust by intensity” → adaptive learning rate
  - Branch “Answer correct?”:
    - Good path: “D-=diffAdjust*(1-R); ease=(10-D)/9; S*=1+stabilityGrowth*ease*(1-R)+0.05”
    - Again path: “D+=diffAdjust*(1-R); S=max(0.2,S*0.5); lapses+=1”
  - “interval = -S*ln(R_target) clamped” → next review gap
  - “Update meta; touch_seen(); Derive state; Increment daily; Save meta” → persistence and UI state

- FSRS-6 next():
  - “Cap reached AND Extra OFF?” → stop vs continue
  - “Build list of due cards” → now >= last_seen + interval
  - “Sort by (due_time asc, D desc, S asc)” → prioritization
  - “Random among top 5” → final pick
  - “Extra ON? → Pick soonest upcoming” → study-ahead logic

## Why FSRS‑6 is a good fit here

- It ties scheduling to a probabilistic memory model (R), not just fixed boxes. That means intervals adapt to how long you waited and how stable the memory is.
- It rewards “desirable difficulty”: when success is unlikely (low R), you gain more.
- It lets the plan be tuned by lifestyle (minutes/day) via intensity and the derived stabilityGrowth/diffAdjust, and it enforces a daily cap for pacing—with an explicit “Extra Study” switch when you want to exceed it.
- The math remains simple enough to explain and visualize (exponential forgetting, log for interval) while being more adaptive than basic Leitner variants.
