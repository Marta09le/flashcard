# Flashcard Vault

A small web app for vocabulary flashcards + quiz.

## Features
- Add word / translation / example
- View list of cards
- Delete a card
- Quiz mode: type the translation

## Run locally (Windows / macOS / Linux)
1) Create & activate a virtual environment (recommended)
2) Install deps
3) Start the server

### 1) Install dependencies
```bash
pip install -r requirements.txt
```

### 2) Run
```bash
uvicorn app.main:app --reload
```

Open in browser:
- http://127.0.0.1:8000

## Project structure
```
flashcard-vault/
  app/
    main.py
    db.py
    models.py
    templates/
    static/
  requirements.txt
  README.md
```

## Git (quick start)
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <YOUR_REPO_URL>
git push -u origin main
```
