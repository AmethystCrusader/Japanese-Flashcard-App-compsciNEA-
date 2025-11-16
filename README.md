# Japanese-Flashcard-App-compsciNEA-
A comprehensive Japanese hiragana learning application implementing FSRS-6 spaced repetition algorithm for OCR H446 Computer Science NEA project.

## Features

- **FSRS-6 Spaced Repetition**: Scientifically-validated scheduling algorithm for optimal review intervals
- **User-Friendly Intensity Control**: Set study time in minutes, automatically mapped to algorithm parameters
- **Manual Intensity Override**: Power users can directly control scheduling intensity
- **Binary Grading**: Simplified "Again"/"Good" grading reduces cognitive load
- **Daily Review Limits**: Prevent cognitive overload with configurable daily caps
- **Progress Tracking**: View card states, review counts, and FSRS parameters in real-time
- **Local-Only Storage**: Complete privacy, no internet required, all data stored locally
- **Transparent Algorithm**: All FSRS parameters visible and explained

## Quick Start

1. **Requirements**: Python 3.10+ with Tkinter
2. **Run**: `python3 flashcard_app.py`
3. **Login**: Enter any username (creates profile automatically)
4. **Practice**: Click "Practice" to start reviewing hiragana flashcards

## NEA Documentation

Comprehensive design documentation for OCR H446 Band 4 (A*) assessment:

### Core Design Documents

- **[NEA_DESIGN.md](docs/NEA_DESIGN.md)** - Main design document (~8,500 words)
  - Problem definition and stakeholder analysis
  - Systematic decomposition and architecture
  - Detailed algorithms with pseudocode and flowcharts
  - Data model and validation strategy
  - Test plans (iterative and post-iterative)
  - Performance analysis and Big-O complexity
  - Security (STRIDE threat model) and privacy
  - Accessibility and ethical considerations
  - Requirements traceability and evaluation plan

- **[NEA_REQUIREMENTS_TRACEABILITY.md](docs/NEA_REQUIREMENTS_TRACEABILITY.md)** - 57 requirements mapped to design, implementation, algorithms, and tests

- **[NEA_ITERATION_LOG.md](docs/NEA_ITERATION_LOG.md)** - 14 iterations documenting development decisions, pivots, and impacts

- **[NEA_RISK_SECURITY.md](docs/NEA_RISK_SECURITY.md)** - 26 risks analyzed with STRIDE threat modeling

- **[NEA_TEST_STRATEGY.md](docs/NEA_TEST_STRATEGY.md)** - Comprehensive testing plan covering unit, integration, system, acceptance, performance, usability, and retention study methodologies

### Technical Reference

- **[cheat-sheet-fsrs6.md](docs/cheat-sheet-fsrs6.md)** - Quick reference for FSRS-6 parameters and usage
- **[flowcharts-fsrs6.md](docs/flowcharts-fsrs6.md)** - Application flow diagrams
- **[fsrs6-mapping.md](docs/fsrs6-mapping.md)** - Parameter naming conventions and API reference

## Project Structure

````
├── flashcard_app.py         # Main application controller
├── fsrs.py                   # FSRS-6 scheduling algorithm
├── models.py                 # Data models (Card, DeckMetadata)
├── persistence.py            # JSON/CSV persistence layer
├── user_settings.py          # Settings and intensity mapping
├── gui.py                    # Tkinter GUI screens
├── hiragana.csv              # Hiragana flashcard deck
├── test_app.py               # Unit tests for FSRS
├── test_intensity.py         # Unit tests for intensity mapping
├── test_gui.py               # GUI component tests
└── docs/                     # NEA documentation
    ├── NEA_DESIGN.md
    ├── NEA_REQUIREMENTS_TRACEABILITY.md
    ├── NEA_ITERATION_LOG.md
    ├── NEA_RISK_SECURITY.md
    ├── NEA_TEST_STRATEGY.md
    ├── cheat-sheet-fsrs6.md
    ├── flowcharts-fsrs6.md
    └── fsrs6-mapping.md
````

## Development Status

**Completed Features**:
- ✓ User management (username-only login)
- ✓ CSV deck loading with JSON metadata merge
- ✓ FSRS-6 binary grading algorithm
- ✓ Practice view with flashcard presentation
- ✓ Statistics and progress tracking
- ✓ Minutes-to-intensity mapping
- ✓ Manual intensity override
- ✓ Daily review limits with override option
- ✓ Input validation and error handling
- ✓ Comprehensive NEA documentation

**Future Enhancements** (see NEA_DESIGN.md §19):
- Audio pronunciation playback
- Keyboard shortcuts
- Multiple deck support
- Graphical statistics (charts)
- Export progress reports
- Mobile app (Kivy port)

## Testing

Run unit tests:
````bash
python3 test_app.py
python3 test_intensity.py
````

See [NEA_TEST_STRATEGY.md](docs/NEA_TEST_STRATEGY.md) for comprehensive testing methodology.

## License

Educational project for OCR H446 Computer Science NEA assessment.

## Credits

- FSRS-6 algorithm based on research by Jarrett Ye et al. (2024)
- Hiragana character set: Standard Japanese syllabary
- Developed for OCR H446 Computer Science A-Level NEA
