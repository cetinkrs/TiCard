# TiCard — Vocabulary Learning App

A terminal-based vocabulary learning application that uses the **Spaced Repetition** method to help you memorize English words effectively.

## Features
- Create and manage decks (add / delete)
- Add, delete, and update words
- Spaced repetition algorithm (easy / medium / hard → automatic scheduling)
- Statistics screen (total decks, words per deck, today's study count)
- Local data storage with JSON
- Corrupted data protection (auto-backup on JSON error)

## Built With
- Python 3.x
- No external dependencies (standard library only)

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
4. Run the app:
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
    main.py # Terminal UI and menu
    motor.py # Core logic (deck & word management, spaced repetition)
    depolama.py # Data layer (read/write JSON)
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
- [ ] SQLite database integration
- [ ] Desktop UI with CustomTkinter
- [ ] Package as .exe with PyInstaller
## License
MIT License — feel free to use and modify. 
