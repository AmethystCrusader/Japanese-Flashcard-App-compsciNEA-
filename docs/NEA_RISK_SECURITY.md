# NEA Risk & Security Analysis
## Japanese FSRS-6 Flashcard Application

**Purpose**: Comprehensive risk assessment and security threat modeling for the flashcard application.

**Last Updated**: November 2025

---

## Risk Register

| Risk ID | Category | Risk Description | Likelihood | Impact | Mitigation Strategy | Residual Risk | Owner |
|---------|----------|------------------|------------|--------|---------------------|---------------|-------|
| **Technical Risks** |
| RISK-001 | Technical | Python interpreter version incompatibility (3.10 vs 3.12) | Medium | High | Pin Python >= 3.10 in requirements, use dataclasses (3.7+ compatible) | Low | Developer |
| RISK-002 | Technical | Tkinter not installed on Linux systems | Medium | High | Document apt-get install python3-tk in README | Medium | User |
| RISK-003 | Technical | FSRS algorithm bugs producing incorrect intervals | Low | High | Unit tests with manual verification, 35+ test cases | Low | Developer |
| RISK-004 | Technical | Floating point precision errors in stability calculations | Very Low | Medium | Python's 64-bit float sufficient for day-scale intervals | Very Low | N/A |
| RISK-005 | Technical | File system permissions prevent directory creation | Low | High | Check write permissions, show error with instructions | Low | User/Developer |
| **Data Integrity Risks** |
| RISK-006 | Data Integrity | JSON file corruption (disk error, crash during write) | Low | High | Atomic writes via Python open(), fallback to defaults with user warning | Low | Developer |
| RISK-007 | Data Integrity | CSV file corruption (manual editing error) | Medium | Medium | Validate required fields, skip malformed rows with warnings | Low | Developer |
| RISK-008 | Data Integrity | User accidentally deletes data/users/ directory | Medium | High | Document backup strategy, show clear error with recovery steps | Medium | User |
| RISK-009 | Data Integrity | Lost progress due to no backup strategy | High | Medium | Recommend git/cloud backup in documentation | Medium | User |
| RISK-010 | Data Integrity | Concurrent writes from multiple app instances | Very Low | Medium | Single-user design assumption, no file locking | Medium | Design |
| **Performance Risks** |
| RISK-011 | Performance | Slow load time for large decks (>5000 cards) | Low | Low | Projected 5.5s load time acceptable, can optimize later | Low | Developer |
| RISK-012 | Performance | Memory usage scales linearly with deck size | Very Low | Low | 550KB for 5000 cards is negligible on modern systems | Very Low | N/A |
| RISK-013 | Performance | JSON parsing bottleneck | Low | Low | Pure Python json module sufficient for MVP, can switch to ujson later | Very Low | Developer |
| **UX/Usability Risks** |
| RISK-014 | UX | Users confused by intensity parameter meaning | Medium | Medium | Mitigated via minutes-to-intensity mapping, parameter display with tooltips (future) | Low | Developer |
| RISK-015 | UX | Users forget manual override is active | Medium | Low | Show "(manual)" indicator in stats view | Low | Developer |
| RISK-016 | UX | Color-blind users cannot distinguish red/green buttons | High | Medium | Current mitigation: button labels. Future: add icons (X/✓) | Medium | Developer |
| RISK-017 | UX | Users accidentally grade wrong (no undo) | High | Low | Planned feature: "Undo Last Grade" button (Iteration 15+) | Medium | Developer |
| RISK-018 | UX | Users reach daily limit and feel blocked | Medium | Low | Override dialog offers escape hatch | Low | Developer |
| **Maintainability Risks** |
| RISK-019 | Maintainability | Code complexity increases with features | Medium | Medium | Modular architecture, clear separation of concerns | Low | Developer |
| RISK-020 | Maintainability | FSRS-6 algorithm changes in future research | Low | Low | Encapsulated in FSRS6Scheduler class, easy to update parameters | Very Low | Developer |
| RISK-021 | Maintainability | Documentation becomes outdated | High | Medium | Regular review cycle after each iteration | Low | Developer |
| **Security Risks** |
| RISK-022 | Security | Path traversal via malicious username | Low | High | Username validation (alphanumeric only, no ../) | Very Low | Developer |
| RISK-023 | Security | CSV formula injection (Excel execution) | Low | High | CSV parsed as plain text, not evaluated as formulas | Very Low | Developer |
| RISK-024 | Security | Malicious CSV with millions of rows (DoS) | Very Low | Medium | Python MemoryError before system crash, future: add row limit | Low | Developer |
| RISK-025 | Security | Data exposure on shared computer | Medium | Low | User-specific directories, recommend OS-level file permissions | Medium | User |
| RISK-026 | Security | No user authentication (username only) | Medium | Low | Acceptable for personal devices, add password auth for schools | Medium | Design |

---

## STRIDE Threat Model

### Spoofing Identity

**Threat S-1: User Impersonation**  
**Description**: Attacker enters another user's username to access their learning data  
**Likelihood**: Medium (shared computer scenario)  
**Impact**: Low (no sensitive data, only learning progress)  
**Attack Vector**: Simple username entry on login screen  
**Mitigation**: Current: None. Future: Optional password authentication for shared environments  
**Residual Risk**: Acceptable for personal devices; schools would need password feature  
**Related Risk**: RISK-026

**Threat S-2: False Data Origin**  
**Description**: User imports malicious CSV pretending to be legitimate deck  
**Likelihood**: Very Low (requires user to deliberately import attacker file)  
**Impact**: Low (CSV content only affects that user)  
**Attack Vector**: Replace hiragana.csv with malicious content  
**Mitigation**: CSV validation checks required fields, no code execution from CSV  
**Residual Risk**: Very Low  
**Related Risk**: RISK-023

### Tampering

**Threat T-1: Manual Metadata Editing (Cheating)**  
**Description**: User edits cards_metadata.json to mark all cards as "Review" state  
**Likelihood**: High (files are intentionally transparent/editable)  
**Impact**: Very Low (only cheating themselves, no competition/leaderboards)  
**Attack Vector**: Direct file editing in text editor  
**Mitigation**: None (by design). Educational consequence: users who cheat learn less  
**Residual Risk**: Accepted. Transparency valued over tamper-resistance  
**Related Risk**: N/A (acceptable by design)

**Threat T-2: CSV Formula Injection**  
**Description**: Attacker creates CSV with Excel formulas (e.g., =SYSTEM("rm -rf /"))  
**Likelihood**: Low (requires attacker-controlled CSV + Excel with macros)  
**Impact**: High (potential code execution)  
**Attack Vector**: User opens malicious CSV in Excel, macro executes  
**Mitigation**: Python csv module parses as plain text, never evaluates formulas. Warning in docs about Excel macros  
**Residual Risk**: Very Low (requires Excel + user enabling macros)  
**Related Risk**: RISK-023

**Threat T-3: Configuration Tampering**  
**Description**: User sets extreme intensity values to break algorithm  
**Likelihood**: Low (requires deliberate manual JSON editing)  
**Impact**: Low (algorithm still mathematically sound, just impractical intervals)  
**Attack Vector**: Edit settings.json with intensity=1000  
**Mitigation**: Validation clamps intensity to 0-10 range when loaded via UI  
**Residual Risk**: Low (manual editing bypasses validation but doesn't break system)  
**Related Risk**: N/A

### Repudiation

**Threat R-1: Deny Completing Reviews**  
**Description**: User claims they didn't grade cards (not applicable to educational app)  
**Likelihood**: N/A  
**Impact**: N/A  
**Attack Vector**: N/A  
**Mitigation**: Not applicable (no audit requirements)  
**Residual Risk**: N/A  
**Related Risk**: N/A

### Information Disclosure

**Threat I-1: Learning Progress Exposed to Other Users**  
**Description**: Other users on shared computer access another user's learning data  
**Likelihood**: Medium (family/school computer)  
**Impact**: Low (learning progress is not highly sensitive)  
**Attack Vector**: Browse data/users/{other_username}/ directory  
**Mitigation**: User-specific directories. Recommend OS file permissions (chmod 700). Future: Optional encryption  
**Residual Risk**: Low with OS permissions, Medium without  
**Related Risk**: RISK-025

**Threat I-2: Data Exposure on Lost/Stolen Device**  
**Description**: Device theft exposes flashcard data  
**Likelihood**: Low (general device theft risk)  
**Impact**: Very Low (flashcard content is public information, hiragana is not secret)  
**Attack Vector**: Physical device access  
**Mitigation**: Recommend full-disk encryption (OS feature). No PII stored in app  
**Residual Risk**: Very Low (no sensitive data)  
**Related Risk**: N/A

**Threat I-3: Accidental Cloud Backup of Unencrypted Data**  
**Description**: Cloud backup service syncs data/ directory, exposes data to cloud provider  
**Likelihood**: Medium (if user enables Dropbox/Google Drive sync)  
**Impact**: Low (provider sees hiragana flashcards, not sensitive)  
**Attack Vector**: User syncs project directory to cloud  
**Mitigation**: Document that data is stored locally. Users choosing cloud sync accept risk  
**Residual Risk**: Low (acceptable trade-off for backup convenience)  
**Related Risk**: N/A

### Denial of Service

**Threat D-1: Malicious CSV with Millions of Rows**  
**Description**: Attacker creates CSV with millions of rows to exhaust memory  
**Likelihood**: Very Low (requires attacker-created file + user importing it)  
**Impact**: Medium (application becomes unusable until file repaired)  
**Attack Vector**: Replace hiragana.csv with 10M-row file  
**Mitigation**: Python interpreter raises MemoryError before OS crash. Future: Add row count limit (10,000) with warning  
**Residual Risk**: Low (self-inflicted, requires deliberate action)  
**Related Risk**: RISK-024

**Threat D-2: Corrupted JSON Prevents Deck Loading**  
**Description**: Disk corruption or bug creates invalid JSON, blocks app usage  
**Likelihood**: Low (rare disk errors or software bugs)  
**Impact**: Medium (user cannot access deck until fixed)  
**Attack Vector**: Hardware failure, software bug, manual editing error  
**Mitigation**: JSON parsing wrapped in try/except, falls back to defaults with warning. Error message includes recovery instructions (delete file)  
**Residual Risk**: Low (users can recover by deleting corrupted file)  
**Related Risk**: RISK-006

**Threat D-3: Infinite Loop in FSRS Calculation**  
**Description**: Bug in FSRS algorithm causes infinite loop, hangs application  
**Likelihood**: Very Low (algorithm thoroughly tested)  
**Impact**: Medium (application hangs, requires force quit)  
**Attack Vector**: Edge case in stability/difficulty calculation  
**Mitigation**: 35+ unit tests covering edge cases. No recursion in FSRS code (no stack overflow risk)  
**Residual Risk**: Very Low  
**Related Risk**: RISK-003

### Elevation of Privilege

**Threat E-1: Path Traversal via Username**  
**Description**: Attacker enters username like "../../etc/passwd" to write files outside data directory  
**Likelihood**: Low (requires deliberate attack attempt)  
**Impact**: High (arbitrary file write on filesystem)  
**Attack Vector**: Username validation bypass  
**Mitigation**: Username validation restricts to alphanumeric + underscore/hyphen (regex ^[a-zA-Z0-9_-]+$). pathlib constructs paths safely  
**Residual Risk**: Very Low (validation prevents attack)  
**Related Risk**: RISK-022

**Threat E-2: Privilege Escalation via Malicious Code Injection**  
**Description**: Attacker injects Python code into CSV/JSON that gets executed  
**Likelihood**: Very Low (Python json/csv modules don't evaluate code)  
**Impact**: High (code execution with user's privileges)  
**Attack Vector**: Crafted JSON with malicious pickle data  
**Mitigation**: Application uses json module (safe), not pickle (unsafe). CSV parsed as data, not code  
**Residual Risk**: Very Low  
**Related Risk**: N/A

---

## Security Best Practices Implemented

1. **Input Validation**: All user inputs validated (username, minutes, intensity)
2. **Safe Deserialization**: JSON/CSV only, no pickle or eval()
3. **Path Safety**: pathlib used for all filesystem operations, prevents traversal
4. **No Network Access**: Zero HTTP requests, eliminates entire class of network attacks
5. **Principle of Least Privilege**: Application runs as user, no elevated permissions needed
6. **Defense in Depth**: Multiple validation layers (UI validation + backend validation)
7. **Graceful Degradation**: Errors caught and handled, never expose stack traces to user
8. **Transparent Data**: Plaintext formats allow user inspection, no hidden data

---

## Privacy Considerations

### Data Minimization
- Only collect data necessary for functionality: card content, learning state, user settings
- No demographic information, email, phone number, or real name required
- Username can be pseudonym

### User Control
- Users own their data (local storage in accessible formats)
- Can export/backup/delete data at any time
- No vendor lock-in (CSV format is universal)

### No Telemetry
- Zero analytics or tracking
- No phone-home functionality
- No anonymous usage statistics collected
- No crash reports sent to developer

### Local-Only Processing
- All computation happens locally
- No cloud services, APIs, or remote servers
- Internet connection never required
- Data never leaves local filesystem

### GDPR Alignment (Though Not Legally Required)
- Right to access: Data in plaintext files
- Right to rectification: Edit JSON/CSV directly
- Right to erasure: Delete user directory
- Right to data portability: CSV export
- Data protection by design: No network, minimal data

---

## Ethical Considerations

### No Dark Patterns
- Application never guilt-trips users for missing days
- No manipulative notifications ("Your streak is dying!")
- No artificial scarcity or FOMO tactics
- Daily limit can be overridden (respects user agency)

### No Addictive Gamification
- No points, badges, leaderboards
- No social comparison features
- No artificial rewards or psychological manipulation
- Focus on intrinsic learning motivation

### Accessibility
- Color-coded buttons aid comprehension (red/green semantic meaning)
- **Limitation**: Not colorblind-safe (red-green deficiency affects ~8% of males)
- **Future**: Add icons (X/✓) alongside colors
- **Limitation**: No screen reader testing, Tkinter provides basic ARIA

### Honest Communication
- Algorithm explained, not hidden as "magic"
- Success criteria realistic (memorization, not fluency)
- No false promises about learning speed
- Acknowledge limitations (Japanese proficiency requires more than flashcards)

### Educational Integrity
- FSRS-6 algorithm based on peer-reviewed research
- No pseudoscience or unvalidated methods
- Transparent about what app can/cannot do
- Respects cognitive science principles (spaced repetition, cognitive load)

---

## Incident Response Plan

### Scenario 1: Data Loss (User Deleted Directory)
**Response**:
1. Show clear error message: "Data directory not found"
2. Offer to recreate with defaults
3. Inform user progress is lost, suggest restoring from backup
4. Document backup strategy in README

### Scenario 2: Corrupted Metadata
**Response**:
1. Catch JSON parsing error
2. Log warning to console
3. Fall back to default values
4. Show user-friendly message: "Metadata corrupted, using defaults. Your cards are safe in CSV."
5. Suggest deleting corrupted .json files

### Scenario 3: Security Vulnerability Discovered
**Response**:
1. Assess severity (CVSS score)
2. If high: Issue immediate patch, notify users
3. If medium/low: Include in next release
4. Document in changelog and security advisory

### Scenario 4: User Reports Bug
**Response**:
1. Request system info (Python version, OS)
2. Request steps to reproduce
3. Check if data corruption involved (request JSON/CSV files)
4. Add regression test
5. Fix and release patch

---

## Security Testing Plan

### Penetration Testing Checklist
- [ ] Attempt path traversal via username input
- [ ] Inject SQL/code into CSV fields (expect no execution)
- [ ] Create CSV with 1M rows (expect graceful failure)
- [ ] Corrupt JSON with invalid syntax (expect fallback to defaults)
- [ ] Set extreme values in JSON (intensity=1000, stability=1e100)
- [ ] Create symlink attacks (username -> /etc)
- [ ] Test concurrent writes (two app instances)
- [ ] Memory exhaustion test (load 50K-card deck)

### Security Code Review
- [ ] No use of eval(), exec(), pickle.load()
- [ ] All filesystem operations use pathlib (not string concatenation)
- [ ] No HTTP libraries imported (requests, urllib)
- [ ] Input validation on all user inputs
- [ ] Error messages don't expose stack traces
- [ ] No hardcoded credentials (N/A for this app)
- [ ] Secrets not logged (N/A, no secrets)

---

## Risk Acceptance Statement

The following risks are consciously accepted for this MVP:

1. **No User Authentication**: Username-only login is sufficient for personal device use. Schools requiring authentication can add password feature in future iteration.

2. **No Data Encryption**: Plaintext storage prioritizes transparency and user control over confidentiality. Data content (hiragana flashcards) is not sensitive.

3. **No File Locking**: Single-user assumption means concurrent access is unlikely. Adding file locking would complicate code without significant benefit.

4. **Limited Accessibility**: Colorblind users can still use text labels, but optimal experience requires icon addition (future work).

5. **Manual Backup Responsibility**: Users must manage their own backups. Automatic backup would add complexity and potential privacy concerns (cloud sync).

---

**Risk Register Maintained By**: Student Candidate  
**STRIDE Analysis Conducted**: 2025-11-02  
**Last Security Review**: 2025-11-16  
**Next Review Date**: After each major feature addition

