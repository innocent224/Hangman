from flask import Flask, render_template, request, jsonify, session
import random
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'hangman_secret_key'
CORS(app)

# Categories and words
data = {
    'Animals': ['elephant', 'giraffe', 'kangaroo', 'alligator', 'dolphin', 'penguin', 'rhinoceros', 'chimpanzee'],
    'Fruits': ['banana', 'strawberry', 'pineapple', 'watermelon', 'blueberry', 'mango', 'pomegranate', 'apricot'],
    'Countries': ['brazil', 'germany', 'australia', 'canada', 'japan', 'nigeria', 'sweden', 'portugal'],
    'Sports': ['football', 'basketball', 'cricket', 'badminton', 'baseball', 'hockey', 'volleyball', 'tennis']
}

# Difficulty settings
difficulty_guesses = {
    'easy': 10,
    'medium': 7,
    'hard': 5
}

# ---------------- ROUTES ---------------- #

@app.route('/')
def index():
    """Serve the main game page with categories."""
    return render_template('index.html', categories=list(data.keys()))

@app.route('/start_game', methods=['POST'])
def start_game():
    """Start a new game with chosen category and difficulty."""
    category = request.json.get('category')
    difficulty = request.json.get('difficulty')

    if not category or not difficulty:
        return jsonify({'error': 'Category and difficulty required'}), 400

    word = random.choice(data[category])
    session['word'] = word
    session['guesses_left'] = difficulty_guesses.get(difficulty, 7)
    session['guessed_letters'] = []
    session['score'] = session.get('score', 0)

    return jsonify({
        'word_length': len(word),
        'guesses_left': session['guesses_left'],
        'score': session['score']
    })

@app.route('/guess', methods=['POST'])
def guess():
    """Handle a player's guess."""
    letter = request.json.get('letter', '').lower()

    if not letter or len(letter) != 1:
        return jsonify({'error': 'Invalid guess'}), 400

    word = session.get('word', '')
    guessed_letters = session.get('guessed_letters', [])

    # Already guessed
    if letter in guessed_letters:
        return jsonify({'status': 'already_guessed'})

    guessed_letters.append(letter)
    session['guessed_letters'] = guessed_letters

    # Correct guess
    if letter in word:
        if all(l in guessed_letters for l in word):
            session['score'] += 1
            return jsonify({'status': 'win', 'word': word, 'score': session['score']})
        else:
            return jsonify({'status': 'correct', 'guessed_letters': guessed_letters})

    # Incorrect guess
    session['guesses_left'] -= 1
    if session['guesses_left'] <= 0:
        session['score'] = 0
        return jsonify({'status': 'lose', 'word': word, 'score': session['score']})
    else:
        return jsonify({
            'status': 'incorrect',
            'guesses_left': session['guesses_left'],
            'guessed_letters': guessed_letters
        })

@app.route('/get_state', methods=['GET'])
def get_state():
    """Get the current state of the game."""
    word = session.get('word', '')
    guessed_letters = session.get('guessed_letters', [])
    display = [l if l in guessed_letters else '_' for l in word]

    return jsonify({
        'display': display,
        'guesses_left': session.get('guesses_left', 0),
        'guessed_letters': guessed_letters,
        'score': session.get('score', 0)
    })

@app.route('/hint', methods=['POST'])
def hint():
    """Reveal the word and end the game as a loss."""
    word = session.get('word', '')
    session['score'] = 0
    session['guesses_left'] = 0
    session['guessed_letters'] = list(set(word))

    return jsonify({
        'status': 'lose',
        'word': word,
        'score': session['score'],
        'hint': word
    })

# ---------------- RUN APP ---------------- #

if __name__ == '__main__':
    app.run(debug=True)