# FSRS‑6 Mapping: Equations ⇄ Code ⇄ Flowcharts (with Justification)

This document maps each FSRS‑6 formula or rule used in the app to:
- What it means (plain English/justification)
- Where it is implemented in code
- Which flowchart step(s) it corresponds to
- Its key inputs and outputs

## Core Update Equations (updateOnAnswer)

| Element / Equation | Meaning & Why (Justification) | Code Location | Flowchart Node(s) | Inputs | Outputs/Effect |
|---|---|---|---|---|---|
| t = days(now − last_seen) | How long since you last reviewed this card. Time drives forgetting. | scheduler/fsrs6.py → updateOnAnswer | “t = days since last_seen” | last_seen, now | t (elapsed days) |
| R = exp(−t / S) (clipped) | Retrieval probability right now. Larger S or smaller t ⇒ higher R. Basis of spaced repetition: test near the “edge of forgetting.” | scheduler/fsrs6.py → updateOnAnswer | “R = exp(-t / S) clipped” | t, S | R in (≈0..1) |
| alpha = base_alpha × (0.6 + 0.8 × intensity) | Scales how fast stability grows on success. More daily minutes ⇒ higher intensity ⇒ learn faster. | scheduler/fsrs6.py → updateOnAnswer | “Scale alpha,beta by intensity” | intensity | alpha (growth factor) |
| beta = base_beta × (0.6 + 0.8 × intensity) | Scales how strongly difficulty shifts on success/failure. Higher intensity ⇒ faster adaptation. | scheduler/fsrs6.py → updateOnAnswer | “Scale alpha,beta by intensity” | intensity | beta (difficulty adjustment) |
| If correct: D_new = clamp(D − beta × (1 − R), 1..10) | Make the card slightly easier on success; bigger drop if success was “stretchy” (low R ⇒ big 1−R). | scheduler/fsrs6.py → updateOnAnswer | “Good: D-=beta*(1-R)” | D, beta, R | D_new |
| ease = (10 − D_new) / 9 | Convert difficulty to an ease factor 0..1 for scaling stability growth (easier items grow faster). | scheduler/fsrs6.py → updateOnAnswer | “ease=(10-D)/9” | D_new | ease (0..1) |
| If correct: S_new = clamp(S × (1 + alpha × ease × (1 − R)) + 0.05, 0.2..3650) | Increase stability on success. Bigger growth for easier items and “stretch successes.” +0.05 ensures some growth. | scheduler/fsrs6.py → updateOnAnswer | “S*=1+alpha*ease*(1-R)+0.05” | S, alpha, ease, R | S_new |
| If incorrect: D_new = clamp(D + beta × (1 − R), 1..10) | Make the card slightly harder on failure; bigger increase if you waited too long (low R). | scheduler/fsrs6.py → updateOnAnswer | “Again: D+=beta*(1-R)” | D, beta, R | D_new |
| If incorrect: S_new = max(0.2, S × 0.5) | Collapse stability on failure so the card resurfaces soon to rebuild memory. Floor prevents zero. | scheduler/fsrs6.py → updateOnAnswer | “Again: S=max(0.2,S*0.5)” | S | S_new |
| interval_days = clamp(−S_new × ln(R_target), 0.01..3650) | Schedule next review so the expected recall prob. at that time equals your target (e.g., 90%). Higher S_new ⇒ longer interval; higher R_target ⇒ shorter interval. | scheduler/fsrs6.py → updateOnAnswer | “interval = -S*ln(R_target) clamped” | S_new, R_target | interval_days |
| card.touch_seen() = now | Record that we just reviewed now; needed for future t calculations. | scheduler/fsrs6.py → updateOnAnswer | “touch_seen() = now” | now | last_seen updated |
| state = f(S_new): [<1d→0, <3d→1, <7d→2, ≥7d→3] | Map stability to a familiar 0..3 state for the UI. The scheduler still uses S/interval internally. | scheduler/fsrs6.py → updateOnAnswer | “Derive state from S” | S_new | user-visible state |
| Increment daily count; persist | Track reviews per day (for caps/insights) and save per-deck FSRS metadata. | scheduler/fsrs6.py → updateOnAnswer | “Increment daily count; save meta” | — | daily count++, fsrs deck JSON updated |

### Why these equations?
- R = exp(−t/S) is a standard exponential forgetting curve. It captures that forgetting slows as memories stabilize.
- interval = −S ln(R_target) schedules the next review so your modelled probability of remembering then is R_target (e.g., 90%).
- (1 − R) terms reward “stretch” correct answers (low R) with more growth, and penalize long-overdue failures with stronger difficulty increases, aligning with desirable difficulty.
- Intensity scales alpha/beta so your daily time commitment actually changes how fast the system adapts.

## Due Logic and Card Selection (next)

| Element / Rule | Meaning & Why | Code Location | Flowchart Node(s) | Inputs | Outputs/Effect |
|---|---|---|---|---|---|
| due_time = last_seen + interval_days | When the card becomes due under current plan. | scheduler/fsrs6.py → _due_time | (implicit in “Build list of due cards”) | last_seen, interval_days | due_time (datetime) |
| If cap reached AND Extra OFF ⇒ return None | Respect daily plan. Encourages consistent pacing and avoids burnout. | scheduler/fsrs6.py → next | “Cap reached AND Extra OFF?” → “Return None” | max_per_day, today_count, allow_over_limit_today | Stops session when plan is met |
| If due cards exist: sort by (due_time asc, D desc, S asc) | Prioritize earliest due; break ties by harder/higher D first, then lower stability S (more fragile) first. | scheduler/fsrs6.py → next | “Sort by (due_time asc, D desc, S asc)” | due list | Ordered shortlist |
| Pick random among top 5 | Avoids strict determinism and keeps variety while respecting priority. | scheduler/fsrs6.py → next | “Pick random among top 5” | shortlist | chosen card |
| If no due and Extra ON: pick soonest upcoming | When you want to continue studying, use “study ahead” on the nearest future item. | scheduler/fsrs6.py → next | “Pick soonest upcoming (study ahead)” | cards | chosen early card or None |

## Global & Persistence

| Element / Rule | Meaning & Why | Code Location | Flowchart Node(s) | Inputs | Outputs/Effect |
|---|---|---|---|---|---|
| set_context(user, deck, intensity, R_target, cap, extra-flag) | Bind FSRS to per-user/deck storage, load existing metadata, and apply current plan settings. | scheduler/fsrs6.py → set_context | “FSRS set_context(user, deck, intensity, retention, cap, extra-flag)” | settings, deck path | FSRS ready for this deck |
| _meta (per-card S, D, interval, lapses) | Memory parameters are tracked per card and persisted per deck. | scheduler/fsrs6.py | Used across | — | JSON under data/users/<user>/fsrs/<deck>.json |
| _global.max_per_day, _global.daily | Store per-deck cap and daily review counts for pacing & insights. | scheduler/fsrs6.py | “Increment daily count; save meta” | — | Enforced cap and analytics |
| set_over_limit_today(flag) | Toggle daily cap override and persist for insights. | scheduler/fsrs6.py → set_over_limit_today | “Extra Study Today (bypass cap)” | UI flag | Affects next() & suggestions |

## Clamps & Safety Nets

| Clamp | Reason | Code Location |
|---|---|---|
| R ∈ [1e−6, 0.999999] | Prevent numeric edge cases when R≈0 or R≈1. | scheduler/fsrs6.py → updateOnAnswer |
| S_new ∈ [0.2, 3650] days | Stability never zero/negative; cap at ~10 years. | scheduler/fsrs6.py → updateOnAnswer |
| interval_days ∈ [0.01, 3650] | Avoid instant repeats (<~15 minutes) or absurd long gaps. | scheduler/fsrs6.py → updateOnAnswer |

## Inputs and Their Effects (at a glance)

| Input | Where It Comes From | Affects | Effect on Scheduling |
|---|---|---|---|
| daily_minutes | First-login prompt or Insights “Apply” | intensity, R_target, daily cap | Higher minutes → higher intensity (faster learning), often higher R_target (tighter retention), larger daily cap |
| correctness (True/False) | Your answer | D_new, S_new, interval | Correct grows S and lowers D; incorrect halves S and raises D; both recompute interval |
| t (elapsed days) | last_seen vs now | R | Larger t → smaller R ⇒ bigger changes |
| S (stability) | Card meta | R, next interval | Larger S → slower forgetting; longer intervals |

## Flowcharts: Node Mappings Summary

- FSRS-6 updateOnAnswer() core:
  - “t = days since last_seen” → compute elapsed days
  - “R = exp(-t / S) clipped” → retrieval probability
  - “Scale alpha,beta by intensity” → adaptive learning rate
  - Branch “Answer correct?”:
    - Good path: “D-=beta*(1-R); ease=(10-D)/9; S*=1+alpha*ease*(1-R)+0.05”
    - Again path: “D+=beta*(1-R); S=max(0.2,S*0.5); lapses+=1”
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
- It lets the plan be tuned by lifestyle (minutes/day) via intensity and target retention, and it enforces a daily cap for pacing—with an explicit “Extra Study” switch when you want to exceed it.
- The math remains simple enough to explain and visualize (exponential forgetting, log for interval) while being more adaptive than basic Leitner variants.
