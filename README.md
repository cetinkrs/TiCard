# TiCard — Vocabulary Learning App

A vocabulary learning application that uses the **Spaced Repetition** method to help you memorize English words effectively. Available as both a terminal (CLI) tool and a desktop app built with CustomTkinter.

## Features
- Create and manage decks (add / delete)
- Add, delete, and update words
- Spaced repetition algorithm (easy / medium / hard → automatic scheduling)
- Statistics screen (total decks, words per deck, today's study count)
- Desktop UI (CustomTkinter): deck management, word CRUD screens, and an interactive study flow (show word → reveal answer → rate difficulty)
- Local data storage with JSON
- Corrupted data protection (auto-backup on JSON error)

## Built With
- Python 3.x
- CustomTkinter (desktop UI)
- No external dependencies for the core logic (standard library only)

## How to Run
1. Make sure Python 3.x is installed
2. Clone the repository:
```bash
git clone https://github.com/cetinkrs/TiCard.git
```
3. Navigate to the project folder:
```bash
cd TiCard
```
4. Install the UI dependency:
```bash
pip install customtkinter
```
5. Run the desktop app:
```bash
python ui_test.py
```
Or run the terminal version instead:
```bash
python main.py
```

## Preview
\```
[1] Create Deck [2] Add Word [3] Study [4] Delete Word [5] Update Word
[6] Delete Deck [7] Statistics [8] Exit
Select an action: 7

=== Statistics ===
Total decks: 2

Words per deck:

English_B1: 5 words
Trial_1: 3 words

Today's total words to study: 4
\```

## Project Structure
\```
TiCard/
    main.py       # Terminal UI and menu
    ui_test.py    # Desktop UI (CustomTkinter)
    motor.py      # Core logic (deck & word management, spaced repetition)
    depolama.py   # Data layer (read/write JSON)
    test_motor.py # Unit tests (pytest)
\```

## Roadmap
- [x] Basic CRUD operations (create, read, update, delete)
- [x] Deck deletion
- [x] Spaced repetition algorithm
- [x] Refactoring (DRY principle, targeted error handling)
- [x] Error handling (corrupted JSON protection, invalid input handling)
- [x] Unit tests with pytest
- [x] Statistics screen
- [x] Desktop UI with CustomTkinter
- [ ] Refine spaced repetition algorithm (dynamic intervals based on review history)
- [ ] REST API layer with FastAPI
- [ ] PostgreSQL + SQLAlchemy integration
- [ ] Dockerize (FastAPI + PostgreSQL via docker-compose)
- [ ] Package as .exe with PyInstaller
- [ ] Architecture diagram & API documentation
- [ ] `test_motor.py` is written for the old JSON-based data layer and needs to be rewritten for PostgreSQL (including test database isolation, so tests don't touch production data).
## License
MIT License — feel free to use and modify.