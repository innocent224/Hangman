# Hangman Game (Web Version)

A classic Hangman word-guessing game with a modern web interface, built using Python (Flask) for the backend and HTML/CSS/JavaScript for the frontend.

## Features
- Category selection (Animals, Fruits, Countries, Sports)
- Difficulty modes (Easy, Medium, Hard)
- Virtual keyboard for guessing
- Score and high score tracking
- Fun facts/motivational quotes after each game
- Animated word reveal on win/lose
- Hangman drawing updates as you guess
- Hint button (reveals a random letter at the cost of a guess)
- Sound effects (win/lose/click)
- Timer (count-up/countdown, pause/resume, warning color, customizable duration)
- Responsive and modern UI

## How to Run
1. **Install dependencies:**
   ```
   pip install flask flask-cors
   ```
2. **Start the server:**
   ```
   cd hangman_game
   python hangman_server.py
   ```
3. **Open your browser:**
   Go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## File Structure
```
hangman_game/
├── hangman_server.py      # Flask backend
├── static/
│   ├── style.css          # Game styles
│   ├── script.js          # Frontend logic
│   ├── win.mp3            # Win sound
│   ├── lose.mp3           # Lose sound
│   └── click.mp3          # Button click sound
├── templates/
│   └── index.html         # Main game UI
├── test_hangman.py        # Backend API tests
└── README.md              # This file
```

## Customization
- **Add more categories/words:** Edit the `data` dictionary in `hangman_server.py`.
- **Change timer settings:** Use the timer controls in the UI.
- **Change sounds:** Replace the MP3 files in `static/`.

## Testing
Run backend API tests with:
```
python test_hangman.py
```

## Credits
- Built with Flask, HTML, CSS, and JavaScript.
- Sound effects and fun facts are for demonstration purposes.

---
Enjoy playing and customizing your Hangman game!