# Hangman Game

This project is a simple web-based Hangman game built using Flask. Players can choose a category and difficulty level, make guesses, and receive hints as they try to guess the word.

## Project Structure

```
hangman_game
├── app
│   ├── __init__.py
│   ├── routes.py
│   └── templates
│       └── index.html
├── static
│   ├── style.css
│   └── script.js
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd hangman_game
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Flask application:
   ```
   flask run
   ```

2. Open your web browser and go to `http://127.0.0.1:5000`.

## Game Instructions

- Select a category and difficulty level to start the game.
- Guess letters to try to figure out the word.
- Use hints if you get stuck, but be mindful of your remaining guesses!

## Dependencies

- Flask
- Flask-CORS

## License

This project is licensed under the MIT License.