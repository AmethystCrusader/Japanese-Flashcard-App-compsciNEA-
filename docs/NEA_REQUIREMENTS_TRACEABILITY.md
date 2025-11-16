# NEA Requirements Traceability Matrix
## Japanese FSRS-6 Flashcard Application

**Purpose**: This matrix maps each functional and non-functional requirement to its design specification, implementation, algorithm reference, and test cases. It demonstrates comprehensive coverage from requirements through to verification.

**Last Updated**: November 2025

---

## Requirements Table

| Requirement ID | Description | Source/User Story | Design Section Ref | Implementation Ref | Algorithm/Flowchart Ref | Test Case ID(s) | Status |
|----------------|-------------|-------------------|-------------------|-------------------|------------------------|----------------|--------|
| **Functional Requirements - User Management** |
| REQ-001 | User login by username (no password) | Alex persona: "simple login" | NEA_DESIGN.md §2, §7 | flashcard_app.py:60-80 | Algorithm 1 (Login) | TC-001, TC-002 | ✓ Complete |
| REQ-002 | Create new user on first login | Alex persona: "no setup" | NEA_DESIGN.md §7 | persistence.py:109-112 | Algorithm 1 (Login) | TC-003 | ✓ Complete |
| REQ-003 | Load existing user settings | Jordan persona: "persistent config" | NEA_DESIGN.md §6 | user_settings.py:33-46 | N/A | TC-004 | ✓ Complete |
| REQ-004 | List existing usernames at login | Usability requirement | NEA_DESIGN.md §9 | persistence.py:99-103 | N/A | TC-002 | ✓ Complete |
| **Functional Requirements - Deck Management** |
| REQ-005 | Load hiragana deck from CSV | Core functionality | NEA_DESIGN.md §6, §7 | persistence.py:72-88 | Algorithm 5 (CSV Load) | TC-005, TC-006 | ✓ Complete |
| REQ-006 | Parse CSV with front/back/state/lastSeen fields | Data format spec | NEA_DESIGN.md §6 | persistence.py:80-87 | Algorithm 5 (CSV Load) | TC-007 | ✓ Complete |
| REQ-007 | Merge CSV data with JSON metadata | Data integrity | NEA_DESIGN.md §6, §7 | persistence.py:84-86 | Algorithm 5 (CSV Load) | TC-008 | ✓ Complete |
| REQ-008 | Save card metadata to JSON | Persistence requirement | NEA_DESIGN.md §6 | persistence.py:28-39 | N/A | TC-030, TC-031 | ✓ Complete |
| REQ-009 | Save deck metadata (daily counts) | Persistence requirement | NEA_DESIGN.md §6 | persistence.py:52-58 | N/A | TC-032 | ✓ Complete |
| REQ-010 | Save CSV with updated state/lastSeen | Backup persistence | NEA_DESIGN.md §6, §7 | persistence.py:90-97 | Algorithm 6 (CSV Save) | TC-033 | ✓ Complete |
| **Functional Requirements - FSRS-6 Scheduling** |
| REQ-011 | Implement FSRS-6 binary grading | Core algorithm | NEA_DESIGN.md §7, §8 | fsrs.py:171-216 | Algorithm 4 (FSRS Update) | TC-010, TC-011, TC-012 | ✓ Complete |
| REQ-012 | Update card difficulty based on grade | FSRS-6 spec | NEA_DESIGN.md §7 | fsrs.py:126-142 | Algorithm 4 (Difficulty) | TC-013 | ✓ Complete |
| REQ-013 | Update card stability based on grade | FSRS-6 spec | NEA_DESIGN.md §7 | fsrs.py:144-169 | Algorithm 4 (Stability) | TC-014 | ✓ Complete |
| REQ-014 | Calculate next review interval | FSRS-6 spec | NEA_DESIGN.md §7 | fsrs.py:118-124 | Algorithm 3 (Interval Calc) | TC-015 | ✓ Complete |
| REQ-015 | Filter due cards by date | Scheduling logic | NEA_DESIGN.md §7 | fsrs.py:218-232 | N/A | TC-016, TC-017 | ✓ Complete |
| REQ-016 | Track card lapses (forgetting events) | Diagnostic data | NEA_DESIGN.md §6 | fsrs.py:198-199 | Algorithm 4 (FSRS Update) | TC-018 | ✓ Complete |
| REQ-017 | Manage card state transitions (FSM) | Learning progression | NEA_DESIGN.md §6, §7 | fsrs.py:202-212 | Algorithm 4 (State FSM) | TC-019 | ✓ Complete |
| **Functional Requirements - Intensity System** |
| REQ-018 | Map minutes per day to intensity | User-friendly input | NEA_DESIGN.md §7, §8 | user_settings.py:62-91 | Algorithm 2 (Minutes→Intensity) | TC-020, TC-021 | ✓ Complete |
| REQ-019 | Calculate stabilityGrowth from intensity | FSRS-6 derived param | NEA_DESIGN.md §6, §7 | fsrs.py:48-66 | Algorithm 2 logic | TC-022 | ✓ Complete |
| REQ-020 | Calculate diffAdjust from intensity | FSRS-6 derived param | NEA_DESIGN.md §6, §7 | fsrs.py:68-85 | Algorithm 2 logic | TC-023 | ✓ Complete |
| REQ-021 | Allow manual intensity override | Jordan persona: "fine control" | NEA_DESIGN.md §9, §11 | user_settings.py:106-123 | Algorithm 7 (Manual Override) | TC-024, TC-025 | ✓ Complete |
| REQ-022 | Display effective intensity (auto or manual) | Transparency requirement | NEA_DESIGN.md §9 | user_settings.py:93-104 | Algorithm 7 (Effective Intensity) | TC-026 | ✓ Complete |
| REQ-023 | Persist intensity settings to JSON | Settings persistence | NEA_DESIGN.md §6 | user_settings.py:48-60 | N/A | TC-027 | ✓ Complete |
| **Functional Requirements - Practice Session** |
| REQ-024 | Display flashcard front side | Core UI | NEA_DESIGN.md §4, §9 | gui.py (PracticeView) | N/A | TC-040 | ✓ Complete |
| REQ-025 | Accept Again/Good grade via buttons | Binary grading UI | NEA_DESIGN.md §9 | gui.py (PracticeView) | N/A | TC-041 | ✓ Complete |
| REQ-026 | Show flashcard back after user thinks | Flashcard flow | NEA_DESIGN.md §4 | gui.py (PracticeView) | N/A | TC-042 | ✓ Complete |
| REQ-027 | Update card immediately on grade | Immediate persistence | NEA_DESIGN.md §5 | flashcard_app.py:174-183 | N/A | TC-043 | ✓ Complete |
| REQ-028 | Advance to next due card automatically | Session flow | NEA_DESIGN.md §4 | gui.py (PracticeView) | N/A | TC-044 | ✓ Complete |
| REQ-029 | Show session completion message | UX feedback | NEA_DESIGN.md §9 | flashcard_app.py:185-189 | N/A | TC-045 | ✓ Complete |
| **Functional Requirements - Daily Limits** |
| REQ-030 | Enforce max_per_day review limit | Cognitive load prevention | NEA_DESIGN.md §9, §11 | models.py:99-103 | Algorithm 8 (Daily Cap) | TC-050, TC-051 | ✓ Complete |
| REQ-031 | Increment daily count on each review | Limit tracking | NEA_DESIGN.md §6 | models.py:94-97 | Algorithm 8 (Increment) | TC-052 | ✓ Complete |
| REQ-032 | Offer override option when limit reached | User autonomy | NEA_DESIGN.md §9 | flashcard_app.py:148-157 | Algorithm 8 (Override Dialog) | TC-053 | ✓ Complete |
| REQ-033 | Reset allow_over_limit_today flag daily | Daily scope | NEA_DESIGN.md §6 | models.py:70 | N/A | TC-054 | ✓ Complete |
| REQ-034 | Store daily counts by date | Historical tracking | NEA_DESIGN.md §6 | models.py:89-97 | N/A | TC-055 | ✓ Complete |
| **Functional Requirements - Statistics** |
| REQ-035 | Display card counts by state | Progress visibility | NEA_DESIGN.md §9 | gui.py (StatsView) | Algorithm 9 (Aggregation) | TC-060 | ✓ Complete |
| REQ-036 | Show today's review count | Daily progress | NEA_DESIGN.md §9 | gui.py (StatsView) | N/A | TC-061 | ✓ Complete |
| REQ-037 | Display due cards count | Pending work indicator | NEA_DESIGN.md §9 | gui.py (MainMenu) | N/A | TC-062 | ✓ Complete |
| REQ-038 | Show current FSRS parameters | Transparency | NEA_DESIGN.md §9 | gui.py (StatsView) | N/A | TC-063 | ✓ Complete |
| REQ-039 | Allow minutes_per_day adjustment | Settings control | NEA_DESIGN.md §9 | gui.py (StatsView) | N/A | TC-064 | ✓ Complete |
| **Non-Functional Requirements - Validation** |
| REQ-040 | Validate username format | Security (path injection) | NEA_DESIGN.md §11, §15 | gui.py (LoginScreen) | N/A | TC-070 | ✓ Complete |
| REQ-041 | Validate minutes_per_day range (1-300) | Input sanity | NEA_DESIGN.md §11 | user_settings.py:131-132 | N/A | TC-071 | ✓ Complete |
| REQ-042 | Validate manual intensity range (0-10) | Input sanity | NEA_DESIGN.md §11 | user_settings.py:115-120 | Algorithm 7 (Validation) | TC-072, TC-073 | ✓ Complete |
| REQ-043 | Handle corrupted JSON gracefully | Resilience | NEA_DESIGN.md §11, §15 | persistence.py:41-50, user_settings.py:43-46 | N/A | TC-080, TC-081 | ✓ Complete |
| REQ-044 | Validate CSV required fields | Data integrity | NEA_DESIGN.md §11 | persistence.py:80 | Algorithm 5 (Validation) | TC-082 | ✓ Complete |
| REQ-045 | Handle missing files gracefully | Resilience | NEA_DESIGN.md §11 | persistence.py:46-50, 64-70 | N/A | TC-083 | ✓ Complete |
| **Non-Functional Requirements - Performance** |
| REQ-046 | Grade response time <200ms | User experience | NEA_DESIGN.md §3, §14 | fsrs.py:171-216 | Algorithm 4 (optimized) | TC-090 | ✓ Complete |
| REQ-047 | Load 5000-card deck in <5s | Scalability | NEA_DESIGN.md §3, §14 | persistence.py:72-88 | Algorithm 5 (O(n)) | TC-091 | ✓ Complete |
| REQ-048 | Memory usage <500MB for 5000 cards | Resource efficiency | NEA_DESIGN.md §14 | All modules | N/A | TC-092 | ✓ Complete |
| **Non-Functional Requirements - Security** |
| REQ-049 | No network requests (offline-only) | Privacy | NEA_DESIGN.md §15 | All modules (no HTTP libs) | N/A | TC-100 | ✓ Complete |
| REQ-050 | Store data in user-specific directories | Data isolation | NEA_DESIGN.md §6, §15 | persistence.py:16-26 | N/A | TC-101 | ✓ Complete |
| REQ-051 | Use plaintext formats (transparency) | User control | NEA_DESIGN.md §9, §15 | persistence.py (JSON/CSV) | N/A | TC-102 | ✓ Complete |
| REQ-052 | Prevent path traversal in username | Security | NEA_DESIGN.md §11, §15 | gui.py (LoginScreen validation) | N/A | TC-103 | ✓ Complete |
| **Non-Functional Requirements - Usability** |
| REQ-053 | First practice session within 3 minutes | Onboarding speed | NEA_DESIGN.md §3 | All modules (zero-config) | N/A | TC-110 | ✓ Complete |
| REQ-054 | Binary grading buttons clearly labeled | Clarity | NEA_DESIGN.md §9 | gui.py (PracticeView) | N/A | TC-111 | ✓ Complete |
| REQ-055 | Color-coded buttons (red/green) | Visual feedback | NEA_DESIGN.md §9, §16 | gui.py (PracticeView) | N/A | TC-112 | ✓ Complete |
| REQ-056 | Display clear error messages | Error handling | NEA_DESIGN.md §11 | All modules (messagebox.showerror) | N/A | TC-113 | ✓ Complete |
| REQ-057 | Confirm extreme manual intensity values | User protection | NEA_DESIGN.md §11 | user_settings.py:119-120 | Algorithm 7 (Confirm) | TC-114 | ✓ Complete |

---

## Requirements Coverage Summary

**Total Requirements**: 57  
**Completed**: 57 (100%)  
**In Progress**: 0  
**Not Started**: 0  

### Requirements by Category

| Category | Count | Percentage |
|----------|-------|------------|
| User Management | 4 | 7.0% |
| Deck Management | 6 | 10.5% |
| FSRS-6 Scheduling | 7 | 12.3% |
| Intensity System | 6 | 10.5% |
| Practice Session | 6 | 10.5% |
| Daily Limits | 5 | 8.8% |
| Statistics | 5 | 8.8% |
| Validation | 6 | 10.5% |
| Performance | 3 | 5.3% |
| Security | 4 | 7.0% |
| Usability | 5 | 8.8% |

### Traceability Gaps

**None identified**. All requirements trace to:
- Design specification (NEA_DESIGN.md sections)
- Implementation (file:line references)
- Algorithm documentation (where applicable)
- Test cases (TC-XXX identifiers)

### Test Case Reference

Test cases (TC-XXX) are defined in:
- **Unit Tests**: `test_app.py`, `test_intensity.py`, `test_gui.py`
- **Integration Tests**: Documented in NEA_TEST_STRATEGY.md
- **System Tests**: Manual test protocol in NEA_TEST_STRATEGY.md
- **Evaluation Tests**: Retention study and usability protocol in NEA_DESIGN.md §13

---

## Requirements Changes Log

| Date | Requirement ID | Change Type | Description | Reason |
|------|---------------|-------------|-------------|--------|
| 2025-10-15 | REQ-018 | Added | Minutes-to-intensity mapping | User feedback: direct intensity confusing for beginners |
| 2025-10-20 | REQ-021 | Added | Manual intensity override | User feedback: power users need fine control |
| 2025-10-25 | REQ-030-034 | Added | Daily limit system | Design decision: prevent cognitive overload |
| 2025-11-01 | REQ-040, REQ-052 | Added | Username validation | Security review: prevent path injection |
| 2025-11-05 | REQ-057 | Added | Confirm extreme intensity | Usability: prevent accidental extreme values |

---

## Future Requirements (Backlog)

| Future Req ID | Description | Priority | Estimated Effort | Depends On |
|---------------|-------------|----------|------------------|------------|
| REQ-F01 | Audio pronunciation playback | High | 2 weeks | None |
| REQ-F02 | Keyboard shortcuts (Space/Backspace) | High | 1 week | None |
| REQ-F03 | Multiple deck support | Medium | 3 weeks | None |
| REQ-F04 | Custom deck import | Medium | 2 weeks | REQ-F03 |
| REQ-F05 | Graphical statistics (charts) | Medium | 2 weeks | matplotlib library |
| REQ-F06 | Export progress to CSV | Low | 1 week | None |
| REQ-F07 | Dark mode theme | Low | 1 week | Theme system |
| REQ-F08 | Undo last grade | Medium | 1 week | History stack |
| REQ-F09 | Anki deck import | Low | 3 weeks | SQLite, zipfile |
| REQ-F10 | Mobile app (Kivy port) | Low | 8 weeks | Kivy framework |

---

**Maintained By**: Student Candidate  
**Review Cycle**: Updated after each iteration  
**Approval**: Self-assessed against OCR H446 Band 4 criteria

