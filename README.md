# TiCard — Vocabulary Learning App

A terminal-based vocabulary learning application that uses the **Spaced Repetition** 
method to help you memorize English words effectively.

## Features
- Create and manage decks
- Add, delete, and update words
- Spaced repetition algorithm (easy / medium / hard → automatic scheduling)
- Local data storage with JSON

## Built With
- Python 3.x
- No external dependencies (standard library only)

## How to Run
1. Make sure Python 3.x is installed
2. Clone the repository:
\```bash
git clone https://github.com/cetinkrs/ticard.git
\```
3. Navigate to the project folder:
\```bash
cd ticard
\```
4. Run the app:
\```bash
python main.py
\```

## Preview
\```
[1] Create Deck  [2] Add Word  [3] Study  [4] Delete Word  [5] Update Word  [6] Exit
Select an action: 3

Next word: Resilient
Press Enter to see the answer.

Meaning: Able to recover quickly from difficulties
Example: He is very resilient after failures.

How difficult was it?
[1] Easy (4 days later)
[2] Medium (1 day later)
[3] Hard (10 minutes later)
\```

## Project Structure
\```
ticard/
    main.py        # Terminal UI and menu
    motor.py       # Core logic (deck & word management, spaced repetition)
    depolama.py    # Data layer (read/write JSON)
\```

## Roadmap
- [x] Basic CRUD operations (create, read, update, delete)
- [x] Spaced repetition algorithm
- [x] Refactoring (DRY principle, targeted error handling)
- [ ] Strengthen error handling (corrupted JSON protection)
- [ ] SQLite database integration
- [ ] Desktop UI with CustomTkinter

## License
MIT License — feel free to use and modify. 
