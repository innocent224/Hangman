# Copilot Instructions for Hangman Game (Flask)

## Overview
- This is a web-based Hangman game using Flask (Python) for the backend and HTML/CSS/JS for the frontend.
- The main backend is in `hangman_server.py` at the project root. It exposes REST endpoints for game logic and serves the main page.
- Frontend assets (JS, CSS, sounds) are in the `static/` directory. The main HTML template is in `templates/index.html`.
- There is a nested `hangman_game/app/` directory for an alternative or modular Flask app structure, but the main entrypoint is `hangman_server.py`.

## Key Files & Structure
- `hangman_server.py`: Flask app, all main routes (`/`, `/start_game`, `/guess`, `/get_state`, `/hint`).
- `static/`: JS, CSS, and sound files for the game UI and effects.
- `templates/index.html`: Main HTML template rendered by Flask.
- `test_hangman.py`: Unittest-based API tests for the Flask backend.
- `requirements.txt`: Flask and flask-cors dependencies.

## Developer Workflows
- **Run the app:**
  ```
  pip install -r requirements.txt
  python hangman_server.py
  # Visit http://127.0.0.1:5000/
  ```
- **Run tests:**
  ```
  python test_hangman.py
  ```
- **Frontend changes:** Edit files in `static/` and `templates/`.
- **Backend changes:** Edit `hangman_server.py`.

## Patterns & Conventions
- Game state is stored in Flask `session` (per user/browser).
- All game logic (word selection, guesses, scoring, hints) is handled server-side.
- API returns JSON for frontend JS to update UI.
- Categories and words are hardcoded in `hangman_server.py`.
- Difficulty affects allowed guesses (see `difficulty_guesses`).
- Hints cost a guess and reveal a random unguessed letter.
- Score resets on loss, increments on win.

## Integration Points
- No database or external API dependencies.
- Sound and animation handled in frontend JS/CSS.
- CORS enabled for local development (flask-cors).

## Examples
- To add a new category, update the `data` dict in `hangman_server.py`.
- To add a new route, follow the Flask route pattern in `hangman_server.py`.
- To add a new test, see `test_hangman.py` for unittest structure.

---
For more details, see `README.md` in the project root and in `hangman_game/`.